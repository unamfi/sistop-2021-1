from os import path
from mmap import mmap
from time import sleep
filename = '/tmp/mapeado'

fh = open(filename, 'r+')
misdatos = mmap(fh.fileno(), 0)
i = 0
while True:
    misdatos[0:10] = b'%10d' % i
    i = i + 1
    sleep(0.1)
