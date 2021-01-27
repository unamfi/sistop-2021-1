#!/usr/bin/python3
l = ['A', 'B', 'C', 'D', 'E']
segura = []

proclama = {'A': [], 'B': [], 'C': [], 'D': [], 'E': []}
asignado = {'A': [], 'B': [], 'C': [], 'D': [], 'E': []}
libres = []

while len(l) > 0:
    ### Esta diferencia entre dos listas _debe_ resultar en remover
    ### todos los elementos de asignado de proclama
    menores = list( filter( lambda x: proclama[x] - asignado[x] > libres, l) )
    if len(menores) == 0:
        raise Exception('Estado inseguro')
    primero = menores[0]
    libres.append(asignado[primero])
    l.remove(primero)
    segura.push(primero)

print('La secuencia segura encontrada es: %s' % segura)
