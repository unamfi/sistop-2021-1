#Tarea 2 Comparación de planificadores Nava Escobar Jose Alfredo

Tarea que permite comparar la ejecución de diferentes algoritmos de planificación como lo son FCFS/FIFO, RR y SPN

##Algoritmos empleados
**- FCFS/FIFO**
**-Round Robin**
**-SPN**

##Como funciona
El programa **comparaPlani.py** funciona desde una funcion principal, en esta se ejecuta una funcion que genera una lista de 5 procesos con un orden y duración aleatorias para cada uno de ello.

Posteriormente, con la lista de procesos constituida, esta se envia a 3 funciones que corresponden a los algoritmos de planificación mencionados en el apartado anterior y estas ejecutan tales algoritmos.

Cada función replica el comportamiento de los algoritmos de planificación vistos en clase y se apoyan en tres funciones más que se encargan de obtener el cálculo de la espera y penalización a cada proceso y el promedio del *Tiempo de respuesta*,  *Tiempo en espera* y *Proporción de penalización*.

##Ejecución
El programa fue escrito en el lenguaje de programación Python en su version 3.8.5.

Para ejecutar el programa basta con escribir en la terminal (estando en el directorio donde esta el documento claro):


		$python3 comparaPlani.py





