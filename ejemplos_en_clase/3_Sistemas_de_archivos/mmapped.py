from os import path
from mmap import mmap
from time import sleep
filename = '/tmp/mapeado'

fh = open(filename, 'w+')
# Llevamos el archivo a los 10K (10240 bytes)
fh.seek(10239)
fh.write('.')
fh.seek(0)

datos = mmap(fh.fileno(), 0)
datos[50:74] = b'Escribiendo directamente'
while True:
    print(datos[0:20])
    sleep(3)

