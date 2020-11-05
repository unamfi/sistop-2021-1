
import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-s) %(message)s')

class Car(threading.Thread):
    def __init__(self, nombreHilo, carID, carDir, semaforo):
        threading.Thread.__init__(self, name=nombreHilo, target=Car.run)
        self.nombreHilo = nombreHilo
        self.carID = carID
        self.carDir = carDir
        self.semaforo = semaforo
    
    def run(self):
        self.avanza(self.carID, self.carDir, self.semaforo)
    
    def avanza(self, carID, carDir, semaforo):
        """Metodo cuando se ejecute un hilo (se llama cuando se sobreescribe el metodo run() de un threading.Thread)"""
        semaforo.acquire()
        logging.info("El carro " + str(carID) + " tiene direccion: " + str(carDir))
        time.sleep(random.randint(1,5))
        logging.info("Avanza y sale carro " + str(carID) + " con direccion: " + str(carDir))
        semaforo.release()
        return

def creaHilosCarros(direccion, id_inicial, id_final):
    """Funcion que regresa una lista de hilos por cada direccion y de cantidad id_final-id_inicial"""
    return [ Car(f"Hilo {i}", i, direccion, semaforo) for i in range(id_inicial, id_final) ]

if __name__ == '__main__':
    semaforo = threading.Semaphore(5)  # 5 indica que el semaforo puede ser accedido por 5 hilos al mismo tiempo y los hilos restantes tienen que esperar hasta que se libere el semaforo
    direcciones = ["Izquierda a derecha", "Derecha a izquierda", "Arriba a abajo", "Abajo a arriba"]
    carros_dir = {}  # diccionario de carros donde la clave es la direccion y el valor es la cantidad de carros que
                     # que hay en esa posicion inicial
    carros = []  # lista de carros (hilos)
    id_inicial = 1  # id inicial de los carros
    
    for dir in direcciones:  # se agregaran carros en las 4 direcciones posibles
        cantidad = random.randint(1,4)
        carros_dir[dir] = cantidad
        id_final = id_inicial + cantidad  # el id final de cada direccion va aumentando por cada una de las claves en el dicc
        carros += creaHilosCarros(dir, id_inicial, id_final)  # se agregan los carros a los hilos que se ejecutaran después
        id_inicial = id_final

    print("Los carros en cada posición son: ")
    for direccion in carros_dir:
        print(f"{direccion} : {carros_dir[direccion]}")
    
    # inicia ejecucion de los hilos
    for car in carros:
        car.start()

        