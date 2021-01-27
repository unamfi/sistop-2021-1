Tercer Proyecto

Sistemas Operativos

Profesor: Gunnar Wolf

Alumno: Diego Armenta

-----------------------------
El siguiente programa se implemento en python 3.6.9

Consta de los siguientes metodos:

	listar: no recibe argumentos, itera en el directorio del sistema de archivos e imprime los nombres que encuentre

	erase: recibe un parametro, lo busca en el directorio del sistema de archivos y sustituye el nombre para que se sepa que el espacio esta disponible

	todesktop: recibe dos argumentos, busca el primero en el sistema de archivos y copia los datos en la ubicacion dada por el segundo argumento

	defrag: no recibe argumentos, a partir de los tamaños y puntos de inicio de los archivos listados crea una lista con orden ascendente a partir de los clusters de inicio. Con esto se calcula el espacio libre que queda entre archivos, cada archivo se relocaliza individualmente justo donde termina el archivo anterior. Con esto se elimina el espacio entre archivos. Una vez hecho esto se vuelve a mapear la informacion de cluster de inicio para cada archivo en el directorio.

	IMPORTANTE: La funcion de defragmentacion se programo para reducir el espacio entre informacion de archivos, no reduce los espacios en el directorio.

Como utilizar:

	El programa solo necesita correrse con la siguiente sentencia:
	
		"python3 fs.py"

	El archivo fiunamfs.img debe estar en el mismo directorio donde se corra el programa

	La interfaz de usuario solo le permitira ingresar los comandos programados y le indicara cuando se necesiten o sobren argumentos

	Para detener el programa solo utilice ctrl+c

	IMPORTANTE: Los argumentos de archivo y ruta de archivo NO llevan comillas, los archivos de ruta no deben llevar diagonal al final pero si al inicio.
		Ejemplos de uso: cp mensaje.png .
				 cp mensaje.png /home
				 rm logo.png



