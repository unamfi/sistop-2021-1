import random  

#fifo
def FCFS(procs_lista):
	
	#_________Datos y listas________
	t = 0
	procesos_entrada = []
	procesos_queue = []
	
	procs_entrada_x = 0
	proc_queue_x = 0

	esquema = ""

	for proc in procs_lista:
    		procesos_entrada.append(proc.copy())
	#____________________


	#Si hay algun proceso aun o proceso de entrada o en la queue 
	while(len(procesos_queue) != 0 or procs_entrada_x < len(procesos_entrada)  ):

		#Si coincide el tiempo de llegada , se agrega a la queue
		if(procs_entrada_x < len(procesos_entrada) and procesos_entrada[procs_entrada_x][0] == t):
				procesos_queue.append(procesos_entrada[procs_entrada_x].copy())
				procs_entrada_x += 1

		#Si aun hay procesos en la queue
		if(len(procesos_queue) > 0):
    		
			#Se agrega nombre del proceso al esquema
			esquema = esquema + procesos_queue[0][2] 

			for proc in procesos_queue:
    			#aumenta  T
				proc[3]+=1

			#decrementa el tiempo necesario
			procesos_queue[0][1] -= 1

			#si t=0
			if(procesos_queue[0][1] == 0):
				procesos_entrada[proc_queue_x][3] = procesos_queue[0][3]
				procesos_entrada[proc_queue_x][6] = procesos_queue[0][6] 
				proc_queue_x += 1;
				procesos_queue.pop(0) 

		t = t+1

	Calculo_E_y_P(procesos_entrada)
	Imprime_Datos(procesos_entrada,"FCFS")
	print(esquema)


#round robin
def RR(procs_lista, n):
    
	#_________Datos y listas________
	t = 0

	procesos_entrada = []
	procesos_queue = []
	
	procs_entrada_x = 0

	esquema = ""

	#tamaño de quantum
	quantum = n 
	#encola
	queue = None

	for proc in procs_lista:
    		procesos_entrada.append(proc.copy())
	#_____________________

	#Si hay algun proceso aun o proceso de entrada o en la queue 
	while(queue != None or len(procesos_queue) != 0 or procs_entrada_x < len(procesos_entrada) ):

		#Si coincide el tiempo de llegada , se agrega a la queue
		if(procs_entrada_x < len(procesos_entrada) and procesos_entrada[procs_entrada_x][0] == t):
				procesos_queue.append(procesos_entrada[procs_entrada_x].copy())
				procs_entrada_x += 1

		#Encolar ultimo proceso
		if(queue != None ):
			procesos_queue.append(queue)
			queue = None

		#Si aun hay procesos en la queue
		if(len(procesos_queue) > 0):
    		#Se agrega nombre del proceso al esquema
			esquema = esquema + procesos_queue[0][2]

			for proc in procesos_queue:
    			#aumenta  T
				proc[3]+=1 

			#decrementa el tiempo necesario
			procesos_queue[0][1] -= 1
			#decrementa el tamaño del quantum
			quantum -= 1

			if(procesos_queue[0][1] == 0):
    			#Se guarda nombre del proceso
				nom_proc = procesos_queue[0][2]

				len_proc=len(procesos_entrada)
				k=0
				while k <len_proc:
    					
					if(procesos_entrada[k][2] == nom_proc):
    						
						procesos_entrada[k][3] = procesos_queue[0][3]
						procesos_entrada[k][6] = procesos_queue[0][6] 
						break
					k +=1

				procesos_queue.pop(0)
				quantum = n 

			#Si el tamaño del quantum es igual a 0
			elif(quantum == 0):
				queue = procesos_queue.pop(0)
				quantum = n

		t = t+1

	Calculo_E_y_P(procesos_entrada)
	Imprime_Datos(procesos_entrada,"RR"+str(n))
	print(esquema)

