import random

procesos=[]
imprimir=[]
procesosFIFO=[]

def generaProcesos(n):
	global total
	i=0
	total=0
	while(i < n):
		nombre=chr(random.randint(65,90))
		procesos.append(nombre)
		llegada=random.randrange(10)
		procesos.append(llegada)
		procesosFIFO.append(llegada)
		#Rango de duracion de cada proceso
		dura=random.randint(1,5)
		procesos.append(dura)
		#Variable que pensaba que podria utilizar 
		total=dura+total
		i += 1
		
def FIFO(n):
	while len(procesos) > 0:
		#Si se encuentra un 0 significa que un proceso quiere ejecutarse
		try:
			a=procesos.index(0)
			#Mientras alguien quiera ejecutarse se revisa cuantas unidades
			#de tiempo quiere hacerlo 
			while procesos[a+1] > 0:
				imprimir.append(procesos[a-1])
				procesos[a+1]=procesos[a+1]-1
			#Una vez que se haya acabado de ejecutar se saca de la lista de procesos 
			#la tupla [NombreProceso,TiempoLlegada,TiempoDuracion]
			procesos.pop(a)
			procesos.pop(a-1)
			procesos.pop(a+1)
		#Si no se encuentra un cero se reduce el TiempoLlegada de todos	
		except:
			imprimir.append("-")
			k = 1
			i=1
			while i<n:
				procesos[k] -= 1
				k+=3
				i+=1

print("¿Cuantos procesos quieres planificar?")
n = int(input())
generaProcesos(n)
print(procesos)
print(total)
FIFO(n)
#Para visualizar como seria
print(imprimir)