procesos = ["A","B","C","D","E"]
tiempos = [0,0,0,0,0]

for i in range(len(procesos)):
    tiempos[i]=int(input("Ingrese un tiempo para el proceso: "+ procesos[i]+": "))

def FCFS():
    tot = 0
    tiempoT = 0
    tiempoE = 0
    tiempoP = 0
    proceso = []
    for i in range(len(procesos)):
        for j in range(tiempos[i]):
            proceso.append(procesos[i])
        tiempoT+= (tot + tiempos[i])
        tiempoE+=tot
        tiempoP+=((tot + tiempos[i])/tiempos[i])
        tot+=1
        proceso.append("*")
    print("total: " ,tot)
    print("T: ", tiempoT/5)
    print("E: ",tiempoE/5)
    print("P: ",tiempoP/5)
    print(proceso)

def SJF():
    n = len(procesos)
    for i in range(n-1):
        for j in range(1, n-i-1): 
            if tiempos[j] > tiempos[j+1] : 
                tiempos[j], tiempos[j+1] = tiempos[j+1], tiempos[j] 
                procesos[j], procesos[j+1] = procesos[j+1], procesos[j] 
    print(procesos)
    print(tiempos)
    FCFS()
  

def RR(q):
    proc = procesos
    tim = tiempos
    tT = []
    tTot =0
    tP=[]
    tE=[]

    esperas = {"A":[],"B":[],"C":[],"D":[],"E":[]}
    rafagas = {"A":0,"B":0,"C":0,"D":0,"E":0}

    i=0
    k = len(proc)
    while i < k:
        if (tim[i]>q):
            tTot += q
            esperas(proc[i]).append(q)
            rafagas(proc[i])+=q
            proc.append(proc[i])
            tim.append(tim[i]-q)
            proc.pop(i)
            tim.pop(i)
            

        else:
            tTot += tim[i]

            esperas(proc[i]).append(tim[i])
            rafagas(proc[i])+=tim[i]
            proc.pop(i)
            tim.pop(i)

        k = len(proc)





print("-------------------------FCFS------------------------------------")
FCFS()
print("--------------------------SJF-----------------------------------")
SJF()
print("----------------------------RR1---------------------------")
RR(5)


