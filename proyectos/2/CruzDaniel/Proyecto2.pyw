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

import threading
import random  
import time

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
#Barrera orden para acompañantes
barrera= threading.Barrier(total_acompañantes)
#Mutex para de que ya todos pensaron que van a comer
mutex2 = threading.Semaphore(0)
#Para que el mesero tome la orden
tomar_orden =threading.Semaphore(0)
#Mutex para avisar al chef que hay pedido
pedido_chef=threading.Semaphore(0)
#Mutex de que ya esta la orden lista
orden_lista= threading.Semaphore(0)
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
		for i in range(total_acompañantes):
			mutex_acompañantes.release()
		mutex.release()



def chef():
	while True:
		pedido_chef.acquire()
		time.sleep(1)
		orden_lista.release()


def mesero():
	while True:
		tomar_orden.acquire()
		print("Si claro")
		pedido_chef.release()
		orden_lista.acquire()
		print("Aqui esta su orden")
		mutex3.release()



def acompañantes(id):
	while True:
		mutex_acompañantes.acquire()
		time.sleep(random.random())
		barrera.wait()
		mutex2.release()



	

def cliente(id):
	mutex.acquire()
	total_acompañantes=random.randint(1,3)
	print("Hola, ¿tienes mesa disponible? Soy %d Y somos %d" %(id,1+total_acompañantes))
	despertar_hostess.release()
	for i in range(total_acompañantes):
		threading.Thread(target=acompañantes, args=[id]).start()
	mutex2.acquire()
	print("Mesero ¿nos puede tomar la orden?")
	tomar_orden.release()
	mutex3.acquire()
	time.sleep(1)
	mutex_mesas.acquire()




	
threading.Thread(target=mesero).start()
threading.Thread(target=chef).start()
threading.Thread(target=hostess).start()
threading.Thread(target=hostess2).start()

for cliente_id in range(7):
    threading.Thread(target=cliente, args=[cliente_id]).start()