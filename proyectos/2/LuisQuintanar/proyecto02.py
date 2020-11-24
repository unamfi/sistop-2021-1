import threading
import random
import time
import tkinter as tk
from tkinter import ttk

# Se implementa la interfaz de usuario
class MainWindow:
	#Cerramos la ventana de la interfaz
	def detener(self):
		#Hacemos que los hilos se detengan para después terminar el proceso
		self.mi_restaurante.set_stop(True)
		time.sleep(3)
		#Eliminamos la ventana de la interfaz
		self.root.destroy()

	#Inicamos la simulación
	def iniciar(self):
		#Bloqueo el boton para evitar que se cambien los parametros durante la ejecución
		self.boton.config(state="disable")
		self.mi_restaurante.inicialize(self.num_hilos.get(),self.num_asientos.get(),self.prob_llegada.get(),self.num_meseros)
		#Corremos los hilos
		self.mi_restaurante.run()
		self.updateWindow()
		
	#Actualizamos constantemente la información
	def updateWindow(self):			
		self.sentados.set(self.mi_restaurante.get_clientes_sentados())
		self.esperando.set(self.mi_restaurante.get_clientes_esperando())
		self.root.update_idletasks()
		self.root.after(2,self.updateWindow)
		return

	#Instanciamos los atributos de las UI
	def __init__(self):
		self.mi_restaurante = Restaurante()
		self.root = tk.Tk()	
		self.root.title("Simulación restaurante")
		self.root.configure(background='lightblue')
		self.root.geometry('500x500')
		self.root.resizable(width=False,height=False)

		ttk.Label(self.root,text="Numero de Hilos (Clientes):",font=("Times New Roman",10)).grid(column=0,row=5,padx=10,pady=25)
		self.num_hilos = tk.IntVar()
		self.num_hilos.set(10)
		self.entrada1= tk.Entry(self.root,width=25,bg="aquamarine",textvariable=self.num_hilos).grid(column=1,row=5)

		ttk.Label(self.root,text="Numero de Meseros:",font=("Times New Roman",10)).grid(column=0,row=6,padx=10,pady=25)
		self.num_meseros = tk.IntVar()
		self.num_meseros.set(5)
		self.entrada2= tk.Entry(self.root,width=25,bg="aquamarine",textvariable=self.num_meseros).grid(column=1,row=6)

		ttk.Label(self.root,text="Numero de asientos :",font=("Times New Roman",10)).grid(column=0,row=7,padx=10,pady=25)
		self.num_asientos = tk.IntVar()
		self.num_asientos.set(7)
		self.entrada3= tk.Entry(self.root,width=25,bg="aquamarine",textvariable=self.num_asientos).grid(column=1,row=7)

		ttk.Label(self.root,text="Probabilidad de llegada (%):",font=("Times New Roman",10)).grid(column=0,row=8,padx=10,pady=25)
		self.prob_llegada = tk.IntVar()
		self.prob_llegada.set(80)
		self.entrada4= tk.Entry(self.root,width=25,bg="aquamarine",textvariable=self.prob_llegada).grid(column=1,row=8)

		ttk.Label(self.root,text="Lista clientes sentados",font=("Times New Roman",10)).grid(column=0,row=10,padx=10 ,pady=25)
		self.sentados= tk.StringVar()
		self.sentados.set("")
		ttk.Label(self.root,textvariable=self.sentados,font=("Times New Roman",10)).grid(column=1,row=10,padx=10,pady=25)

		ttk.Label(self.root,text="Lista clientes esperando",font=("Times New Roman",10)).grid(column=0,row=11,padx=10,pady=25)
		self.esperando = tk.StringVar()
		self.esperando.set("")
		ttk.Label(self.root,textvariable=self.esperando,font=("Times New Roman",10)).grid(column=1,row=11,padx=10,pady=25)

		self.boton = tk.Button(self.root,command=self.iniciar,text="Comenzar",activeforeground='blue')
		self.boton.grid(column=1,row=9)

		self.botonDetener = tk.Button(self.root,command=self.detener,text="Detener",activeforeground='blue')
		self.botonDetener.grid(column=0,row=9)

		self.root.mainloop()

