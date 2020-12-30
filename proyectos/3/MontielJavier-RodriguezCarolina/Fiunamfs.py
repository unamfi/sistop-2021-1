#!/usr/bin/python3
import os
import struct 

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
          self.sistema_archivo.seek(posicion+16)
          archivo.append(self.a_32.unpack(self.sistema_archivo.read(4))[0])
          self.sistema_archivo.seek(posicion+20)
          archivo.append(self.a_32.unpack(self.sistema_archivo.read(4))[0])
          archivos.append(archivo)
        else:
          archivos.append(nombre_archivo)

    return archivos
    

  def ls(self):
    lista_archivos = self.listar_archivos()

    for i in lista_archivos:
      print("-> ",i.decode())
      
  #cp origen destino
  #cp -l (del sistema al disckete) ar1 ar2
  #cp ar1 ar2 (del disckete al sist)



    '''
    listar()
      -> recorrer todo el directorio devilver un arreglo con los nombres

    ls()
      ->manda a llamar a listar()
      ->imprima el arreglo retornado

    existe_archivo(listado, nombre)
      ->recorre la lista comparando con el nombre ingresado


    copiar(nombre)
      llama a listar(nombre)
      si existe_archivo(lista,nombre)
        creamos archivo
        hacemos copiado
      ecc
        manda mensaje
      
    '''

    '''
    --copiar de fi al sistema 
    -> si encuentra el archivo
      -> sacar su info (tamaño y cluster inicial)
      -> crear archivo en la ruta especificada
      -> posicionar en el cluster inicial
      -> leer todo el archivo
      -> escribir todo el archivo en la ruta esp
      -> cerrar el archivo copiado
    ->ecc
      ->mensaje de error


    '''

    '''
    --tentativo para desfragmentar
    -> crear el bitmap para ver los espacios
    -> recorrer el bitmap
      -> en caso de encontrar un hueco 
        -> analizar tamaño del hueco 
        -> recorrer el siguiente bloque de informacion al espacio hueco
    '''


if __name__ == '__main__':
  sistema = Fiunamfs()
  sistema.ls()
