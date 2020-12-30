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

  def ls(self):
    
    for i in range(0,64):
      self.sistema_archivo.seek(self.tamanio_cluster+(i*64))
      nombre_archivo = self.sistema_archivo.read(14)

      if nombre_archivo != b'Xx.xXx.xXx.xXx':
        print("[",i+1,"]"," ",nombre_archivo.decode())


if __name__ == '__main__':
  sistema = Fiunamfs()
  sistema.ls()
