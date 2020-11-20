#!/usr/bin/env python
#_*_ coding: utf8 _*_

#programa Comparacion de planificadores
#Alumnos: Aguilar Barcena Miguel Angel y Rosario Callejas Ramses

from random import randint
import copy
import os                                           #trate de pasar los resultados a un txt pero no supe como

ITERACIONES = 4                                     #numero de cargas, 5
PROCESOS = ["A","B","C","D","E"]                    #nombres de los procesos

def lista(l):                                       #lista para mostrar los procesos
    for i in l:
        print(i)

def carga(process):
    return[randint(0,6),randint(4,8),process]

def fifo(l):                                       #se empieza con fifo
    lista_fifo = copy.deepcopy(l)                  #con deepcopy se copia de la lista original sin modificar esta
    print("\nFIFO\n")
    T = 0.0
    E = 0.0
    P = 1

    lista_fifo[0].append(lista_fifo[0][0])
    T = lista_fifo[0][1]

    for i in range(1,ITERACIONES):
        tex = (lista_fifo[i-1][3] + lista_fifo[i-1][1] - lista_fifo[i][0])
        lista_fifo[i].append(tex + lista_fifo[i][0])
        E = tex + E
        T = T + tex + lista_fifo[i][1]
        P = P + (tex + lista_fifo[i][1]) / lista_fifo[i][1]

    for i in range(0,ITERACIONES):
        for g in range(0,lista_fifo[i][1]):
            print(lista_fifo[i][2],end='|')

    E = E / ITERACIONES
    T = T / ITERACIONES
    P = P / ITERACIONES

    print()
    print("\nT = %f E = %f P = %f" % (T,E,P))
    print("\n************************")

def roundrobin(l,q):
    lista_rr = []
    lista_rr = copy.deepcopy(l)
    print("\nRound Robin q = %d\n"%q)
    queue = []
    t = lista_rr[0][0]
    n = 0
    for i in lista_rr:
        if i[0] == t:
            lista_rr[n].append(0)
            queue.append(i)
        n = n + 1
    r = []
    started = False
    while True:
        for i in range(0,ITERACIONES):
            if started == True:
                break
            if(lista_rr[i][0] <= t + q and lista_rr[i].__len__() < 4):
                lista_rr[i].append(0)
                queue.append(lista_rr[i])

                if(i == ITERACIONES - 1):
                    started = True
        interr_exe = 0
        n = 0

        for i in queue:
            if n == 0:
                i[1] = i[1] - q
                if i[1] > 0:
                    for j in range(0,q):
                        print(i[2],end='|')
                        interr_exe = interr_exe + 1
                elif i[1] <= 0:
                    for j in range(0,q + i[1]):
                        print(i[2],end='|')
                        interr_exe = interr_exe + 1
                    i[1] = 0
                    r.append(i)
                n = 1
            else:
                queue.remove(i)
                i[3] = i[3] + t + interr_exe - i[0]
                i[0] = i[0] + t + interr_exe - i[0]
                queue.insert(n,i)
                n = n + 1
        otro = queue[0]
        queue.remove(otro)
        otro[0] = otro[0] + interr_exe
        queue.append(otro)

        for i in queue:
            if i[1] == 0:
                queue.remove(i)
        if started == True and queue.__len__() == 0:
            print()
            break
        t = t + interr_exe
    P = 0.0
    E = 0.0
    T = 0.0

    for i in range(0,ITERACIONES):
        for g in range(0,ITERACIONES):
            if lista_rr[i][2] == r[g][2]:
                T = T + l[i][1] + r[g][3]
                E = E + r[g][3]
                P = P + (l[i][1] + r[g][3]) / l[i][1]

    E = E / ITERACIONES
    T = T / ITERACIONES
    P = P / ITERACIONES

    print("\nT = %f E = %f P = %f" % (T,E,P))
    print("\n************************")

def spn(l):
    print("\nSPN\n")
    lista_spn = copy.deepcopy(l)
    for h in lista_spn:
        h.append(0)
        h.append(False)
    queue = []
    t = lista_spn[0][0]
    started = False
    while True:
        for i in range(0,ITERACIONES):
            if lista_spn[i][0] <= t and lista_spn[i][4] == False:
                lista_spn[i][4] = True
                lista_spn[i][3] = t - lista_spn[i][0]
                queue.append(lista_spn[i])
                if i == ITERACIONES - 1:
                    started = True
        if queue.__len__() == 0:
            continue
        else:
            punta = queue[0]
        for i in range(0, queue.__len__()):
            if queue[i][1] < punta[1]:
                punta = queue[i]
        for i in range(0, punta[1]):
            print(punta[2],end='|')

        queue.remove(punta)
        t = t + punta[1]
        for i in range(0, queue.__len__()):
            queue[i][3] = queue[i][3] + punta[1]
        if started == True and queue.__len__() == 0:
            print()
            break
    P = 0.0
    E = 0.0
    T = 0.0
    for g in lista_spn:
        T = T + g[1] + g[3]
        E = E + g[3]
        P = P + (g[1] + g[3]) / g[1]

    E = E / ITERACIONES
    T = T / ITERACIONES
    P = P / ITERACIONES

    print("\nT = %f E = %f P = %f" % (T,E,P))
    print("\n************************")

cargas_al = []
print("\n--------- PRIMERA CARGA ---------\n")
for i in range(0,ITERACIONES):
    cargas_al.append(carga(PROCESOS[i]))
    print(cargas_al[i][2] + ": " + str(cargas_al[i][0]) + ", t = " + str(cargas_al[i][1]),end='')
    print()

cargas_al.sort()
fifo(cargas_al)
roundrobin(cargas_al,1)
roundrobin(cargas_al,4)
spn(cargas_al)
cargas_al.clear()

print("\n--------- SEGUNDA CARGA ---------\n")
for i in range(0,ITERACIONES):
    cargas_al.append(carga(PROCESOS[i]))
    print(cargas_al[i][2] + ": " + str(cargas_al[i][0]) + ", t = " + str(cargas_al[i][1]),end='')
    print()

cargas_al.sort()
fifo(cargas_al)
roundrobin(cargas_al,1)
roundrobin(cargas_al,4)
spn(cargas_al)
cargas_al.clear()

print("\n--------- TERCERA CARGA ---------\n")
for i in range(0,ITERACIONES):
    cargas_al.append(carga(PROCESOS[i]))
    print(cargas_al[i][2] + ": " + str(cargas_al[i][0]) + ", t = " + str(cargas_al[i][1]),end='')
    print()

cargas_al.sort()
fifo(cargas_al)
roundrobin(cargas_al,1)
roundrobin(cargas_al,4)
spn(cargas_al)
cargas_al.clear()

print("\n--------- CUARTA CARGA ---------\n")
for i in range(0,ITERACIONES):
    cargas_al.append(carga(PROCESOS[i]))
    print(cargas_al[i][2] + ": " + str(cargas_al[i][0]) + ", t = " + str(cargas_al[i][1]),end='')
    print()

cargas_al.sort()
fifo(cargas_al)
roundrobin(cargas_al,1)
roundrobin(cargas_al,4)
spn(cargas_al)
cargas_al.clear()

print("\n--------- QUINTA CARGA ---------\n")
for i in range(0,ITERACIONES):
    cargas_al.append(carga(PROCESOS[i]))
    print(cargas_al[i][2] + ": " + str(cargas_al[i][0]) + ", t = " + str(cargas_al[i][1]),end='')
    print()

cargas_al.sort()
fifo(cargas_al)
roundrobin(cargas_al,1)
roundrobin(cargas_al,4)
spn(cargas_al)
cargas_al.clear()
