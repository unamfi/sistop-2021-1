from random import randint #Importamos la funcion randint para poder generar la duración y orden de llagada para cada proceso


#Función que genera una lista de 5 procesos con su tiempo de duración y orden de llegada
def listaProcesos():
    llegada = 0
    i = 0
    procesos = ['A','B','C','D','E'] #Definimos como se van a llamar nuestros procesos
    lista_procesos = [] #Aqui vamos a agregar cada proceso con su respectiva característica

    while i < 5 : #Mediante el while generamos 5 procesos para esta ejecucio
        duracion = randint(1,8) #generamos una duración aletoria para cada proceso
        lista_procesos.append([procesos[i],llegada,duracion])#ingresamos nuestro proceso a la lista
        llegada += randint(0,duracion-1) #El primer proceso llego en 0, los siguientes pueden llegar a la hora que a randint se le antoje \(o_o)/
        i = i+1        
    return lista_procesos #Listo le mandamos la lista de procesos a la función principal

#Función que calcula los promedios de Tiempo de respuesta, Espera y Penalización
def promedioListas(lista):
    l = len(lista)
    aux=0

    for i in range(l):#Mediante el for iremos obteniendo cada valor de la lista
        aux = aux+lista[i]

    promedio=aux/l#Una simple división para calcular el promedio de los valores en la lista
    return promedio#Le regresamos el promedio a la función que lo pidio
    
#Función que obtiene los valores de Espera
def Espera(T,listaP):
    l = len(listaP)
    E = []#Aquí vamos a ir agregando el valor de tiempo de espera para cada proceso
    for i in range(l):
        E.append(T[i] - listaP[i][2])#Calculamos el valor del tiempo de espera como vimos en clase E=T-t

    return E#Regresamos la lista con el tiempo de espera por proceso


#Función que obtiene los valores de Penalización
def Penalizacion(T,listaP):
    l = len(listaP)
    P = []#Aquí vamos a ir agregando el valor de la proporcion de penalizació para cada proceso
    for i in range(l):
        P.append(T[i] / listaP[i][2])#Calculamos la proporción de penalización del proceso en turno con P=T/t

    return P#Le mandamos la lista de penalizaciones a quien no la solicito, la necesita :)

#Función que representa al algoritmo FCFS/FIFO
def FIFO(listaP):
    l = len(listaP)
    tTotal = []
    T = []
    for i in range (l):#Con este for calculamos el valor del tiempo de Respuesta para cada proceso
        if i == 0:
            tTotal.append(listaP[i][2])#Agregamos a la lista auxiliar el valor del tiempo que requiere el primer proceso 
        else:
            tTotal.append(tTotal[i-1]+listaP[i][2])#Despues agregamos el de los que siguen pero ademas le sumamos el del anterior
        
        T.append(tTotal[i]-listaP[i][1])#Aqui guardamos el tiempo total que se tomo para ejectuar el proceso en turno

    E=Espera(T,listaP)#Necesitamos los valores del tiempo de espera de cada proceso, pero que flojera hacerlo nosotros para eso esta la función 'Espera'
    P=Penalizacion(T,listaP)#De igual manera le pasamos el trabajo de calcular la penalización de cada proceso a la funcion que lleva ese nombre


    tProm = promedioListas(T)#'promedioListas' nos hará el favor de obtener el promedio del Tiempo de Respuesta 
    eProm = promedioListas(E)#y de Espera
    pProm = promedioListas(P)#Lo mismo para el promedio de penalizaciones

    tA = 'A'*listaP[0][2]#Guardamos el numero de A's equivalente al tiempo que necesita el proceso A
    tB = 'B'*listaP[1][2]#Lo mismo para B
    tC = 'C'*listaP[2][2]#Tambien para C
    tD = 'D'*listaP[3][2]#Y para D
    tE = 'E'*listaP[4][2]#Ya que estamos por ahí lo hacemos para E

    cadena = tA + tB + tC + tD + tE #Formamos la cadena que representara lo que hace el algoritmo

    print('      FCFS/FIFO: T= %.2f' % tProm,' E= %.2f' % eProm,' P= %.2f' % pProm)#Se imprime el valor de cada promedio para este algoritmo, intente apegarme al formato de su ejemplo 
    print('     ',cadena)#Tambien el esquema visual

