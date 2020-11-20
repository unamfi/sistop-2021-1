# Tarea 2: _Comparación de planificadores_ 🚦🕛
---

## Lenguaje y entorno 🖥️

Este programa fue escrito en **Sublime Text 3**, asi como tambien compilado y ejecutado con _SublimeRPL_ una vez ya instalado el Package Control propio de Python3 Version 3.9.0

Tambien se puede ejecutar en sistemas Linux/Ubuntu una vez ya instalado Python3 con la siguiente linea de comando en la terminal (_estando ya una vez dentro del directorio que contiene al archivo.py)_ :
```
python Tarea2.py
```
En sistemas Windows tambien se puede ejecutar con la misma linea de comando desde CMD _(si es que ya se tiene modificada la variable de entorno PATH)_

### Análisis

* Para la resolucion de la tarea mi idea fue que el usuario decidiera cuantos procesos queria analizar. Una vez que escribiera los procesos entrarian a la lista `procesos[]` de la forma `procesos[NombreProceso,TiempoLlegada,TiempoDuracion]`

### Problemas/Errores ❌

Como se podrá dar cuenta mi implementación no esta ni completa ni tiene una correcta ejecucion. La verdad no tuve idea de como implementarlos. En cuanto a la teoria entiendo el correcto funcionamiento pero a la hora de implementarlos es donde me estanque.

Espero pueda darme sus comentarios y criticas de que hice mal en mi analisis para asi poder ver mi error, ya que desde el primer y unico planificador como puede ver, no pude.  

A la hora de ejecutarlos me produce estos errores, la verdad no supe como resolverlos:
```
	¿Cuantos procesos quieres planificar?
4
['H', 6, 5, 'J', 7, 4, 'V', 2, 4, 'P', 0, 5]
18
Traceback (most recent call last):
  File "C:\Users\DELL\Desktop\prueba.py", line 31, in FIFO
    procesos.pop(a+1)
IndexError: pop index out of range

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\DELL\Desktop\prueba.py", line 47, in <module>
    FIFO(n)
  File "C:\Users\DELL\Desktop\prueba.py", line 37, in FIFO
    procesos[k] -= 1
IndexError: list index out of range
```
(Bueno, si pude resolverlos pero al hacerlo se moria mi computadora :( , se trababa, obviamente porque no los resolvi de la manera adecuada)

### Implementación

* En la primer funcion `def generaProcesos(n):`: es donde se generan automaticamente el nombre,llegada y duracion una vez recibidos cuantos procesos se desean analizar.
Me ayude de los caracteres ASCII par darles nombre a los procesos.

* En la segunda funcion `def FIFO(n):`: es donde sucede todo el planificador del mismo nombre, mi idea es verificar si hay un 0 en la lista para saber si hay algun porceso que quiera ejecutarse, si no hay entonces se decrementaria su tiempo de llegada y se mandaria a la lista `imprimir[]` una "-" para avisar que por el momento no hay ningun proceso en ejecucion.

Una vez que se detecte un 0 significa que deberia guardarse en la lista `imprimir[]` las veces que tenga de ejecucion.

Trate de hacer los promedios por lo menos pero para poder obtenerlos tengo que tener bien definido cuando empieza realmente el proceso y cuando acaba, es por es por eso que ni siquiera pude obtenerlos.

Una disculpa por tan pobre tarea :(

