import threading
import random
import time 

def alumnos(id):
  profe_dormido.release()  
        

def profe():
    while True:
        if len(alumnos_en_silla) > 0:
            print('Resolviendo duda')
            time.sleep(random.random())
            alumno_id = alumnos_con_preguntas.pop()
            print('Duda resuelta del alumno %d' %alumno_id)
     
        else:
            profe_dormido.acquire()
            print('Profesor descansando')

num_alumno = 20
alumnos_con_preguntas = []
alumnos_en_silla = []
sillas = threading.Semaphore(2)
profe_dormido = threading.Semaphore(0)

threading.Thread(target=profe).start()
for alumno_id in range(num_alumno):
    threading.Thread(target=alumnos,args=[alumno_id]).start()