#spn
def SPN(procs_lista):
	
	#_________Datos y listas________
	t = 0

	procesos_entrada = []
	procesos_queue = []
	
	procs_entrada_x = 0

	esquema = ""
	flag = 0

	for proc in procs_lista:
    		procesos_entrada.append(proc.copy())
	#____________________

	#Si hay algun proceso aun o proceso de entrada o en la queue 
	while(len(procesos_queue) != 0 or procs_entrada_x < len(procesos_entrada) ):

		#Si coincide el tiempo de llegada , se agrega a la queue
		if(procs_entrada_x < len(procesos_entrada) and procesos_entrada[procs_entrada_x][0] == t):
    			
				p = flag
				for i in range(flag,len(procesos_queue)):
					if(procesos_entrada[procs_entrada_x][1] < procesos_queue[i][1]):
						p = i
						break
					p+=1
				procesos_queue.insert(p,procesos_entrada[procs_entrada_x].copy())
				procs_entrada_x += 1

		#Si aun hay procesos en queue
		if(len(procesos_queue) > 0):
    		#Se agrega nombre del proceso al esquema
			esquema = esquema + procesos_queue[0][2]

			for i in procesos_queue:
    			#aumenta T
				i[3]+=1 
			#decrementa el tiempo necesario
			procesos_queue[0][1] -= 1

			flag = 1

			#si t requerido =0
			if(procesos_queue[0][1] == 0):
				nom_proc = procesos_queue[0][2]
				for i in range(len(procesos_entrada)):
    				#si el nombre del proceso coincide
					if(procesos_entrada[i][2] == nom_proc):
    					#T iésimo = primer T
						procesos_entrada[i][3] = procesos_queue[0][3]
						#Nombre de proceso iésimo = nombre del primer proceso 
						procesos_entrada[i][6] = procesos_queue[0][6] 
						break
				procesos_queue.pop(0)
				flag = 0

		t = t+1

	Calculo_E_y_P(procesos_entrada)
	Imprime_Datos(procesos_entrada,"SPN")
	print(esquema)



#Calcula E y P de cada proceso en la lista con los procesos
def Calculo_E_y_P(procesos):
	for lista_proc in procesos:
		#E=T-t_requerido
		lista_proc[4] = lista_proc[3] - lista_proc[1]
		#P=T/t_requerido
		lista_proc[5] = lista_proc[3] / lista_proc[1]

#Calculo recursivos de los promedios T, E y P en procesos.
def Calculo_Promedio_T_E_P(procesos, Calculo_Promedio_T_E_P):
	for lista_proc in procesos:
    	#t=t+T
		Calculo_Promedio_T_E_P[0] += lista_proc[3]
		# t requerido= t requerido + E
		Calculo_Promedio_T_E_P[1] += lista_proc[4]
		Calculo_Promedio_T_E_P[2] += lista_proc[5]

	for i in range(len(Calculo_Promedio_T_E_P)):
		Calculo_Promedio_T_E_P[i] = Calculo_Promedio_T_E_P[i]/len(procesos)

#Imprime datos de los procesos
def Imprime_Datos(procesos,algoritmo):
	lista_promedios = [0,0,0]
	Calculo_Promedio_T_E_P(procesos,lista_promedios)
	print("\n"+algoritmo+":\tT="+str(lista_promedios[0])+",\t"+"E="+str(lista_promedios[1])+",\t"+"P="+str(round(lista_promedios[2],2)))

def Crea_Proceso(lista_procesos,n,p,t_min,t_max):
    
	t = 0

	nombres_procesos=['A','B','C','D','E','F','G','H']
	i=0
	while(n > 0):
    	#Se crea proceso con probabilidad de 0.2=1/5
		if(random.randint(0,p) == 1):
            #lista con tiempo en el que llego el proceso, tiempo entre t_min y t_max, nombre del proceso, valor T, valor E, valor P y esquema de proceso
			proceso = [t,random.randint(t_min,t_max), nombres_procesos[i],0,0,0,""]
            #se agrega el proceso creado a la lista de procesos
			lista_procesos.append(proceso)
			#Se aumenta contador para letra del nombre de proceso
			i += 1
			n -= 1
		t += 1

procesos_lista = []
Crea_Proceso(procesos_lista,8,4,5,15)

FCFS(procesos_lista)
RR(procesos_lista,1)
RR(procesos_lista,4)
SPN(procesos_lista)
