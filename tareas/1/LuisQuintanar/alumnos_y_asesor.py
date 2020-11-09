import threading
import random
import time

def alumnos(id):
	
	while True:
		time.sleep(random.random())

		if random.random() < probabilidad_de_llegada: 	# Llega un alumno y toca la puerta
			print("--Tocando la puerta")

			if len(alumnos_sentados) < numero_de_sillas: 	# Checa si hay asientos disponibles
		
				mutex_alumnos.acquire()
				print(" ++Tengo mi lugar")
				alumnos_sentados.append(id)
				mutex_alumnos.release()
				despertar_al_profesor.release()				# Se va a despertar al profesor porque ya hay al menos un alumno
		
			else:
				print("_________________________________Ya no hay lugar :c")

def profesor():
	
	while True:
	
		if len(alumnos_sentados) > 0:						# Se ha despertado al profesor y hay al menos un alumno
			despertar_al_profesor.acquire()
			tenga_dudas = True								# Nos ayudará para saber si el alumno preguntará algo nuevamente
	
			while len(alumnos_sentados) > 0:				# El profesor comienza a atender a los alumnos
				alumno_id = alumnos_sentados.pop()			
	
				while tenga_dudas:							# Si el alumno tiene más dudas, se le seguirá atendiendo
	
					if random.randint(0,1):					# Nos dice si el alumno seguirá teniendo preguntas
						tenga_dudas = False
					print('     Ayudandole al alumno ',+alumno_id)
					time.sleep(random.random())
	
				print("Resolvimos todas las dudas.........")
				break
	
		else:
			print("Durmiendo... zzzz")
			time.sleep(random.random())
		

numero_de_sillas = 5										# Número de asientos en el despacho del profesor
alumnos_sentados = []										# Lista de los id de los alumnos
probabilidad_de_llegada = 0.5								# Probabilidad de que un alumno toque la puerta

mutex_alumnos = threading.Semaphore(1)
despertar_al_profesor = threading.Semaphore(0)

threading.Thread(target = profesor).start()
for alumno_id in range(10):
	threading.Thread(target=alumnos,args=[alumno_id]).start()
