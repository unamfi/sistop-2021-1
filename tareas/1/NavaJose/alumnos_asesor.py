import threading
from time import sleep
import random

alumnos = 0
max_preguntas = 5 #con esta variable pensaba limitar el maximo de preguntas por alumno y emplear la funcion randint de random
turno = 0  #Con esta variable pensé en manejar los turnos
n=0

mutex = threading.Semaphore(1)
vacio = threading.Semaphore(1)


#Función que duerme y despierta al profesor
def profesor(n):
    if alumnos == 0:
        vacio.acquire()
        print ("No hay alumnos A DORMIR!!! zzz zzz zzz\n")
        sleep(1)
        vacio.release()
    else:
        print("El  %d alumno plantea su duda" % (n))
        asesoria(n)

#Funcion en la que "llegan" los alumnos
def alumno(n):
    global alumnos
    mutex.acquire()
    alumnos = alumnos +1
    mutex.release()
    if alumnos == 1:
        print("Tocan la puerta y el profesor despierta")
    print("El alumno %d entra y toma asiento" %alumnos)
    sleep(1)
    profesor(n)
    alumnos=0
    profesor(n)

#Funcion en la que se aclaran las dudas que plantean los alumnos en turno al profesor
def asesoria(num):
    print ("El profesor aclara la duda al alumno %d\n" % num)
    sleep(1)

#Se solicita el numero de sillas que tiene el salon (Claro que el profe tiene su escritorio :) )
sillas_alumnos = int(input("¿Cuántas sillas tenemos?\n"))
#El profesor llega al salon que en un inicio estara vacio
print("El profesor llega a cubrir su turno de asesorias")
profesor(n)

#Se crean los hilos correspondientes al numero de sillas y se generan los alumnos
for i in range(sillas_alumnos):
    threading.Thread(target = alumno, args = [i+1]).start()
    

