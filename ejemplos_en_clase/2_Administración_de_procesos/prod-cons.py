#!/usr/bin/python3

def consumidor(id):
    while True:
        elementos.acquire()
        mutex.acquire()
        event = buffer.pop()
        if len(buffer) == maxlen:
            print("OJO! estamos a punto...")
        elif len(buffer) > maxlen:
            print("¡OJO! ¡NOS PASAMOS! ¡CATÁSTROFE!")
        mutex.release()
        buff_lleno.release()
        print('* C%d ← E (B:%d)' % (id,len(buffer)))
        event.process()

def productor(id):
    while True:
        event = Evento()
        mutex.acquire()
        buffer.append(event)
        mutex.release()
        buff_lleno.acquire()
        print('* P%d → E (B:%d)' % (id, len(buffer)))
        elementos.release()

import time
import random
import threading
mutex = threading.Semaphore(1)
elementos = threading.Semaphore(0)
buffer = []
maxlen = 10
# Inicializo a maxlen-1, porque el 0 también cuenta - ¡Si
# inicializo a maxlen, me paso del tamaño desado!
buff_lleno = threading.Semaphore(maxlen - 1)

class Evento:
    def __init__(self):
        print("Generando evento")
        time.sleep(random.random())
    def process(self):
        print("Procesando evento")
        time.sleep(random.random())

threading.Thread(target=productor, args=[1]).start()
threading.Thread(target=productor, args=[1]).start()
threading.Thread(target=consumidor, args=[1]).start()

