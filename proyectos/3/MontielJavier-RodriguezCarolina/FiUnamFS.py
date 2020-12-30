import os
import struct
'''
from struct import *

class Fiunamfs:
  def __init__(self):
    self.tamanio_sector = 512
    self.tamanio_cluster = self.tamanio_sector * 2



nombre_sistema_archivo = 'fiunamfs.img'

sistema_archivo = open(nombre_sistema_archivo, 'r+b')
'''
a_32 = struct.Struct('<L')


sistema = open("fiunamfs.img","r+b")
sistema.seek(1024+15)
sector = sistema.read(1).decode("utf-8")
print(sector)

#print(a_32.unpack(sector))

sistema.close()