# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 00:11:10 2020

@author: Jonathan Calzada
"""

#Se utiliza threading para los hilos, random para los valores al azar; time para el tiempo
import threading
import random
import time

#Se crearon variables globales para reutilizar en las funciones
global paquete
global tiempoMin
global distrib
global val 

#Se inicializan las variables globales
conta = 0

tiempoMin = 0 #Es el tiempo que que ha transcurrido en minutos
paquete = 0 #Numero de paquetesas en la fila (contador)
distrib = 0
val = True

#Se asigna los hilos
mutex = threading.Semaphore(1)
camioneta = threading.Semaphore(0)
"""
Se simulara el centro de distribución de paquetes como FEDEX o DHL,
en donde solo se contará con tres camiones/camionetas que distruiran los paquetes
se plantea que son paqutes grandes por lo que solo caben 10 unidades por camioneta
"""

#Esta funcion se utilizará para cuando los paquetes esten cargados en los camiones/camionetas

def start():
    global paquete
    
    
    print("   \t")
    print("   \t")
    print("Viaje Numero: " )
    print("SE EMPIEZA A DISTRIBUIR PAQUETES ")
    time.sleep(0.25)
    print ("El encargado se encarga de la llegada segura de los paquetes")
    print(">> EL CAMINON REGRESA AL CENTRO DE DISTRIBUCION Y EMPIEZA A REPARTIR PAQUETES DE NUEVO")
    #val = True
    print("   \t")
    print("   \t")


    """
  En esta funcion esta la logistica para almacenar los paqutes en cada camioneta  
  donde se supone que son paqutes grandes y solo caben 10 paqutes por camion
    """
def paquetes():
   
    global paquete 
    global val
    mutex.acquire()
    print("Llega una paquete NUEVO")
    print("Paquete esperando Número: %d" %(paquete))
    if random.random() <=1: #Añadimos la llegada aleatorea de la llegada de los paqutes
        paquete += 1
        if paquete <=10:
            print("CAMION UNO   LLEVA el paquete No:", paquete)
            print("   \t")
        elif (paquete >=10 and paquete <=20):
            print("CAMION DOS LLEVA el paquete No:", paquete)
            print("   \t")
        elif (paquete >=20 and paquete <=30):
            print("CAMION TRES  LLEVA el  paquete No:", paquete)
            print("   \t")
        elif (paquete >=30 and paquete <=40):
            print("CAMION CUATRO  LLEVA el  paquete No:", paquete)
            print("   \t")
        #A partir del paquete N. 40 se tiene que espar a que regrese un camion repartidor
        elif paquete >= 40:
                print("A PARTIR DEL PAQ.NUM. 40  deben esperar a que se desocupe un camion")
                print("Cuando se desacupa un camion se empiza de cero el conteo de los paquetes")
    if (paquete == 60):
        val = False
        camioneta.release()
    time.sleep(0.45)
    val = True
           
    mutex.release()
#------------
    
 #Se crea la funcion para contar el tiempo transcurrido   
def contaMin():
    global tiempoMin
    global val
    mutex.acquire()
    tiempoMin += 1
    if tiempoMin == 25:
        camioneta.release()
    mutex.release()
    
   

"""
Esta funcion da inicio a que vuelva a arrancar el camion repartidor de paquetes
ya sea haya pasado cierto tiempo o paquetes

"""

def distrib():
    global tiempoMin
    global paquete
    global val
    val = True
    while val:
        camioneta.acquire()
        mutex.acquire()
        if tiempoMin == 50:
            start()
            tiempoMin -= 50
            #Vaciamos el contador de minutos
            paquete -= paquete
        elif paquete >= 50:
            start()
            paquete -= 50 #Vaciamos la fila
        mutex.release()
        
       
           

#que va a durar cada uno de nuestros hilos
threading.Thread(target = distrib, args = []).start()
while val:
    
	threading.Thread(target = paquetes, args = []).start()
	time.sleep(0.25)
	threading.Thread(target = contaMin, args = []).start()
	time.sleep(0.25)
    
    