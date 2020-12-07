#!/usr/bin/python
import sys
import os

read, write = os.pipe()

pid = os.fork()
if pid:
    # Proceso padre
    os.close(read)
    fh = os.fdopen(write, 'w')
    fh.write("Hola mijito!")
    sys.exit(0)
else:
    # Proceso hijo
    os.close(write)
    fh = os.fdopen(read)
    print('Dice papi que: ', fh.read())
    sys.exit(0)
