'''
En el siguiente ejemplo visto en clase, 
se utilizan los semáforos como una herramienta 
de comunicación entre hilos.
Los palillos se pueden representar como 
un arreglo de semáforos asegurando la exclusión mutua, 
esto quiere decir que, un solo filósofo puede 
sostener un palillo al mismo tiempo.
Se presentó la siguiente solución para evitar 
el bloqueo mutuo pero esta no asegura que no exista inanición
En este caso uno de los filósofos es zurdo, por lo que
evita los bloqueos mutuos.
'''
import threading
import time
num = 5
palillos = [threading.Semaphore(1) for i in range(num)]
comidas = 0
mut_comidas =threading.Semaphore(1)

def filosofo(id):
    while True:
        piensa(id)
        levanta_palillos(id)
        come(id)
        suelta_palillos(id)

def piensa(id):
    print( "%d - Tengo hambre.." % id)

def levanta_palillos(id):
    if id == 0: #Zurdo
        palillos[id].acquire()
        print("%d - Tengo el palillo izquierdo" % id)
        palillos[ (id + 1) % num].acquire()
    else: #Diestro 
        palillos[(id + 1) % num].acquire()
        print("%d - Tengo el palillo derecho" % id)
        palillos[id].acquire()
    print("%d - Tengo ambos palillos" % id)

def suelta_palillos(id):
    palillos[(id +1) % num].release()
    palillos[id].release()
    print("%d - Sigamos pensando..." % id)


def come(id):
    print("%d - !A comer!" % id)

filosofos = [threading.Thread(target=filosofo, args=[i]).start() for i in range(num)]