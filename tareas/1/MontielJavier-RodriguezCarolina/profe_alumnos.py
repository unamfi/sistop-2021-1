#!/usr/bin/python3

import threading
import random
import time 

def alumnos(id):
    num_preguntas = random.randint(1, 10)
    while num_preguntas > 0:
        sillas.acquire()
        print('---->El alumno %d consiguió silla' %id)
        alumnos_en_silla.append(id)
        mutex_primer_alumno.acquire()
        if len(alumnos_en_silla) == 1:
            profe_dormido.release()
        mutex_primer_alumno.release()
        num_preguntas= num_preguntas - 1
    print('-------->El alumno %d ya NO tiene dudas, ya se va' %id)
        

def profe():
    while True:
        if len(alumnos_en_silla) > 0:
            print('------>Resolviendo duda...')
            time.sleep(random.random())
            alumno_id = alumnos_en_silla.pop()
            print('->Duda resuelta del alumno %d' %alumno_id)
            sillas.release()
            print('El alumno %d dejo la silla' %alumno_id)
        else:
            print('->Profesor descansando')
            profe_dormido.acquire()
            print('->Profesor despierto')

num_alumno = 10
num_sillas = 2
alumnos_en_silla = []
sillas = threading.Semaphore(num_sillas)
profe_dormido = threading.Semaphore(0)
mutex_primer_alumno = threading.Semaphore(1)

threading.Thread(target=profe).start()

for alumno_id in range(num_alumno):
    threading.Thread(target=alumnos,args=[alumno_id]).start()
