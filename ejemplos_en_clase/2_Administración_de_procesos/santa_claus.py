#!/usr/bin/python3

import threading
import random
import time

def reno(id):
    while True:
        print('   R%d: Me voy de vacaciones' % id)
        time.sleep(random.random() * 5)
        print('   R%d: Volviendo.' % id)

        barrera_renos.wait()
        if id == 0:
            print('Despertando al jefe. Soy el reno %d' % id)
            despertar_a_santa.release()

        # ¿Listos para irnos de vacaciones?
        santa_a_reno[id].acquire()

def santa():
    while True:
        despertar_a_santa.acquire()
        mutex_elfos.acquire()
        elfos_espera = len(elfos_con_broncas)
        mutex_elfos.release()
        if elfos_espera >= 3:
            # Deberían ser sólo tres, pero cuando Santa sale de viaje,
            # a veces se acumulan las broncas...
            mutex_elfos.acquire()
            while len(elfos_con_broncas) > 0:
                elfo_id = elfos_con_broncas.pop()
                print('Santa ayudándole al elfo %d' % elfo_id)
            mutex_elfos.release()

        else:
            denle_elfos.acquire()
            print('¡Jo jo jo jo! ¡Es hora de viajar!')
            time.sleep(2)
            denle_elfos.release()
            for i in range(num_renos):
                santa_a_reno[i].release()


def elfo(id):
    while True:
        time.sleep(random.random())
        denle_elfos.acquire()
        denle_elfos.release()
        if random.random() < probabilidad_error:
            print('      E%d: problema :-(' % id)
            soy_el_primero = False
            # Tuve un problema construyendo mi juguete :-(
            mutex_elfos.acquire()
            elfos_con_broncas.append(id)
            print('      E%d: Hay %d elfos esperando' % (id, len(elfos_con_broncas)))
            if len(elfos_con_broncas) == 1:
                soy_el_primero = True
            mutex_elfos.release()

            barrera_elfos.wait()
            if soy_el_primero:
                print('      E%d: despierta a Santa' % id)
                despertar_a_santa.release()

num_renos = 9
num_elfos = 100
despertar_con_elfos = 3
probabilidad_error = 0.01
elfos_con_broncas = []

denle_elfos = threading.Semaphore(1)
mutex_elfos = threading.Semaphore(1)
barrera_renos = threading.Barrier(num_renos)
barrera_elfos = threading.Barrier(despertar_con_elfos)
despertar_a_santa = threading.Semaphore(0)
santa_a_reno = [threading.Semaphore(0) for i in range(num_renos)]


threading.Thread(target=santa).start()
for reno_id in range(num_renos):
    threading.Thread(target=reno, args=[reno_id]).start()
for elfo_id in range(num_elfos):
    threading.Thread(target=elfo, args=[elfo_id]).start()
