from tkinter import *
from tkinter import messagebox
import threading
import random  
import time

def funcion():
	root.destroy()
	raiz=Tk()
	raiz.title("La Ratatouille")
	raiz.resizable(0,0)
	raiz.geometry("1024x388")
	raiz.config(bg="black")

	imagen1 = PhotoImage(file="Ratatouille.png")
	fondo = Label(raiz,image=imagen1).place(x=0,y=0)

	mesasSTR=StringVar()
	clientesSTR=StringVar()
	num_mesas=0
	n=0

	consola=Frame()
	consola.config(relief="groove")
	consola.config(width="500", height="550")
	consola.pack(side="right",anchor="n")
	imagen= PhotoImage(file="1.gif")

	Label(raiz,text="Numero de Mesas: ",bg="cornflower blue", font=("Times New Roman",11,"bold"),fg="black").place(x=5,y=65)
	Label(raiz,text="Numero de Clientes",bg="cornflower blue", font=("Times New Roman",11,"bold"),fg="black").place(x=5,y=125)

	Entry(raiz,textvariable=mesasSTR).place(x=140,y=65)
	Entry(raiz,textvariable=clientesSTR).place(x=140,y=125)

	Button(raiz,text="Jugar",width=7,command=lambda:LaRatatouille()).place(x=100,y=155)

	imprimir=Text(consola,bg="black",fg="white")
	imprimir.grid(row=0,column=0)

	scrollVert=Scrollbar(consola,command=imprimir.yview)
	scrollVert.grid(row=0,column=1,sticky="nsew")
	imprimir.config(yscrollcommand=scrollVert.set)

	def LaRatatouille():	
		try:
			num_mesas=int(mesasSTR.get())
			n=int(clientesSTR.get())
			if(num_mesas>0 and n>0):
				imprimir.insert(INSERT,"\n--------------------------------------------------------------------------------\n")
				imprimir.insert(INSERT,"La Ratatouille en servicio\n")
				imprimir.insert(INSERT,"Numero mesas: {} \n".format(str(mesasSTR.get())))
				imprimir.insert(INSERT,"Numero clientes: {} \n".format(str(clientesSTR.get())))
				imprimir.insert(INSERT,"--------------------------------------------------------------------------------\n\n")

				#Señalizacion de mesa disponible
				mutex_mesas = threading.Semaphore(num_mesas)
				mutex_cliente=threading.Semaphore()
				total_acompañantes=0
				#Mutex para preguntar disponibilidad
				mutex = threading.Semaphore(1)
				#Señalizacion para "despertar" a hostess
				despertar_hostess = threading.Semaphore(0)
				#Señalizacion para "despertar" a hostess2
				despertar_hostess2 = threading.Semaphore(0)
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
						imprimir.insert(INSERT,"Hola, bienvenido a La Ratatouille\n")
						mutex_mesas.acquire()
						imprimir.insert(INSERT,"Si claro, adelante. Pase de este lado, mi compañera lo llevara a su mesa\n")
						despertar_hostess2.release()
				
				def hostess2():
					while True:
						despertar_hostess2.acquire()
						imprimir.insert(INSERT,"Bienvenidos, esta es su mesa y esta es la carta\n")
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
						imprimir.insert(INSERT,"Si claro, les tomo su orden\n")
						pedido_chef.release()
						orden_lista.acquire()
						imprimir.insert(INSERT,"Aqui esta su orden\n")
						mutex3.release()
						
				def cliente(id):
					mutex.acquire()
					mutex_cliente.acquire()
					total_acompañantes=random.randint(1,3)
					lista1.append(total_acompañantes)
					imprimir.insert(INSERT,"Hola, ¿tienes mesa disponible? Soy %d Y somos %d \n" %(id,1+total_acompañantes))
					for i in range(total_acompañantes):
						threading.Thread(target=acompañantes, args=[i,id]).start()
					despertar_hostess.release()
					mutex5.acquire()
					for x in range(total_acompañantes):
						mutex_acompañantes.release()
					mutex2.acquire()
					mutex_cliente.release()
					imprimir.insert(INSERT,"Mesero ¿nos puede tomar la orden?\n")
					tomar_orden.release()
					mutex3.acquire()
					time.sleep(1)
					imprimir.insert(INSERT,"Soy %d y nos vamos, dejamos la cuenta pagada en la mesa \n" %id)
					mutex_mesas.release()
					if (id == n-1):
						messagebox.showinfo('ACABAMOS', 'Ya no hay mas clientes\n La Ratatouille cierra sus puertas, hasta luego ...')

				def acompañantes(i,id):
					global barrera
					imprimir.insert(INSERT,"Soy %d y vengo con %d \n" %(i,id))
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

				for cliente_id in range(n):
					threading.Thread(target=cliente, args=[cliente_id]).start()
			else:
				messagebox.showinfo('ERROR', 'Clientes y mesas tienen que ser mayor a 1')
		except ValueError:
			messagebox.showinfo('ERROR', 'Falta ingresar valores o valores erroneos')
	
	raiz.mainloop()

root = Tk()
root.title("La Ratatouille")
root.resizable(False, False)
root.geometry("702x336")
root.config(bg="beige")
imagen = PhotoImage(file="fondo.png")
label = Label(image=imagen)
label.pack()
Label(root,text="Bienvenido",fg="black",font=("Times New Roman",22)).place(x=50,y=130)
Button(root,text="Jugar",width=7,command=funcion,relief="raised").place(x=85,y=175)

root.mainloop()