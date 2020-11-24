import threading
import random  
import time

mutex_cliente=threading.Semaphore()
total_acompañantes=0
#Mutex para preguntar disponibilidad
mutex = threading.Semaphore(1)
#Señalizacion para "despertar" a hostess
despertar_hostess = threading.Semaphore(0)
#Señalizacion para "despertar" a hostess2
despertar_hostess2 = threading.Semaphore(0)
#Señalizacion de mesa disponible
mutex_mesas = threading.Semaphore (3)
#Mutex acompañantes
mutex_acompañantes=threading.Semaphore(0)

#Mutex para de que ya todos pensaron que van a comer
mutex2 = threading.Semaphore(0)
#Para que el mesero tome la orden
tomar_orden =threading.Semaphore(0)
#Mutex para avisar al chef que hay pedido
pedido_chef=threading.Semaphore(0)
#Mutex de que ya esta la orden lista
orden_lista= threading.Semaphore(0)
mutex3=threading.Semaphore(0)
mutex5=threading.Semaphore(0)
lista1=[]


def hostess():
	while True:
		despertar_hostess.acquire()
		print("Hola, bienvenido a La Ratatouille")
		mutex_mesas.acquire()
		print("Si claro, adelante. Pase de este lado, mi compañera lo llevara a su mesa")
		despertar_hostess2.release()
		
def hostess2():
	while True:
		despertar_hostess2.acquire()
		print("Bienvenidos, esta es su mesa y esta es la carta")
		mutex5.release()
		mutex.release()
		

def chef():
	while True:
		pedido_chef.acquire()
		time.sleep(1)
		orden_lista.release()

def mesero():
	while True:
		tomar_orden.acquire()
		print("Si claro, les tomo su orden")
		pedido_chef.release()
		orden_lista.acquire()
		print("Aqui esta su orden")
		mutex3.release()

def cliente(id):
	mutex.acquire()
	mutex_cliente.acquire()
	total_acompañantes=random.randint(1,3)
	lista1.append(total_acompañantes)
	print("Hola, ¿tienes mesa disponible? Soy %d Y somos %d" %(id,1+total_acompañantes))
	for i in range(total_acompañantes):
		threading.Thread(target=acompañantes, args=[i,id]).start()
	despertar_hostess.release()
	mutex5.acquire()
	for x in range(total_acompañantes):
		mutex_acompañantes.release()
	mutex2.acquire()
	mutex_cliente.release()
	print("Mesero ¿nos puede tomar la orden?")
	tomar_orden.release()
	mutex3.acquire()
	time.sleep(1)
	print("Soy %d y nos vamos" %id)
	mutex_mesas.release()
	if (id == n-1):
		print("Ya no hay mas clientes")
		print("La Ratatouille cierra sus puertas ...")

def acompañantes(i,id):
	global barrera
	print("Soy %d y vengo con %d" %(i,id))
	if (i == 0):
		lista=lista1.pop()
		#Barrera orden para acompañantes
		barrera= threading.Barrier(lista)
		#mutex5.release()
	mutex_acompañantes.acquire()
	time.sleep(random.random())
	barrera.wait()
	mutex2.release()

threading.Thread(target=mesero).start()
threading.Thread(target=chef).start()
threading.Thread(target=hostess).start()
threading.Thread(target=hostess2).start()

print("¿Cuantos cientes (principales) entren a La Ratatouille?")
n=int(input())

for cliente_id in range(n):
    threading.Thread(target=cliente, args=[cliente_id]).start()

'''from tkinter import *

ventana=Tk()	#Se crea la ventana
ventana.title("La Ratatouille")	#Titulo
ventana.iconbitmap("rata.ico")	#Icono
#ventana.geometry("700x500")	#Tamaño de ventana
#ventana.config(bg="")	#Color del fondo
frame=Frame()	#Crear Frame
frame.pack(fill="both", expand="True")
#frame.pack(side="left",anchor="n")	#Posicion del frame
frame.config(bg="black")	#Color del fondo
frame.config(width="700",height="500")
frame.config(bd=20)
frame.config(relief="raised")	#groove
#frame.config(cursor="mouse")	#Cursor

ventana.mainloop()	#Bucle infinito '''