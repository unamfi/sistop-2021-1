# -*- coding: utf-8 -*-
import threading
import time
num = 5
palillos = [threading.Semaphore(1) for i in range(num)]
comidas = 0
mut_comidas = threading.Semaphore(1)
multiplex = threading.Semaphore(num-1) # Empleado únicamente en la solución 2

def filosofo(id):
    while True:
        piensa(id)
        levanta_palillos(id)
        come(id)
        suelta_palillos(id)

def piensa(id):
    # time.sleep(0.5)
    print( "%d - Tengo hambre..." % id)

# Función inicial: Lleva a un bloqueo mutuo.
def levanta_palillos(id):
    palillos[id].acquire()
    print( "%d - Tengo el primer palillo" % id)
    palillos[(id+1) % num].acquire()
    print( "%d - Tengo ambos palillos" % id)

# # Solución 1
# #
# # Des-comentar la siguiente función (y comentar la versión inicial)
# # para la solución 1: Hacer que los filósofos pares sean "zurdos" --
# # Que levanten el palillo izquierdo antes del derecho
# #
# # (no requiere modificar suelta_palillos() )
# def levanta_palillos(id):
#     if (id % 2 == 0): # Zurdo
#         palillo1 = palillos[id]
#         palillo2 = palillos[(id+1) % num]
#     else: # Diestro
#         palillo1 = palillos[(id+1) % num]
#         palillo2 = palillos[id]
#     palillo1.acquire()
#     print( "%d - Tengo el primer palillo" % id)
#     palillo2.acquire()
#     print( "%d - Tengo ambos palillos" % id)

# # Solución 2
# #
# # Des-comentar la siguiente función, así como la línea indicada
# # "solución 2" en suelta_palillos(). Evita los bloqueos mutuos empleando
# # un multiplex, para evitar que todos los filósofos levanten su primer
# # palillo al mismo tiempo.
# def levanta_palillos(id):
#     multiplex.acquire()
#     palillos[id].acquire()
#     print( "%d - Tengo el primer palillo" % id)
#     palillos[(id+1) % num].acquire()
#     print( "%d - Tengo ambos palillos" % id)

def suelta_palillos(id):
    palillos[(id + 1) % num].release()
    palillos[id].release()
    # multiplex.release() # Únicamente para la solución #2
    print( "%d - Sigamos pensando..." % id)

def come(id):
    global comidas
    mut_comidas.acquire()
    comidas = comidas + 1
    print( "%d - ¡A comer! (Comida #%d)" % (id, comidas))
    mut_comidas.release()
    # time.sleep(0.3)

filosofos = []
for i in range(num):
    fil = threading.Thread(target=filosofo, args=[i])
    filosofos.append(fil)
    fil.start()
