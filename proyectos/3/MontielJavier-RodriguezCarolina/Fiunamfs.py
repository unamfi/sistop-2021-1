#!/usr/bin/python3 
'''
@Autores:         Montiel Martinez Luis Javier
                  Rodríguez Dávalos Carolina 

@Fecha creación:  28/12/2020
@Descripción:     Implementación de un sistema de archivos para el disquete FIunamFS

'''

import os, struct, time, datetime, math
from getpass import getuser

class Fiunamfs:

  def __init__(self):
    self.tamanio_sector = 512
    #Como un cluster mide 2 sectores se uso como referencia para la definicion de dicho valor
    self.tamanio_cluster = 2*self.tamanio_sector
    self.sistema_archivo = open("fiunamfs.img","r+b")
    #Establecemos una estructura que opere en formato little endian a 32 bits
    #Se usará con el fin de poder traducir numeros en hexadecimal a decimal usando
    #Las funciones unpack() y pack() para su proposito contrario
    self.a_32 = struct.Struct('<L')

  def verificacion(self):
    #Se realiza la verificación que el nombre del sistema de archivos sea correcto
    self.sistema_archivo.seek(0)
    nombre = self.sistema_archivo.read(9)
    #En caso de validar el nombre lee los demás metadatos
    if nombre == "FiUnamFS".encode():

      self.sistema_archivo.seek(10)
      version = self.sistema_archivo.read(4)
      self.sistema_archivo.seek(20)
      etiqueta = self.sistema_archivo.read(16)
      self.sistema_archivo.seek(40)
      #El método unpack devuelve una tupla y recuperamos posición cero para obtener el dato deseado
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
    #Función que lista el nombre de los archivos con base al argumento metadatos
    archivos = []

    #Recorre todas las posibles entradas del directorio 
    for i in range(0,64):
      posicion = self.tamanio_cluster+(i*64)
      self.sistema_archivo.seek(posicion)
      nombre_archivo = self.sistema_archivo.read(15)

      if nombre_archivo != b'Xx.xXx.xXx.xXx.':
        if metadatos:
          archivo = []
          archivo.append(nombre_archivo)
          self.sistema_archivo.seek(posicion+16)
          archivo.append(self.a_32.unpack(self.sistema_archivo.read(4))[0])
          self.sistema_archivo.seek(posicion+20)
          archivo.append(self.a_32.unpack(self.sistema_archivo.read(4))[0])
          archivos.append(archivo)
        else:
          archivos.append(nombre_archivo)

    return archivos
    
  def existe_archivo(self, nombre_archivo):
    #Verifica la existencia de un archivo en el disquete
    archivos = self.listar_archivos(True)
    for i in archivos:
      if nombre_archivo == i[0].decode().strip():
        return i

    return None

  def existe_archivo_en_sistema(self,ruta_sistema):
    #Verifica la existencia de un archivo en el sistema
    return os.path.isfile(ruta_sistema)

  def convertir_a_formato_fecha(self,fecha_en_segundos):
    #Convierte el tiempo representado en segundos al formato necesario para el
    #disqute
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
    #Se considera el espacio total del disquete (1475560) convertidos a bytes y 
    # se les resta el tamaño ocupado por todos los archivos en el floppy
    # asi como el tamaño conformado por los clusters 0 a 4 (5120)
    tamanio_disponible = 1474560 - tamanio_ocupado - 5120

    return True if tamanio_disponible > tamanio_archivo else False

  
  def ordenar_archivos(self,lista_archivos,elemento_criterio):
    #Función dedica a ordenar la lista de archivos existentes en base al cluster
    #de inicio (dato[elemento_criterio])
    return sorted(lista_archivos, key=lambda dato: dato[elemento_criterio])

  def asigna_cluster_inicial(self,tamanio_archivo):
    archivos = self.listar_archivos(True)
    archivos = self.ordenar_archivos(archivos,2)
    #Busca en todo el disquete un cluster en el cual quepa nuestro archivo
    #deseado
    for i in range (0,len(archivos)-1):
      #obtenermos el tamaño en base al numero de clusters que ocupa el archivo
      #a analizar (archivos[i][1])
      tamanio_en_clusters = math.floor(archivos[i][1]/1024)
      #calculamos el cluster final del archivo en el cual se ubica
      cluster_final_actual = archivos[i][2] + tamanio_en_clusters
      tamanio_en_clusters = math.floor(archivos[i+1][1]/1024)
      cluster_final_siguiente = archivos[i+1][2] + tamanio_en_clusters
      #obtenemos el espacio que puede existir entre dos archivos
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
    #Método que se encarga de colocar el archivo en el espacio ideal dentro del 
    #disquete
    nombre = ruta_sistema.split('/')
    for i in range(0,64):
      posicion = self.tamanio_cluster+(i*64)
      self.sistema_archivo.seek(posicion)
      nombre_archivo = self.sistema_archivo.read(15)
      if nombre_archivo == b'Xx.xXx.xXx.xXx.':
        posicion = self.tamanio_cluster+(i*64)
        self.sistema_archivo.seek(posicion)
        self.sistema_archivo.write(nombre[-1].ljust(15).encode())

        self.sistema_archivo.seek(posicion+15)
        self.sistema_archivo.write("-".encode())

        self.sistema_archivo.seek(posicion+16)
        self.sistema_archivo.write(self.a_32.pack(info_archivo[0]))

        self.sistema_archivo.seek(posicion+20)
        self.sistema_archivo.write(self.a_32.pack(cluster_inicial))

        self.sistema_archivo.seek(posicion+24)
        self.sistema_archivo.write(time.strftime("%Y%m%d%I%M%S").encode())

        self.sistema_archivo.seek(posicion+38)
        self.sistema_archivo.write(info_archivo[1].encode())
        break

      self.sistema_archivo.seek(posicion)
      nombre_archivo = self.sistema_archivo.read(15)
    archivo_origen = open(ruta_sistema,"rb")
    contenido = archivo_origen.read(info_archivo[0])
    self.sistema_archivo.seek(cluster_inicial*1024)
    self.sistema_archivo.write(contenido)
    archivo_origen.close()

  def copiar_a_fiunamfs(self,ruta_sistema):
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
    #Método que se posiciona en el lugar indicado dentro del disqute para 
    #leer el archivo a copiar y escribirlo dentro de la unidad
    archivo = self.existe_archivo(origen)
    if archivo != None:
      self.sistema_archivo.seek(archivo[2]*self.tamanio_cluster)
      contenido = self.sistema_archivo.read(archivo[1])
      destino = open(destino+archivo[0].decode().strip(),"wb")
      destino.write(contenido)
      destino.close()
    else:
      print("no se copio")
        
  def archivo_existe(self,nombre_archivo):
    #Método el cual verifica si dentro del floppy existe dicho archivo
    posicion_directorio = 0
    for i in range(0,64):
      posicion = self.tamanio_cluster+(i*64)
      self.sistema_archivo.seek(posicion)
      nombre = self.sistema_archivo.read(15)

      if nombre_archivo == nombre.decode().strip():
        return posicion_directorio
      posicion_directorio += 1
    return -1

  def elimina_entrada_directorio(self,posicion):
    #Método en el cual formatea cierta entrada de memoria a su configuracion por
    #defecto
    ubicacion = self.tamanio_cluster+(posicion*64)
    self.sistema_archivo.seek(ubicacion)
    self.sistema_archivo.write(b'Xx.xXx.xXx.xXx.')
    self.sistema_archivo.seek(ubicacion+15)
    self.sistema_archivo.write("-".encode())
    self.sistema_archivo.seek(ubicacion+16)
    self.sistema_archivo.write(self.a_32.pack(0000))
    self.sistema_archivo.seek(ubicacion+24)
    self.sistema_archivo.write("0000000000000000000000000000".encode())

  def exit(self):
    self.sistema_archivo.close()
    return False
      
  def rm(self,nombre_archivo):
    posicion = self.archivo_existe(nombre_archivo)
    if posicion != -1:
      self.elimina_entrada_directorio(posicion)
    else:
      print("no esta")
      
  def cp(self,origen,destino,l=None):
    #Función encargada de copiar un archivo, ya sea del sistema a fiunamfs
    #o de fiunamfs al sistema
    #NOTA: consideramos que la linea de comandos se ingrese ruta absoluta en
    #siempre que se refiera uno al sistema del usuario y terminar con / en caso de 
    # copiarse un archivo a fiunamfs 
    #(ej. /home/fulano/.../carpeta destino/)
    #
    #Para el caso de copiar un archivo a fiunamfs se debe de colocar la ruta absoluta
    #(ej. /home/fulano/.../carpeta destino/nombre archivo)
    if l != None and l == "-l":
      self.copiar_a_sistema(origen,destino)
    elif l == None:
      self.copiar_a_fiunamfs(origen)
    else:
      print("error argumento inválido")

  def ls(self):
    #Función que muestra los elementos provenientes del disquete
    lista_archivos = self.listar_archivos()

    for i in lista_archivos:
      print("->",i.decode())
  
  def help(self):
    print("******************************************************************************************\n")
    print("Lista de comandos: \n")
    print("$ help -> despliega el manual")
    print("$ exit -> sale de FinunamFS")
    print("$ ls   -> lista los archivos")
    print("$ rm <nombre_archivo>   -> elimina un archivo")
    print("$ cp -l <nombre_archivo> </ruta_destino/>  -> copia un archivo de fiunamfs al sistema")
    print("$ cp <ruta_absoluta_archivo> -> copia un archivo de sistema a fiunamfs\n")
    print("******************************************************************************************\n")


  def ejecuta_comando(self,comando):
    salida = True
    op= comando[0]
    if op == "exit":
      salida = self.exit()
    elif op == "cp":
      if len(comando) >1 and comando[1] == '-l' and len(comando) == 4:
        self.cp(comando[2],comando[3],comando[1])
      elif len(comando) == 2:
        self.cp(comando[1],'')
      else:
        print("\nNúmero de argumentos inválido")
        print("La estructura correcta es: \n")
        print("cp -l /<usuario>/.../carpeta destino/<nombre archivo> -> para copiar a fiunamfs a sistema")
        print("cp <archivo en fiunamfs> /<usuario>/.../carpeta destino/ -> para copiar a fiunamfs\n")
    elif op == "ls":
      if len(comando) == 1:
        self.ls()
      else:
        print("\nEstructura invalida")
        print("La estructura completa es: \n\nls\n")
    elif op == "rm":
      if len(comando) == 2:
        self.rm(comando[1])
      else:
        print("\nEstructura inválida")
        print("La estructura correcta es: \n\nrm <nombre archivo>\n")
    elif op == "help":
      if len(comando) == 1:
        self.help()
    else:
      print("Inválido")
    
    return salida
    
  
  def tratar_cadena(self,comando):
    return comando.split()

  def inicia_interfaz(self):
    salida = True
    usuario = getuser()
    print("Para conocer los comandos válidos, escriba en línea de comando: help")
    while salida:
      entrada = input("["+usuario+"@fiunamfs fiunamfs2021-1]$ ")
      comando = self.tratar_cadena(entrada)
      salida = self.ejecuta_comando(comando)
      

if __name__ == '__main__':
  sistema = Fiunamfs()
  sistema.inicia_interfaz()
  