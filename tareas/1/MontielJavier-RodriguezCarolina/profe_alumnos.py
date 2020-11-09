#!/usr/bin/python3

'''
############################################################################
->Autores:
    -Montiel Martinez Luis Javier
    -Rodríguez Dávalos Carolina
->Fecha de creación: 01/11/2020
->Descripción: Análisis y resolución del problema 'Los alumnos y el asesor'
############################################################################
'''

import threading
import random
import time 

def alumnos(id):
    #Indica el número de preguntas que hará el alumno, puede ser de 1 a 10 preguntas
    num_preguntas = random.randint(1, 10)
    while num_preguntas > 0:
        #El alumno intenta conseguir una silla 
        sillas.acquire()
        print('---->El alumno %d consiguió silla' %id)
        #El arreglo se usa para saber que alumnos ocupan sillas
        alumnos_en_silla.append(id)
        mutex_primer_alumno.acquire()
        #En caso de ser el primer alumno en conseguir silla, despierta al profe
        if len(alumnos_en_silla) == 1:
            profe_dormido.release()
        mutex_primer_alumno.release()
        #Reduce el número de preguntas restantes del alumno
        num_preguntas= num_preguntas - 1
    print('-------->El alumno %d ya NO tiene dudas, ya se va' %id)
        

def profe():
    while True:
        #En caso de que haya alumnos ocupando sillas, resuelve duda 
        if len(alumnos_en_silla) > 0:
            print('------>Resolviendo duda...')
            time.sleep(random.random())
            alumno_id = alumnos_en_silla.pop()
            print('->Duda resuelta del alumno %d' %alumno_id)
            sillas.release()
            print('El alumno %d dejo la silla' %alumno_id)
        #En caso contrario, se va a dormir
        else:
            print('->Profesor descansando')
            profe_dormido.acquire()
            print('->Profesor despierto')

#Máximo de alumnos
num_alumno = 10
#Máximo de sillas en el cubículo
num_sillas = 2
#Lista de alumnos sentados
alumnos_en_silla = []
#Creando semáforos
sillas = threading.Semaphore(num_sillas)
profe_dormido = threading.Semaphore(0)
mutex_primer_alumno = threading.Semaphore(1)

#Creando hilos
threading.Thread(target=profe).start()

for alumno_id in range(num_alumno):
    threading.Thread(target=alumnos,args=[alumno_id]).start()
