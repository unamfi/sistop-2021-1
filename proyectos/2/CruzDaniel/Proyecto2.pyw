from tkinter import *
from tkinter import messagebox
import threading
import random  
import time

#Funcion que creara la segunda ventana
def funcion():
	#Destruimos la ventana anterior
	root.destroy()
	
	#Creacion y configuracion de la segunda ventana
	raiz=Tk()
	raiz.title("La Ratatouille")
	raiz.resizable(0,0)
	raiz.geometry("1024x388")
	raiz.config(bg="black")
	
	raiz.iconbitmap("rata.ico")
	imagen1 = PhotoImage(file="Ratatouille.png")
	fondo = Label(raiz,image=imagen1).place(x=0,y=0)

	#Declaracion de variables para las entradas dadas por el usuario
	mesas_entrada=StringVar()
	clientes_entrada=StringVar()
	num_mesas=0
	n_clientes=0

	Label(raiz,text="Numero de Mesas: ",bg="cornflower blue", font=("Times New Roman",11,"bold"),fg="black").place(x=5,y=65)
	Label(raiz,text="Numero de Clientes",bg="cornflower blue", font=("Times New Roman",11,"bold"),fg="black").place(x=5,y=125)

	#Asignacion de los datos ingresados
	Entry(raiz,textvariable=mesas_entrada).place(x=140,y=65)
	Entry(raiz,textvariable=clientes_entrada).place(x=140,y=125)

	#Boton que hara que empiece el programa
	Button(raiz,text="Jugar",width=7,command=lambda:LaRatatouille()).place(x=100,y=155)

	#Creacion y configuracion del frame que fingira como consola
	consola=Frame()
	consola.config(relief="groove")
	consola.config(width="500", height="550")
	consola.pack(side="right",anchor="n")

	imprimir=Text(consola,bg="black",fg="white")
	imprimir.grid(row=0,column=0)

	scrollVert=Scrollbar(consola,command=imprimir.yview)
	scrollVert.grid(row=0,column=1,sticky="nsew")
	imprimir.config(yscrollcommand=scrollVert.set)

	#Funcion que contiene toda la implementacion
	def LaRatatouille():
		#Se intenta obtener los datos ingresados por el usuario
		try:
			#Se obtiene y se asigna el valor ingresado
			num_mesas=int(mesas_entrada.get())
			n_clientes=int(clientes_entrada.get())
			#Si los datos engraso son correctos se inicia el programa
			if(num_mesas>0 and n_clientes>0):
				imprimir.insert(INSERT,"\n--------------------------------------------------------------------------------\n")
				imprimir.insert(INSERT,"La Ratatouille en servicio\n")
				imprimir.insert(INSERT,"Numero mesas: {} \n".format(str(mesas_entrada.get())))
				imprimir.insert(INSERT,"Numero clientes: {} \n".format(str(clientes_entrada.get())))
				imprimir.insert(INSERT,"--------------------------------------------------------------------------------\n\n")

				'''Puse nombres acorde a la accion que hace cada actor para no 
				comentar mucho las funciones y saturar el codigo'''

				#Multiplex de mesas disponibles
				mesa_libre = threading.Semaphore(num_mesas)
				#Mutex del cliente para evitar concurrencia entre clientes
				mutex_cliente=threading.Semaphore(1)
				#Variable para el total de acompañantes
				total_acompañantes=0
				#Señalizacion para "despertar" a hostess
				despertar_hostess = threading.Semaphore(0)
				#Señalizacion para "despertar" a hostess2
				despertar_hostess2 = threading.Semaphore(0)
				#Señalizacion de que ya todos pensaron que van a comer
				ya_decidimos = threading.Semaphore(0)
				#Señalizacion que el mesero tome la orden
				tomar_orden =threading.Semaphore(0)
				#Señalizacion para avisar al chef que hay pedido
				pedido_chef=threading.Semaphore(0)
				#Señalizacion de que ya esta la orden lista
				orden_lista= threading.Semaphore(0)
				#Señalizacion para que el cliente empiece a comer
				poder_comer=threading.Semaphore(0)
				#Lista que guardara el total de acompañantes del cliente
				lista1=[]
				
				def hostess():
					while True:
						#Despertara cuando un cliente llegue
						despertar_hostess.acquire()
						imprimir.insert(INSERT,"Hola, bienvenido a La Ratatouille\n")
						#Si hay mesa disponible dara permiso de entrar si no dejara esperando al cliente
						mesa_libre.acquire()
						imprimir.insert(INSERT,"Si claro, adelante. Pase de este lado, mi compañera lo llevara a su mesa\n")
						despertar_hostess2.release()
				
				def hostess2():
					while True:
						#Una vez que haya mesa disponble se le llevara al cliente a esa misma mesa 
						despertar_hostess2.acquire()
						imprimir.insert(INSERT,"Bienvenidos, esta es su mesa y esta es la carta\n")

				def chef():
					while True:
						pedido_chef.acquire()
						#Pausa para "cocinar"
						time.sleep(1)
						orden_lista.release()
						

				def mesero():
					while True:
						tomar_orden.acquire()
						imprimir.insert(INSERT,"Si claro, les tomo su orden\n")
						pedido_chef.release()
						orden_lista.acquire()
						imprimir.insert(INSERT,"Aqui esta su orden\n")
						poder_comer.release()
						
				def cliente(id):
					#Evitamos concurrencia entre clientes
					mutex_cliente.acquire()
					#Asignamos total de acompañantes aleatorios
					total_acompañantes=random.randint(1,3)
					#Lo agreagams a lista que servira para crear la barrera clientes
					lista1.append(total_acompañantes)
					time.sleep(random.random())
					imprimir.insert(INSERT,"Hola, ¿tienes mesa disponible? Soy %d Y somos %d \n" %(id,1+total_acompañantes))
					#Creacion de los hilos acompañantes
					for i in range(total_acompañantes):
						threading.Thread(target=acompañantes, args=[i,id]).start()
					despertar_hostess.release()
					ya_decidimos.acquire()
					mutex_cliente.release()
					imprimir.insert(INSERT,"Mesero ¿nos puede tomar la orden?\n")
					tomar_orden.release()
					poder_comer.acquire()
					time.sleep(1)
					imprimir.insert(INSERT,"La comida esta deliciosa \n")
					imprimir.insert(INSERT,"Soy %d y nos vamos, dejamos la cuenta pagada en la mesa \n" %id)
					mesa_libre.release()

					time.sleep(2)
					if (id == n_clientes-1):
						messagebox.showinfo('ACABAMOS', 'Ya no hay mas clientes\n La Ratatouille cierra sus puertas, hasta luego ...')

				def acompañantes(i,id):	
					global barrera				
					#imprimir.insert(INSERT,"Soy %d y vengo con %d \n" %(i,id))
					#Un hilo en especifico creara el argumento de la barrera
					if (i == 0):
						lista=lista1.pop()
						#Barrera para asegurarnos que ya todos decidieron  que comer
						barrera= threading.Barrier(lista)
					else:
						#Teimpo en el que deciden
						time.sleep(random.random())
					barrera.wait()
					#Un hilo en especifico señalizara que ya se puede llamar al mesero
					if (i == 0):
						ya_decidimos.release()

				threading.Thread(target=mesero).start()
				threading.Thread(target=chef).start()
				threading.Thread(target=hostess).start()
				threading.Thread(target=hostess2).start()

				for cliente_id in range(n_clientes):
					threading.Thread(target=cliente, args=[cliente_id]).start()

			#Si los datos ingresados no son correctos se manda un mensaje
			else:
				messagebox.showinfo('ERROR', 'Clientes y mesas tienen que ser mayor a 1')

		#Si no se pueden obtener los datos o son incorrectos se manda un mensaje
		except ValueError:
			messagebox.showinfo('ERROR', 'Falta ingresar valores o valores erroneos')
	
	#Bucle para manter actia la segunda ventana
	raiz.mainloop()

#Creacion y configuracion de la primer ventana
root = Tk()
root.title("La Ratatouille")
root.resizable(False, False)
root.geometry("702x336")
root.config(bg="beige")

imagen = PhotoImage(file="fondo.png")
label = Label(image=imagen)
label.pack()
root.iconbitmap("rata.ico")

Label(root,text="Bienvenido",fg="black",font=("Times New Roman",22)).place(x=50,y=130)

#Boton que llamara a la segunda ventana
Button(root,text="Jugar",width=7,command=funcion,relief="raised").place(x=85,y=175)

#Bucle para manter actia la primer ventana
root.mainloop()