# Ejercicio de sincronización: _Los alumnos y el asesor_ 🚦🕛
---

## Presentación

- Un profesor de la facultad asesora a varios estudiantes, y estamos en su horario de atención.

- Modelar la interacción durante este horario de modo que la espera (para todos) sea tan corta como sea posible.


## Reglas 📋

- Un profesor tiene x sillas en su cubículo
  - Cuando no hay alumnos que atender, las sillas sirven como
sofá, y el profesor se acuesta a dormir la siesta.
- Los alumnos pueden tocar a su puerta en cualquier momento,
pero no pueden entrar más de x alumnos
- Para evitar confundir al profesor, sólo un alumno puede
presentar su duda (y esperar a su respuesta) al mismo tiempo.
  - Los demás alumnos sentados deben esperar pacientemente su
turno.
  - Cada alumno puede preguntar desde 1 y hasta _y_ preguntas
(permitiendo que los demás alumnos pregunten entre una y
otra)


## Lenguaje y entorno 🖥️

Este programa fue escrito en **Sublime Text 3**, asi como tambien compilado y ejecutado con _Build_ una vez ya instalado el Package Control propio de Python3 Version 3.9.0

Tambien se puede ejecutar en sistemas Linux/Ubuntu una vez ya instalado Python3 con la siguiente linea de comando en la terminal (_estando ya una vez dentro del directorio que contiene al archivo.py)_ :
```
python tarea1.py
```
En sistemas Windows tambien se puede ejecutar con la misma linea de comando desde CMD _(si es que ya se tiene modificada la variable de entorno PATH)_


### Mecanismos/Patrones 🚦

Para la resolucion del ejercicio utilice 3 patrones basados en semáforos: 
 
* **Señalización**
```
despertar_profesor = threading.Semaphore(0)
```
Con esta señalización se manda a despertar/avisar al asesor una vez que un alumno quiere entrar al cubículo vacío.

* **Mutex**
```
mutex_orden = threading.Semaphore (1)
```
Con este mutex una vez que se adquiere se evita que haya mas de un alumno (_hilo_) preguntando y asi se evite confundir al profesor.

* **Mutiplex**
```
sillas= 5
mutex_cubiculo = threading.Semaphore(sillas)
```
Con este multiplex se logra que solo haya cierto numero de alumnos con silla dentro del salón.
La variable sillas es la que delimita cuantas sillas hay dentro del salon y por ende cuantos alumnos van a poder estar dentro.


### Análisis

* Para la implementación del programa me di cuenta que tenia una cierta similitud con el ejercicio de Santa Claus visto en la clase y fue así como lo tome en consideración para la construcción del programa.

	De manera análoga la función `elfo(id)` la tome como mi función `alumno(id)` dado que por ciertas circunstacias se terminara despertando/avisando al _"jefe"_ para resolver algún problema/duda.

	La función `santa()` la tome como mi función `profesor()` dado que una vez despierto ayudará a quien lo necesite.

* Analizando detenidamente las reglas del juego me di cuenta que en:
```
Para evitar confundir al profesor, sólo un alumno puede
presentar su duda (y esperar a su respuesta) al mismo tiempo.
```
Se especifica la interaccion del asesor cuando tiene varios alumnos dudosos pero no se menciona si mientras esta ayudando pueda dar permiso de ingresar a un nuevo alumno al cubiculo (_si es que hay cupo disponible_) y es por esto que que al implemntar decidí que él pudiera darle permiso a mas alumnos aparte de estar resolviendo la duda.

* Para que se pueda visualizar al asesor descansando cuando ya haya respondido todas las dudas recomiendo que no se aleje mucho el numero de alumnos (_hilos_) del numero de sillas totales (_que aqui yo puse 5 pero puede variar segun se deseé_) ya que por el ciclo while el asesor la mayoria de veces estará ocupado. 

	Tambien se puede poner como comentario el ciclo `while True:` de la función `alumno(id)` para visualizar mas rápido al asesor dormir una vez todos los hilos hayan terminado

	Estas dos observaciones hacen  ver que no hay una espera activa del profesor, ya que no esta despierto esperando mas dudas, si no tiene entonces duerme y si esta despierto es porque esta ayudando.


### Implementación

* Las líneas de codigo:

```
	print('Toc Toc ... Soy %d ¿Puedo pasar profe? ' %id)
	mutex_cubiculo.acquire()
	alumnos_con_dudas.insert(0,id)
	lista_dudas.insert(0,dudas)
	despertar_profesor.release()
	print('Si claro, adelante %d ' %id)
	print('Alumno %d entrando' %id)
	mutex_orden.acquire()
	print('Soy %d y tengo %d duda(s) ' %(id,dudas))
```

Tienen una parte fundamental de mi progrma dado que el alumno pide permiso para poder pasar y **SI hay sillas disponibles** tomara `mutex_cubiculo.acquire()` y por consecuencia despertará/avisará al asesor y asi mismo, éste le dará "permiso" para poder entrar con `print('Si claro, adelante %d ' %id)` que claro, si ya tomo el `mutex_cubiculo.acquire()` es porque ya tiene permiso pero el print es para que visualmente veamos que no pudo entrar y se queda esperando permiso. Ahora bien, si el alumno pide permiso para poder pasar y si **NO hay sillas disponibles** entonces se quedará dormido esperando a que un alumno salga del cubículo para poder ingresar.

La linea:
```
print('Si claro, adelante %d ' %id)
```

Que a simple vista es un frase propia del asesor, la coloque dentro de la función `alumno(id)` ya que asi podía ponerle el `id` para hacerlo mas visual. Es una de las razones por las cuales mi programa tiene muchas impresiones en pantalla y pueda hacer un poco pesada la lectura en la ejecución pero de este modo es como puedo saber errores a la hora de la implementación y asi saber bien que esta haciendo el programa.

* Ocupe la función `insert()` en las siguientes líneas:

```
alumnos_con_dudas.insert(0,id)
lista_dudas.insert(0,dudas)
```

Para poder meter en la lista al alumno con duda al principio (_indice 0_), puesto que si ocupaba `append()` a la hora de que el asesor resolvia las dudas lo hace de manera que el último alumno que llegó era al primero que ayudaba y así de esa manera la espera ya no sería tan corta como fuera posible ya que los alumnos que llegaron primero y tuvieran mas de una duda se quedarian esperando mucho tiempo. 


### Refinamientos

El ejercicio no pedia como tal algún refinamiento ya que se limita diciendo: _"...interacción durante este horario..."_ pero siento que podría tener alguno, como por ejemplo:

- Delimitar el horario para el asesor
  - Aqui mismo podria ser los dias que daría asesorias.


### Problemas/Errores ❌

Al final no tuve inconvenientes, claro, esperando que mi implementación sea corrrecta. Hubo algunos problemas y dudas pero pude resolverlos.