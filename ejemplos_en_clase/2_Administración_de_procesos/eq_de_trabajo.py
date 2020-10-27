#!/usr/bin/python3
from threading import Thread

def trabaja(n):
    j=0
    for i in range(1000000):
        j = j + 1
    print('%d termina' % n)

threads = []
for i in range(100):
    threads.append(Thread(target=trabaja, args=[i]))

print('Iniciando la ejecución paralela...')
for i in threads:
    i.start()

print('Todos los hilos están corriendo')

for i in threads:
    i.join()

print('Ya terminaron todos los hilos')
