#!/usr/bin/python3
import os
import time

print("¡Hola! Soy un procesito")
print("Mi PID es: ", os.getpid() )

pid = os.fork()

if pid == 0:
    # Proceso hijo
    print("El proceso hijo original tiene por PID: ", os.getpid())
    repid = os.fork()
    if repid == 0:
        # Proceso hijo del hijo
        print("El proceso hijo del hijo es: ", os.getpid())
    else:
        # Proceso padre derivado del hijo
        print("El primer proceso derivado (",os.getpid(),") termina su ejecución")
        exit(0)
    time.sleep(3)
    print("El hijo termina")
    exit(0)
else:
    # Proceso padre
    print("El proceso padre tiene por PID: ", os.getpid(), " y su hijo es el ", pid)

# Observar: Como el proceso hijo terminó, el proceso hijo-del-hijo
# queda "huérfano" y es "adoptado" por el PID 1 - Y ya no queda como
# zombie
time.sleep(10)
