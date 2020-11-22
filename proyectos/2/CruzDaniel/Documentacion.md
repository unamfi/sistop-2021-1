# Proyecto2: _Una situación cotidiana paralelizable_ 🚦🕛
---

Los eventos en el mundo en que vivimos se producen de forma masivamente paralela, por lo cual, la concurrencia puede presentarse en muchos casos, en ámbitos no necesariamente constreñidos al cómputo.

Por tanto, es de esperarse que –si existieran las primitivas de sincronización en el mundo real– podríamos aplicar lo estudiado en esta unidad a muchas otras situaciones.

Para este proyecto, se pide que:

Identifique un proceso de la vida real que presente características de concurrencia. Normalmente, cualquier proceso que presente eventos realizados por múltiples actores (sea como sea que los queramos entender)


## Identificación y descripción del problema

Mi idea para implementar fue hacer una simulación del servicio de un restaurante. 
Los comensales una vez asignados en una mesa se les tomará la orden para despues ser servida y degustada, una vez que haya terminado pagará por el servicio y saldrá del inmueble.
 
* **1. Descripcion de la situacion modelada**
	En mi moleado, el servico del restaurante será como el de la mayoría:

	Habrá dos hostess, la primera será la persona que está en la entrada y es la encargada de recibir y atender en primera instancia a los clientes que llegan al restaurante, si es preciso los anota en una lista de espera o bien les asigna una mesa disponible para que asi la segunda hostess sea la encargada de llevarlos a dicha mesa. La decisión de ocupar dos personas es para que siempre haya alguien en la entrada y sea un mejor servicio, ya que de no ser así se podría dar la posibilidad de que mientras la unica hostess acomodara a los comensales llegara otro cliente y tuviera que esperar una respuesta hasta que regresara la hostess.

	Una vez sentados el grupo de comensales tomará un tiempo para prepar su orden, una vez lista avisaran a algún mesero para que les tome dicha orden. 

	Una vez tomada la orden por el mesero será él quien sea el encargado de llevar la orden al cocinero y a su vez el cocinero de tomar dicha orden para prepararla y avisar de regreso al mesero que la orden esta lista. El mesero llevará a la orden lista al comensal para que asi pueda degustarla.

	Una vez que todos los comensales hayan acabado, llamaran al mesero para pedir la cuenta y asi pagarala para despues proceder a retirarse del lugar.

* **2. ¿Dónde pueden verse las consecuencias nocivas de la concurrencia? ¿Qué eventos pueden ocurrir que queramos controlar?**
	La primer consecuencia que puedo ver es en la entrada, puede haber mas de un cliente quiera preguntar si hay lugar disponible al mismo tiempo.
	Una segunda consecuencia es que el mesero pueda recibir mas de una orden al mismo tiempo y asi tambien confundir al cocinero.

* **3. ¿Hay eventos concurrentes para los cuales el ordenamiento relativo no resulta importante?**
	
	No hay ninguno, ya que dependiendo de la llegada de cada evento es como será tratado.
	

### Mecanismos/Patrones 🚦

* Descripción de los mecanismos de sincronización empleados:
 
	* **Aún no**
```

```
* Lógica de operación:
 
	* **Identificación del estado compartido (variables o estructuras globales):**

	* **Descripción algorítmica del avance de cada hilo/proceso:**
		* **Hostess 1:**

			1. Recibir al cliente
			2. Asignar mesa o poner en la lista de espera
			3. Avisar a la segunda hostess.

		* **Hostess 2:**

			1. Llevar al cliente a su mesa
		
		* **Cliente:**

			1. Pregunta disponibilidad
			2. Espera/Se sienta en la mesa
			3. Prepara su orden
			4. Pide su orden
			5. Degusta
			6. Pide la cuenta
			7. Paga

		* **Mesero:**

			1. Toma orden
			2. Lleva la orden al chef
			3. Sirve la comida
			4. Lleva la cuenta

		* **Chef:**

			1. Recoge la orden
			2. Cocina
			3. Avisa "¡orden lista!"

	* **Descripción de la interacción entre ellos (sea mediante los mecanismos de sincronización o de alguna otra manera):**

	* **Capturas de ejecuciónes exitosas:**
	

## Lenguaje y entorno 🖥️

Este programa fue implementado en Python3 Version 3.9.0.
Fue escrito  **Sublime Text 3**, asi como tambien compilado y ejecutado con el mismo gracias a la herramienta _SublimeREPL_ una vez ya instalado el Package Control propio de Python3

* **Sistemas Windows**
	Tambien fue ejecutado en sistemas Windows con la siguiente linea de comando en la terminal CMD _(si es que ya se tiene modificada la variable de entorno PATH)_:
```
	python Proyecto2.pyw
```
	_(Si no se tiene modificada la variable de entorno Path se necesita acceder a la ruta donde se tiene instalado Python y ejecutar desde ahi el archivo, que dicho archivo debe estar en la misma ruta.)_

* **Sistemas Windows**
	En sistemas Linux/Ubuntu tambien se puede ejecutar con la siguiente linea desde cualquier consola de comandos _(si ya se tiene instaldo Tkinter)_: 
```
python3 Proyecto2.pyw
```
	Si aún no se tiene instalado Tkinter basta con ingrasar los siguientes comandos:
```
sudo apt-get install python3-tk (Versiones Python 3)
```
``` 
sudo apt-get install python-tk (Versiones Python 2.7)
```