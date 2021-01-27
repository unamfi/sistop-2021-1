import time
from random import randint, random, uniform
from threading import Semaphore, Thread

semaf = Semaphore(0) # Inicializamos semáforo en 1
mutex = Semaphore(0) # Inicializamos semáforo en 1

def semaforo(semaf, color): # 
    while True:
        if color == 0: # 0 es rojo
            print("semaforo en rojo")
            """pasar_rojo_a_verde():"""
            semaf.acquire() # Los carros están ocupando la calle esperando
            time.sleep(5) # Semáforo en rojo dura 5 segundos
            print("pasando a color verde")
            color = 1 # Pasamos de rojo a verde para que los carros puedan avanzar
            semaf.release() # Liberamos el semáforo para que los carros avancen

        if color == 1: # 2 es verde
            print("semaforo en verde")
            """pasar_verde_a_rojo():"""
            semaf.acquire() # Los carros están avanzando
            time.sleep(5) # Semáforo en verde dura 5 segundos
            print("pasando a color rojo")
            color = 0 # Pasamos a rojo para dejar pasar a los otros carros
            semaf.release()

def carro(semaf, mutex, color):
    while True:

            if color == 0: # Semaforo en ROJO
                print("semaforo verde para mí")
                mutex.acquire() # No entiendo bien para qué sirve este pero lo pongo porsiacaso, supongo que ocupa un tiempo extra aquí y evita caer en bloqueos mutuos
                time.sleep(5) # EL otro semáforo en siga dura 5 segundos jaja XD maldito gobierno delegacional
                print("carros avanzando del otro lado")
                cola_carros = cola_carros + int(random()*10) # Se acumula una cantidad aleatoria de carros en la cola de carros
                semaf.release() # Su semáforo se pondrá en ROJO:
                color = 1
                mutex.release()

            elif color == 2: # Semaforo en VERDE
                print("semaforo rojo para mí")
                mutex.acquire()
                semaf.acquire() # Los autos están esperando por su semáforo ponerse en verde
                time.sleep(5) # Semáforo en ROJO durante 5 segundos para los otros carros
                print("carros detenidos del otro lado")
                cola_carros = cola_carros - randint(0,cola_carros) # Avanza una cantidad aleatoria de carros, cantidad no superior a la cantidad de carros que ya hay
                color = 0
                mutex.release() 


color_inicial = randint(0,2) # color: verde = 1, o rojo = 0
color = color_inicial


# Ahora color pasa como argumento a las funciones que lo vayan a implementar       
Thread(target=semaforo, args=[semaf, color]).start()
Thread(target=carro, args=[semaf, mutex, color]).start()