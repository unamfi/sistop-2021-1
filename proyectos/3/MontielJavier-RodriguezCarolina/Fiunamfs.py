#!/usr/bin/python3 
import os, struct, time, datetime, math

class Fiunamfs:
  def __init__(self):
    self.tamanio_sector = 512
    self.tamanio_cluster = 2*self.tamanio_sector
    self.sistema_archivo = open("fiunamfs.img","r+b")
    self.a_32 = struct.Struct('<L')

  def verificacion(self):
    self.sistema_archivo.seek(21)
    nombre = self.sistema_archivo.read(14)
    
    if nombre == "FiUnamFS2021-1".encode():

      self.sistema_archivo.seek(10)
      version = self.sistema_archivo.read(4)
      self.sistema_archivo.seek(20)
      etiqueta = self.sistema_archivo.read(16)
      self.sistema_archivo.seek(40)
      tamanio_cluster = self.a_32.unpack(self.sistema_archivo.read(4))[0]
      self.sistema_archivo.seek(44)
      num_clusters_directorio = self.a_32.unpack(self.sistema_archivo.read(4))[0]
      self.sistema_archivo.seek(48)
      num_clusters_unidad = self.a_32.unpack(self.sistema_archivo.read(4))[0]

      print('Nombre del sistema de archivos: ', nombre.decode())
      print('Versión: ',version.decode())
      print('Etiqueta del Volumen',etiqueta.decode())
      print('Tamaño de cluster: ',tamanio_cluster)
      print('Numero de clusters por directorio: ',num_clusters_directorio)
      print('Número de clusters que mide la unidad completa: ',num_clusters_unidad)


    else:
      print('Con este disco no puedo trabajar')
      self.sistema_archivo.close()

  def listar_archivos(self, metadatos = False):
    archivos = []

    for i in range(0,64):
      posicion = self.tamanio_cluster+(i*64)
      self.sistema_archivo.seek(posicion)
      nombre_archivo = self.sistema_archivo.read(14)

      if nombre_archivo != b'Xx.xXx.xXx.xXx':
        if metadatos:
          archivo = []
          archivo.append(nombre_archivo)
          self.sistema_archivo.seek(posicion+16)
          archivo.append(self.a_32.unpack(self.sistema_archivo.read(4))[0])
          self.sistema_archivo.seek(posicion+20)
          archivo.append(self.a_32.unpack(self.sistema_archivo.read(4))[0])
          archivos.append(archivo)

    return archivos
    

  def ls(self):
    lista_archivos = self.listar_archivos(True)

    for i in lista_archivos:
      print("-> ",i[0].decode(),"Tamaño: ",i[1]," Cluster inicial",i[2])

  def existe_archivo(self, nombre_archivo):
    archivos = self.listar_archivos(True)
    for i in archivos:
      if nombre_archivo == i[0].decode().strip():
        return i

    return None

  def existe_archivo_en_sistema(self,ruta_sistema):
    return os.path.isfile(ruta_sistema)

  def convertir_a_formato_fecha(self,fecha_en_segundos):
    return datetime.datetime.fromtimestamp(fecha_en_segundos).strftime("%Y%m%d%I%M%S")
      
  def obtener_info_archivo(self,ruta_sistema):
    info_archivo = []
    archivo_a_copiar = os.stat(ruta_sistema)
    info_archivo.append(archivo_a_copiar.st_size)
    info_archivo.append(self.convertir_a_formato_fecha(archivo_a_copiar.st_ctime))
    return info_archivo

  def verifica_espacio_disponible(self,tamanio_archivo):
    archivos_almacenados = self.listar_archivos(True)
    tamanio_ocupado = 0
    if len(archivos_almacenados) > 0:
      for i in archivos_almacenados:
        tamanio_ocupado += i[1]
    
    tamanio_disponible = 1474560 - tamanio_ocupado - 5120

    return True if tamanio_disponible > tamanio_archivo else False

  
  def ordenar_archivos(self,lista_archivos,elemento_criterio):
    return sorted(lista_archivos, key=lambda dato: dato[elemento_criterio])

  def asigna_cluster_inicial(self,tamanio_archivo):
    archivos = self.listar_archivos(True)
    archivos = self.ordenar_archivos(archivos,2)
    for i in range (0,len(archivos)-1):
      #print("actual ",archivos[i],"\nsiguiente ",archivos[i+1])
      tamanio_en_clusters = math.floor(archivos[i][1]/1024)
      cluster_final_actual = archivos[i][2] + tamanio_en_clusters
      tamanio_en_clusters = math.floor(archivos[i+1][1]/1024)
      cluster_final_siguiente = archivos[i+1][2] + tamanio_en_clusters
      espacio_entre_bloques = (cluster_final_siguiente - cluster_final_actual) - 1
      if espacio_entre_bloques >= math.floor(tamanio_archivo/1024):
        return cluster_final_actual + 1
    tamanio_en_clusters = math.floor(archivos[-1][1]/1024)
    cluster_final_actual = archivos[-1][2] + tamanio_en_clusters
    tamanio_restante = (1440 - cluster_final_actual)*1024
    
    if tamanio_restante >= tamanio_archivo:
      return cluster_final_actual + 1
    
    return -1

  def escribe_archivo(self,ruta_sistema,info_archivo,cluster_inicial):
    nombre = ruta_sistema.split('/')
    for i in range(0,64):
      posicion = self.tamanio_cluster+(i*64)
      self.sistema_archivo.seek(posicion)
      nombre_archivo = self.sistema_archivo.read(14)
      if nombre_archivo == b'Xx.xXx.xXx.xXx':
        print("si encontro")
        posicion = self.tamanio_cluster+(i*64)
        self.sistema_archivo.seek(posicion)
        self.sistema_archivo.write(nombre[-1].encode())

        self.sistema_archivo.seek(posicion+15)
        self.sistema_archivo.write(self.a_32.pack(info_archivo[0]))

        self.sistema_archivo.seek(posicion+16)
        self.sistema_archivo.write(self.a_32.pack(info_archivo[0]))

        self.sistema_archivo.seek(posicion+20)
        self.sistema_archivo.write(self.a_32.pack(cluster_inicial))

        self.sistema_archivo.seek(posicion+24)
        self.sistema_archivo.write(time.strftime("%Y%m%d%I%M%S").encode())

        self.sistema_archivo.seek(posicion+38)
        self.sistema_archivo.write(info_archivo[1].encode())
        break

    archivo_origen = open(ruta_sistema,"rb")
    contenido = archivo_origen.read(info_archivo[0])
    self.sistema_archivo.seek(cluster_inicial*1024)
    self.sistema_archivo.write(contenido)
    archivo_origen.close()

  def copiar_a_fiunamfs(self,ruta_sistema,ruta_disqute):
    if self.existe_archivo_en_sistema(ruta_sistema): 
      info_archivo = self.obtener_info_archivo(ruta_sistema)
      if self.verifica_espacio_disponible(info_archivo[0]):
        cluster_inicio = self.asigna_cluster_inicial(info_archivo[0])
        if cluster_inicio != -1:
          self.escribe_archivo(ruta_sistema,info_archivo,cluster_inicio)
        else:
          print("NO entro :(")
      else:
        print("no hay espacio disponible") 
      
    else:
      print("no existe :c")

  def copiar_a_sistema(self,origen,destino):
    archivo = self.existe_archivo(origen)
    print(archivo)
    if archivo != None:
      self.sistema_archivo.seek(archivo[2]*self.tamanio_cluster)
      contenido = self.sistema_archivo.read(archivo[1])
      destino = open(destino+archivo[0].decode().strip(),"wb")
      destino.write(contenido)
      destino.close()
      print("se copio")
    else:
      print("no se copio")
        

  def cp(self,origen,destino,l=None):
    if l != None and l == "-l":
      print("al disquete")
    elif l == None:
      self.copiar_a_sistema(origen,destino)
    else:
      print("error argumento inválido")
  #cp origen destino
  #cp -l (del sistema al disckete) ar1 ar2
  #cp ar1 ar2 (del disckete al sist)

    '''
    
    -> verificar que el archivo existe
    -> obtener sus metadatos 
    -> listar_archivos(True)
      ->sumar el tamaño de todos los archivos
      ->si el tamaño > al del archivo
        ->pegar los metadatos al directorio
        ->pegar el contenido
       

    '''

    '''
    --tentativo para desfragmentar
    -> crear el bitmap para ver los espacios
    -> recorrer el bitmap
      -> en caso de encontrar un hueco 
        -> analizar tamaño del hueco 
        -> recorrer el siguiente bloque de informacion al espacio hueco
    '''

    '''
    -> listamos todos los archivos 
    -> vemos si podemos ordenar todo en base al cluster de inicio
    [[x,6],[x,5]] -> [[x,5],[x,6]]
    -> analizamos si el cluster actual y el proximo es el continuo (para todo el arreglo) (si el cluster es el 12 y pesa 3 clusters, termina 
    en el 15, por lo tanto el proximo archivo inicie en el cluster 16)
      -> en caso de que no vemos cuanto espacio hay
      -> analizamos si el espacio es suficiente para almacenar el archivo 
      -> si el tamaño es suficiente lo escribimos tanto en el directorio como en el espacio disponible 
      ->en caso contrario seguimos 
    ->  si no se logro encontrar hueco entre clusters vemos si hay espacio desde el ultimo cluster
    hasta el final del espacio disponible en disco 
    -> en caso de haber espacio almacenamos el archivo al final 
    '''


if __name__ == '__main__':
  sistema = Fiunamfs()
  sistema.copiar_a_fiunamfs('/home/carol/Desktop/hola1.pdf','')
  #sistema.ls()

'''
-> readme tam = 30751 c = 5
-> logo tam = 0 c = 37
-> datetime tam 63 c = 352
-> hola tam 4000  c =  38
'''