class Mesero:
	#Mostrara en la terminal las listas de los clientes
	def imprimeLista(self,msg,lista):
		print(msg,end="")
		for elemento in lista:
			print(elemento.get_id(),"-",end="")
		print()

	#El mesero dará un asiento al cliente
	def da_asiento(self,clientes_sentados,clientes_esperando,numero_asientos,cliente):
		clientes_esperando.append(cliente)
		self.imprimeLista("Clientes sentados:",clientes_sentados)
		self.imprimeLista("Clientes esperando: ",clientes_esperando)
		if len(clientes_sentados) + len(clientes_esperando) <= numero_asientos:
			clientes_sentados.extend(clientes_esperando)
			clientes_esperando[:] = []
		#El cliente no quiere esperar, no le gusta hacer fila
		elif not cliente.esperar():
			print("El cliente ",cliente.get_id(), " se marchó")
			clientes_esperando.remove(cliente)
			clientes_sentados.extend(clientes_esperando[:(len(clientes_sentados)-numero_asientos)])
		self.imprimeLista("Clientes sentados: ",clientes_sentados)
		self.imprimeLista("Clientes esperando: ",clientes_esperando)
	
	#El mesero tomará la orden del cliente
	def toma_orden(self,cliente):
		print("          Tomando orden del cliente",cliente.get_id())
		while random.randint(0,3):
			cliente.ordenar()
		print("EL CLIENTE ", cliente.get_id()," YA NO TIENE MÁS QUE ORDENAR")
		cliente.comer()

	def get_id(self):
		return self.id

	def __init__(self,id):
		self.id = id

class Cliente:
	#El cliente decide si quiere esperar según sus ganas
	def esperar(self):
		return random.random() < self.ganas_esperar
	#El mesero ya lo atendió, come y se marcha
	def comer(self):
		print("........ Cliente ",self.id," comiendo")
		time.sleep(random.random())
		print(".........EL cliente ",self.id," se marcha")
	#El cliente se toma su tiempo para decidir qué 	comers
	def ordenar(self):
		time.sleep(random.random())

	def get_id(self):
		return self.id

	def __init__(self,id):
		self.ganas_esperar = 0.2
		self.id  = id

class Restaurante(threading.Thread):

	def get_clientes_sentados(self):
		clientes_id = ""
		for cliente in self.clientes_sentados:
			clientes_id+=str(cliente.get_id())+" "
		return clientes_id

	def get_clientes_esperando(self):
		clientes_id = ""
		for cliente in self.clientes_esperando:
			clientes_id+=str(cliente.get_id())+" "
		return clientes_id
	#Cuando el usuario lo indique, se detendrán los hilos y se cerrará el programa
	def set_stop(self,stop):
		self.stop = stop
	#Define el comportamiento del cliente en el Restaurante
	def Clientes(self,id):
		while True:
			time.sleep(random.random())
			if random.random() < self.probabilidad_llegada:
				cliente = Cliente(id)
				print("Llego el cliente %",cliente.get_id())
				self.mutex_clientes.acquire()
				self.mesero.da_asiento(self.clientes_sentados, self.clientes_esperando,self.numero_asientos,cliente)
				self.mutex_clientes.release()
				self.alertar_mesero.release()
				if self.stop:
					self.mutex_clientes.acquire()
					self.alertar_mesero.acquire()
	#Define el comportamiento del mesero
	def Meseros(self,id):
		while True:
			self.mesero = Mesero(id)
			if len(self.clientes_sentados) > 0:
				print("Mesero",self.mesero.get_id(),"atendiendo a ",self.clientes_sentados[0].get_id())
				self.alertar_mesero.acquire()
				self.mutex_clientes.acquire()				
				self.mesero.toma_orden(self.clientes_sentados[0])
				self.clientes_sentados.pop(0)
				self.mutex_clientes.release()
	#Para crear darle valores al restaurante cuando el usuario lo indique
	def inicialize(self,num_threads,numero_asientos,probabilidad_llegada,num_meseros):
		self.numero_asientos = numero_asientos
		self.probabilidad_llegada = probabilidad_llegada/10
		self.num_threads = num_threads
		self.num_meseros = num_meseros

	def __init__(self):
		self.stop = False
		self.clientes_sentados = []
		self.clientes_esperando = []
		self.alertar_mesero = threading.Semaphore(0)
		self.mutex_clientes = threading.Semaphore(1)
	
	def run(self):
		for meseros_id in range(self.num_threads):
			threading.Thread(target=self.Meseros,args=[meseros_id]).start()
		for cliente_id in range(self.num_threads):
			threading.Thread(target=self.Clientes,args=[cliente_id]).start()

window = MainWindow()
