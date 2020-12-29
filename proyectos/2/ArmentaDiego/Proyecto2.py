import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from string import ascii_uppercase

#Candados para proteger las variables compartidas
lock = threading.Lock()
lock2 = threading.Lock()

#Asientos disponibles para la sala de cine
asientos = [
        "A1","A2","A3","A4","A5",
        "B1","B2","B3","B4","B5",
        "C1","C2","C3","C4","C5",
        "D1","D2","D3","D4","D5",
        "E1","E2","E3","E4","E5", 
        ]

#Lista de asientos restantes a medida que se ocupan
asientos2 = asientos

#Lista de asientos ocupados
asientosOcupados = []

#Metodo para compra de las diferentes taquillas electrónicas que existen
def comprar():
    print(threading.get_ident(),"Comprando")
    time.sleep(2)
    lock.acquire()
    try:
        asiento = random.randint(0,len(asientos2)-1)
        asientosOcupados.append(asientos2[asiento])
        print(asientosOcupados)
        print("Asignando asiento: ",asientos2[asiento])
        asientos2.pop(asiento)
    finally:    
        lock.release()
#Metodo para devolucion de los boletos
def devolver():
    print(threading.get_ident(), "Devolviendo")
    time.sleep(2)
    lock.acquire()
    try:
        asientoD = random.randint(0,len(asientosOcupados)-1)
        asientos2.append(asientosOcupados[asientoD])
        print("Devolviendo asiento: ",asientosOcupados[asientoD])
        asientosOcupados.pop(asientoD)
    finally:    
        lock.release()


#mapa grafico de como se modifica la asignacion de asientos
def mapa():
    rows=[[],[],[],[],[]]
    print("mapa de asientos disponibles: \n")
    for i in range(5):
        for j in range(5):
            asientoB = ascii_uppercase[i]+str(j+1)
            if asientoB in asientosOcupados:
                rows[i].append("**")
            else:
                rows[i].append(asientoB)
    for i in range(5):
        print(rows[i])
    print("\n")


#Main, se mandan a llamar los hilos con un maximo de 6 por ronda, utilizando 5 rondas
def main():
    print("Estos son los asientos disponibles: ")
    print(asientos,"\n")
    mapa()
    for i in range(5):
        with ThreadPoolExecutor(max_workers = 6) as executor:
            task1 = executor.submit(comprar)
            task2 = executor.submit(comprar)
            task3 = executor.submit(comprar)
            task4 = executor.submit(comprar)
            task5 = executor.submit(devolver)
            task6 = executor.submit(devolver)
        mapa()


if __name__ == '__main__':
    main()

