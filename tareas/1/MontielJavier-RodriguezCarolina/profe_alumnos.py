import threading
import random
import time 

def alumnos(id):
    #while True:
    print('Soy el alumno %d ' %id)

    sillas.acquire()
    print('   Se sento el alumno %d' %id)
    #profe.acquire()
    print('***El alumno %d deja la silla' %id)
    sillas.release()

num_alumno = 20
sillas = threading.Semaphore(2)
profe = threading.Semaphore(1)

for alumno_id in range(num_alumno):
    threading.Thread(target=alumnos,args=[alumno_id]).start()

#def preguntar()