#Para generar numeros aleatorios que se ocuparan en los procesos
from random import randint
#Se importa la libreria copy para reusar la lista de procesos
import copy

#Enlistado de procesos y asignacion a numero de cargas
nProcesos=['A','B','C','D','E','F','G','H']
nCargas=4

#Funcion para imprimir la lista
def imprimirList(listaP):
    for i in listaP:
        print(i)

#Funcion para implementar procesos enlistados
def impCarga(listaP):
    listaP.append([0,3,'A'])
    listaP.append([1,5,'B'])
    listaP.append([3,2,'C'])
    listaP.append([9,5,'D'])
    listaP.append([12,5,'E'])    
#Funcion para el manejo de cargas para cada proceso
def carga(letra):
    return [randint(0,6),randint(4,8),letra]

#Implementación del algoritmo que es el Fifo (First In, First Out)

def Algoritmo_fifo(listaP):
    c=copy.deepcopy(listaP)
    Respuesta=0.0
    Espera=0.0
    Penal=1
    
    c[0].append(c[0][0])
    Respuesta=c[0][1]
    
    for i in range (1,nCargas):
        te=(c[i-1][3]+c[i-1][1])-c[i][0]
        c[i].append(te+c[i][0])
        Espera=te+Espera
        Respuesta=Respuesta+te+c[i][1]
        
        Penal=Penal+(te+c[i][1])/c[i][1]
    Espera=Espera/nCargas
    Respuesta=Respuesta/nCargas
    Penal=Penal/nCargas
    print("First In, First Out (FIFO): ")
    
    for i in range (0,nCargas):
        for j in range(0,c[i][1]):
            print(c[i][2],end='')
    print()
    print("\nTiempo de respuesta=%f \nTiempo de espera =%f \nTiempo de penalización=%f"%(Respuesta,Espera,Penal)) #imprime los valores FIFO
    print("----------------------")
    
#Implementación del algoritmo rr (Round-robin)
def Algoritmo_rr(listaP,q):
    c=[]
    c=copy.deepcopy(listaP)
    print("Round-robin (RR)%d: "%q)
    queue=[]
    t=c[0][0]
    n=0
    for i in c:
        if i[0]==t:
            c[n].append(0)
            queue.append(i)
        n=n+1
    r=[]
    
    comienzo=False
    while True:
        for i in range (0,nCargas):
            if comienzo==True:
                break
            if(c[i][0]<=t+q and c[i].__len__()<4):
                c[i].append(0)
                queue.append(c[i])
                
                if (i==nCargas-1):
                    comienzo=True
        quantum=0 #Para que el proceso entre cuando debe   
        n=0

        for i in queue:
           if n==0:
               i[1]=i[1]-q
               if i[1]>0:
                   
                   for j in range(0,q):
                       print(i[2],end='')
                       quantum=quantum+1
                   
               elif i[1]<=0:
                   for j in range(0,q+i[1]):
                       print(i[2],end='')
                       quantum=quantum+1
                   i[1]=0
                   r.append(i)
               n=1
           else:
               queue.remove(i)
               i[3]=i[3]+t+quantum-i[0]
               
               
               i[0]=i[0]+t+quantum-i[0]
               
               queue.insert(n,i)
               n=n+1
        
        aux=queue[0]
        queue.remove(aux)
        aux[0]=aux[0]+quantum
        queue.append(aux)
        
        for i in queue:
            if i[1]==0:
                queue.remove(i)
        
        if comienzo==True and queue.__len__()==0:
            print()
            break
        
        t=t+quantum
    Penal=0.0
    Espera=0.0
    Respuesta=0.0
    for i in range (0,nCargas):
        for j in range(0,nCargas):
            if c[i][2]==r[j][2]:
                Respuesta=Respuesta+listaP[i][1]+r[j][3]
                Espera=Espera+r[j][3]
                Penal=Penal+(listaP[i][1]+r[j][3])/listaP[i][1]
    Espera=Espera/nCargas
    Respuesta=Respuesta/nCargas
    Penal=Penal/nCargas
    
    print("\nTiempo de respuesta=%f \nTiempo de espera =%f \nTiempo de penalización=%f"%(Respuesta,Espera,Penal))#imprime los valores RR
    print("----------------------")

#Implementación del algoritmo SPN (Shortest Process Next)   

def Algoritmo_spn(listaP):
    print("Shortest Process Next (SPN): ")
    c=copy.deepcopy(listaP)
    for x in c:
        x.append(0)
        x.append(False)
    queue=[]
    t=c[0][0]
    comienzo=False
    while True:    
        for i in range(0,nCargas):
            if c[i][0]<=t and c[i][4]==False:
                c[i][4]=True
                c[i][3]=t-c[i][0]
                queue.append(c[i])
                if i==nCargas-1:
                    comienzo=True
        if queue.__len__()==0:
            continue
        else:
            pRef=queue[0]
        for i in range(0,queue.__len__()):
            if queue[i][1]<pRef[1]:
                pRef=queue[i]
        for i in range(0,pRef[1]):
            print(pRef[2],end='')
        
        queue.remove(pRef)
        t=t+pRef[1]
        for i in range(0,queue.__len__()):
            queue[i][3]=queue[i][3]+pRef[1]
        
        if comienzo==True and queue.__len__()==0:
            print()
            break
    
    Penal=0.0
    Espera=0.0
    Respuesta=0.0    
    for x in c:
        Respuesta=Respuesta+x[1]+x[3]
        Espera=Espera+x[3]
        Penal=Penal+(x[1]+x[3])/x[1]
        
    Espera=Espera/nCargas
    Respuesta=Respuesta/nCargas
    Penal=Penal/nCargas
    
    print("\nTiempo de respuesta=%f \nTiempo de espera =%f \nTiempo de penalización=%f"%(Respuesta,Espera,Penal))#imprime los valores SPN
    print("\nAcaba una ejecución\n----------------------")


#Ciclo para entrar N numero de veces a la ejecución 
 
def Ejecucion():
	n = int(input("¿Cuántas ejecuciones de cargas aleatorias quieres hacer?: "))#Se le pide al usuario un numero para determinar las ejecuciones	
	for i in range(n):
            cargasA = [] 
            for i in range (0,nCargas):
                cargasA.append(carga(nProcesos[i]))
                print(cargasA[i][2]+': '+str(cargasA[i][0])+', t='+str(cargasA[i][1])+';',end=' ')
            print()
            #llamada a las funciones 
            cargasA.sort()
            Algoritmo_fifo(cargasA)
            Algoritmo_rr(cargasA,1)
            Algoritmo_rr(cargasA,4)
            Algoritmo_spn(cargasA)
            cargasA.clear()

Ejecucion()