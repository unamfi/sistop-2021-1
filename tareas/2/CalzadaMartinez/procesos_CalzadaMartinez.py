import random 

#Se generara cada proceso 
def generaLista():
    numProceso = 5
    lis=['A','B','C','D','E','F']
    proceso = []
    llegada = 0
    for i in range(numProceso): 
        tiempoRandom = random.randint(1,8) 
        proceso.append([lis[i],llegada,tiempoRandom]) 
        llegada += random.randint(0,tiempoRandom-1) 
    return proceso 
    
    """
    Se crea el algoritmo de FCFSalmacenando 
    la longitud de arreglo del proceso
    """
def FCFS(colas): 
    l = len(colas) 
    t = [colas[i][2] for i in range(l)] #Es el tiempo total que dura el proceso
   
    T = [0 for i in range(l)]
    E = [0 for i in range(l)]
    P = [0 for i in range(l)]
    End = [0 for i in range(l)]
    salida = '' #Cadena vacía para guardar la salida

    for i in range(l):
        if i == 0:
            End[i] = colas[i][2]
        else:
            if colas[i][1] <= End[i-1]:
                End[i] = colas[i][2] + End[i-1]
            else:
                End[i] = colas[i][1] + colas[i][2]
        T[i] = End[i] - colas[i][1]
        E[i] = T[i] - colas[i][2]
        P[i] = T[i]/ colas[i][2]
        
     #Se calculara, respuesta, espera y la proporción de penalización (T,E,P)
    auxT = 0
    for i in range(l):
        auxT += T[i]
    averageT = auxT / l
    auxE = 0
    for i in range(l):
        auxE += E[i]
    averageE = auxE / l
    auxP = 0
    for i in range(l):
        auxP += P[i]
    averageP = auxP / l
    print ('FCFS:   T = %.2f' % averageT,'\t', 'E = %.2f' % averageE,'\t', 'Promedio = %.2f' % averageP) #Imprime la tabla con el formato y los valores que regresa son los promedios


    # Se crearan las rondas de manera aleatoria  con valores de entre 1 a 10
rondas = random.randint(1,10)  
for i in range (rondas):
    #for i in rond
    colas = generaLista()

    print ('Ronda número :', i+1 )
    strr = str(colas)
    strrAux = strr.replace("[" , " ")
    str1 = strrAux.replace("]" , " ")
    print ('Proceso:', str1)
    FCFS(colas)