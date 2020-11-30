from threading import Semaphore, Thread
from time import sleep 
from random import randint

#Constantes para controlar el numero de clientes que pueden estar en la tienda y el máximo de pedidos que puede hacer
maxClient = 3 
maxPed =  5 

#Variable para controlar el cerrado de la tiendita 
n = 0

#Mecanismos a implementar en la solucíon 
tiendita = Semaphore(maxClient) #Multiplex control de clientes en tiendita por COVID-19
pedidos = Semaphore(0) #Mutex de pedido realizado
despacho = Semaphore(1) #Mutex de proceso de despacho
turnos = Semaphore(1) #Mutex que maneja los turnos de pedido

#Lista donde manejamos que cliente hace pedido y que numero de pedido es
turno = []

#Funcion que maneja al hilo de la tendera	
def tendera():
    global n
    while(True):
        #La tendera espera a que se le realice un pedido
        pedidos.acquire() 
        #Se despacha el pedido en turno 
        turnos.acquire()   
        #Vaciamos la lista de los pedidos en turno
        numCliente = turno.pop(0)
        articulo = turno.pop(0)
        print('     La tendera despacha el pedido %d del cliente %d' % (articulo,numCliente))
        #Esperamos el siguiente pedido
        turnos.release()
        despacho.release()
        #Mediante esta condicional rompemos el bucle para poder cerrar la tienda
        if(n == clientes-1):
            break  

#Funcion que maneja los hilos de los clientes
def cliente(numCliente):
    global n
    #Generamos aleatoriamente el numero de artículos que el cliente va a comprar
    articulos = randint(1,maxPed)  
    #Utilizaremos un contador para que los clientes puedan realizar pedidos hasta que ya tengan todos sus artículos a comprar
    articulo = 1 
    #Ponemos a operar nuestro Multiplex para tener el control de cuantas personas estan dentro de la tiendita
    tiendita.acquire()
    print('El cliente %d ha entrado a la tiendita y va a comprar %d cosas' % (numCliente, articulos))
    #Mientras el cleinte tenga articulos por comprar realizará pedidos
    while(articulo <= articulos): 
        #Se inicia el proceso de despacho del pedido en turno
        despacho.acquire() 
        #El cliente realiza su pedido en turno
        turnos.acquire()
        print('     El cliente %d hace su pedido numero %d' % (numCliente, articulo))
        #Almacenamos el pedido en turno y el cliente al que pertenece
        turno.append(numCliente)
        turno.append(articulo)
        turnos.release()
        #La tendera toma el pedido
        pedidos.release() 
        #Se reduce el numero de artículos a comprar
        articulo += 1
        sleep(0.3)
    #Si el cliente ya no tiene más artículos por comprar se retira de la tiendita
    print('         El cliente %d sale de la tiendita' % (numCliente))
    print('         Tendera: "Hasta luego vuelva pronto!!!"')
    #Sale de la tiendita y se libera un espacio
    tiendita.release() 
    #Se aumenta el numero de clientes despachados en el día 
    n = n+1
    #Si la tendera ha despachado a todos los clientes del dia se cierra la tiendita
    if(n == clientes):
        print('')
        print('')
        print('8 de la noche se cierra la tienda')
        print('')
        print('')
        print('                    ---------')
        print('                    -CERRADO-')
        print('                    ---------')
  
#Numero de clientes que irán a la tienda
clientes = int(input('¿Cuántos clientes se atenderan hoy?\n'))

#Se inicia el hilo de la tendera y se abre la tienda
Thread(target = tendera).start()
print('')
print('')
print('9 de la mañana se abre la tienda')
print('')
print('')
print('                    ---------')
print('                    -ABIERTO-')
print('                    ---------')
print('')
print('')
#Se inicia el numero de hilos de acuerdo al numero de clientes que van a ir a la tienda
for i in range(1,clientes+1):
    Thread(target = cliente, args = [i]).start()
