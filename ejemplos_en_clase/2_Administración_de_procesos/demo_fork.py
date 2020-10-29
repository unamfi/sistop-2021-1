#!/usr/bin/python3
import os
import time

print("¡Hola! Soy un procesito")
print("Mi PID es: ", os.getpid() )

pid = os.fork()

if pid == 0:
    # Proceso hijo
    print("El proceso hijo tiene por PID: ", os.getpid())
    time.sleep(3)
    print("El hijo termina")
    exit(0)
else:
    # Proceso padre
    print("El proceso padre tiene por PID: ", os.getpid(), " y su hijo es el ", pid)


# Observar: El proceso hijo existe aún, pero es zombie.
time.sleep(10)
