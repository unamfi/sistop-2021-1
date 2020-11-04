import threading
import random  
import time

#Maximo de sillas que se desea tener en el cubiculo 
sillas= 5
#Maximo de dudas que se desea que tenga un alumno
maximo_dudas=3
#Lista que guardara a los alumnos
alumnos_con_dudas = []
#Lista que guardara el numero de dudas que tiene cada alumno
lista_dudas=[]

#Mutex que una vez adquirido despertara al asesor
despertar_profesor = threading.Semaphore(0)
##Mutex que si se adquiere entonces hay un lugar disponible
mutex_cubiculo = threading.Semaphore(sillas)
#Mutex para no confundir al asesor con varias duda simultaneamente
mutex_orden= threading.Semaphore(1)

def alumno(id):
	while True:
		dudas = (random.randint(1, maximo_dudas)) 
		time.sleep(random.random())
		print('Toc Toc ... Soy %d ¿Puedo pasar profe? ' %id) 
		mutex_cubiculo.acquire()
		#Una vez dentro del cubiculo se agrega al alumno, duda a las listas
		alumnos_con_dudas.insert(0,id)
		lista_dudas.insert(0,dudas)
		#Señal para despertar al asesor
		despertar_profesor.release()
		#Confirmacion de que pudo entrar al cubículo
		print('Si claro, adelante %d ' %id)
		print('Alumno %d entrando' %id)
		#Se presenta en orden la duda al asesor
		mutex_orden.acquire()
		print('Soy %d y tengo %d duda(s) ' %(id,dudas))
        


def profesor():
    while True:      
        print('zzzz ... Profesor durmiendo ')
        despertar_profesor.acquire()
        while len(alumnos_con_dudas)>0:
            time.sleep(0.05)
            #Se sacan de la lista al alumno asi como su pregunta
            alumno_id = alumnos_con_dudas.pop()
            #Variable que servira como acumulador para cuando se tiene mas de 1 duda
            aux = lista_dudas.pop()
            print('Profesor ayudando al alumno %d Con la pregunta %d' %(alumno_id,aux))
            aux = aux-1
            #Si una vez respondida la duda aún hay mas entonces se ingresa al alumno 
            #y a su duda a su respectiva lista de nuevo
            if aux>0:
            	alumnos_con_dudas.insert(0,alumno_id)
            	lista_dudas.insert(0,aux)
            	mutex_orden.release()
            #Sino hay mas dudas entonces el alumno se va y despierta a un alumno dormido
            else:
                print('Alumno se va ...')
                #El sigueinte alumno puede presentar su duda
                mutex_orden.release()
                mutex_cubiculo.release()

#Inicialización de hilos
threading.Thread(target=profesor).start()
for alumno_id in range(7):
    threading.Thread(target=alumno, args=[alumno_id]).start()


