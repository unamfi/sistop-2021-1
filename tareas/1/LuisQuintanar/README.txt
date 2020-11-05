* El problema que decidí resolver fue el de los alumnos y el asesor
* El lenguaje utilizado es python, para ejecutar en la línea de comandos en la carpeta donde se encuentra el archivo escribir: $python3 alumnos_y_asesor.py
* Para resolver este problema utilice dos semáforos, uno nos ayudará a controlar la llegada de los alumnos para que no alteren las variables al mismo tiempo además de que controlará el turno de los alumnos y otro que nos ayudará a despertar al profesor cuando llegue algún alumno
* En este problema no venian propuestas de refinamiento
* Tuve algunas discrepancias cuando lo corrí en Linux y en Windows; en Linux, cuando imprimía los mensajes, no se interrumpían, a diferencia de Windows que hacía cosas extrañas; por ejemplo
	Linux:
		--Tocando la puerta
		++Tengo mi lugar
		    Ayudandole al alumno 1
		--Tocando la puerta
		++Tengo mi lugar
		--Tocando la puerta
		++Tengo mi lugar
		--Tocando la puerta
		_____________________________Ya no hay lugar :c
		    Ayudandole al alumno 1

	Windows
		--Tocando la puerta
		++Tengo mi lugar
		--Tocando la puerta
		++Tengo mi lugar
		--Tocando la puerta
		     Ayudandole al alumno 1
		++Tengo mi lugar
		--Tocando la puerta
		++Tengo mi lugar --Tocando la puerta
		--Tocando la puerta
		_____________________________Ya no hay lugar
   		     Ayudandole al alumno 1 --Tocando la puerta