#Función que ejecuta al proceso Round Robin con un quantum de 1
def RR(listaP):
    #Definimos variables que serán de gran utilidad para nuestro intento por replicar el algoritmo Round Robin
    l = len(listaP)
    t = listaP[0][2] + listaP[1][2] + listaP[2][2] + listaP[3][2] + listaP[4][2]
    aux = []
    RR1 = []
    T = []
    ta = 0
    tb = 0
    tc = 0
    td = 0
    te = 0
    cadena = ''
    n = 0
    orden = 0
    for i in range(l):#Este for nos permitira obtener el tiempo que necesita cada proceso para ejecutarse
        aux.append(listaP[i][2])#Cada valor lo guardamos en una lista auxiliar
        
    while (n < t):#Con este while vamos a recorrer generar una lista con las apariciones de cada proceso de forma ordenada (porque los procesos son civilizados) pero solo un turno a la vez osea su quantum en 1
        for i in range(l):
            if aux[i] >= 1 and orden >= listaP[i][1]:#Aqui nos aseguramos que cada proceso ordenado solo ingrese una vez por turno a la lista
                RR1.append(listaP[i][0])#Ingresamos la aparicion del proceso ordenado en turno
                aux[i] = aux[i]-1#Como ya registramos esa aparición hay que quitarla de nuestra lista auxiliar o esto no dara el resultado esperado
                orden = orden+1 #Aumentamos el orden para que el proceso en turno si tiene más apariciones no acapare la lista y permita a los demás que tambien ingresen en su turno
        n = n+1

    for i in range(len(RR1)):#Recorremos la lista para poder generar nuestra representación visual, no podemos mostrar unicamente la lista porque no queremos que nuestra representación sea opacada por las otras
        cadena += RR1[i]#Uno a uno se agrega el proceso
    
    #Mediante este For vamos a ver cuanto tiempo en total se llevo en ejecutar cada proceso
    for  i in range (t):
        if(RR1[i] == 'A'):
            ta = i+1
        elif (RR1[i] == 'B'):
            tb = i+1
        elif (RR1[i] == 'C'):
            tc = i+1
        elif (RR1[i] == 'D'):
            td = i+1
        else:
            te = i+1
    
    T.append(ta-listaP[0][1])#Agregamos el valor del Tiempo de espera para el primer proceso
    T.append(tb-listaP[1][1])#Para el segundo
    T.append(tc-listaP[2][1])#El tercero
    T.append(td-listaP[3][1])#El cuarto
    T.append(te-listaP[4][1])#Y el quinto, listo son todos :')

    E=Espera(T,listaP)#'Espera' Nos hara el favor de calcular el tiempo de espera para cada proceso
    P=Penalizacion(T,listaP)#Mientras que 'Penalización' nos ayudará con la proporción de penalización

    tProm = promedioListas(T)#Como en los otros algoritmos, promedioListas se pone la capa y nos calcula el promedio del Tiempo de Respuesta para cada proceso
    eProm = promedioListas(E)#El del tiempo de espera
    pProm = promedioListas(P)#Y el del promedio de penalización

    print('      RR: T= %.2f' % tProm,' E= %.2f' % eProm,' P= %.2f' % pProm)#Se imprime el valor de cada promedio para este algoritmo
    print('     ',cadena)#Sin olvidar la representación visual

#Función que representa al algoritmo de 'El proceso más corto' o 'Shortest Process Next'
def SPN(listaP):
    l = len(listaP)
    #Definimos algunas variables que nos ayudaran más adelante en la implementacion de SPN
    T = []
    aux2 = []
    cadena = ''
    tTotal = []
    ordCortos = []
    ordCortos.append(listaP[0])#Tomamos el primer proceso con sus características para asegurarnos que este se ejecute primero
    listaP.pop(0)#Lo sacamos de nuestra lista 
    listaP.sort(key=lambda x: x[2])#Hay que ordenarla para ver cual sigue del primer proceso y que sea mas corto, de ahí en adelante
    for i in range(l-1):
        ordCortos.append(listaP[i])#Una vez que ya esta ordenado esto, lo agregamos en la lista que tiene ya al primer proceso y que no se quede solo :(
    for i in range (l):
        if i == 0:
            tTotal.append(ordCortos[i][2])#Agregamos a la lista auxiliar el valor del tiempo que requiere el primer proceso 
        else:
            tTotal.append(tTotal[i-1]+ordCortos[i][2])#Despues agregamos el de los que siguen pero ademas le sumamos el del anterior
        
        T.append(tTotal[i]-ordCortos[i][1])#Aqui guaramos el tiempo de respuesta para este proceso

    E=Espera(T,ordCortos)#Nuevamente le mandamos el trabajo de calcular los valores del tiempo de espera a 'Espera'
    P=Penalizacion(T,ordCortos)#Y los de penalización a 'Penalización' Me suena a pleonasmo el comentar esto así 

    #De sacar los promedios se encargara 'promedioListas'
    tProm = promedioListas(T)
    eProm = promedioListas(E)
    pProm = promedioListas(P)

    for i in range(l):#Este for nos va ayudar a formar nuestra representación visual
        aux2.append(ordCortos[i][0])#Aquí tenemos que proceso ira primero de acuerdo a cual es más corto, pero el primero siempre será A
        cadena += aux2[i]*ordCortos[i][2]#Dependiendo cuantas veces aparezca el proceso en turno se lo agregaremos al string que será nuestra representación visual 
    

    print('      SPN: T= %.2f' % tProm,' E= %.2f' % eProm,' P= %.2f' % pProm)#Se imprime el valor de cada promedio para este algoritmo
    print('     ',cadena)#Y su representación visual


#Función principal
def principal():
    maxEjecuciones = 5 #Se define el numero de ejecuciones de cada algoritmo, 5 son buenas para comparar :)
    rondas = ['Primera','Segunda','Tercera','Cuarta','Quinta']
    for i in range(maxEjecuciones): #Mediante el for ejecutamos 5 veces cada algoritmo
        procesos = listaProcesos()#Llamada a la función que generara nuestras listas con procesos aleatorios
        total = procesos[0][2] + procesos[1][2] + procesos[2][2] + procesos[3][2] + procesos[4][2]#Aquí obtenemos el tiempo total que se tomaran los 5 procesos en turno de ejecutar, ni más ni menos
        print('-',rondas[i],' ejecucion')
        print('     ',procesos[0][0],': ',procesos[0][1], ', t=',procesos[0][2],';  ',procesos[1][0],': ',procesos[1][1], ', t= ',procesos[1][2],';  ',procesos[2][0],': ',procesos[2][1], ', t= ',procesos[2][2],';  ',procesos[3][0],': ',procesos[3][1], ', t= ',procesos[3][2],';  ',procesos[4][0],': ',procesos[4][1], ', t= ',procesos[4][2],'  (tot:',total,')')
        FIFO(procesos)#Primero FIFO
        RR(procesos)#Despues Round Robin
        SPN(procesos)#Y para terminar El proceso mas corto siguiente
        print('')
        print('')

principal()#Llamamos a la función principal pa' que todo funcione




