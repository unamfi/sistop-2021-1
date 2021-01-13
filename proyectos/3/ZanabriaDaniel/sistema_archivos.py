# -*- encoding: utf-8	

# importamos las librerias nescesarias
import os, math, time, datetime

# declaracion de arreglos a utilizar
archivos = []
tamanio = []
localizacion = []
info=[]

# Con esta función extraemos toda la información del SISTEMA DE ARCHIVOS, almacenándola en un arreglo "info"
def obtenerInformacion():
    # abrimos el sistema de archivos ejemplo (fiunamfs.img) en modo lectura y almacenamos en una variable sistema_archivos
	sistema_archivos = open('fiunamfs.img','r')
    # inicializamos la posicion actual en 0
	posicion_actual = 0
    # configuramos la posicion actual del archivo a 0. no mandamos segundo parámetro.
	sistema_archivos.seek(posicion_actual)
	# obtenemos el nombre del sistema de archivos leyéndolo del mismo y lo guardamos ne variable "byte"
	byte = sistema_archivos.read(8)
    # agregamos el nombre a un arreglo llamado "info" en la primera posición
	info.append(byte)
	# obtenemos la version de la implementacion.
	posicion_actual = 10
	sistema_archivos.seek(posicion_actual)
    # leemos los siguientes 3 caracteres para leer la versión con formato X.X
	byte = sistema_archivos.read(3)
	info.append(byte)
	# Etiqueta del volumen
	posicion_actual = 20
	sistema_archivos.seek(posicion_actual)
	byte = sistema_archivos.read(15)
	info.append(byte)
	# Tamaño del cluster en bytes
	posicion_actual = 40
	sistema_archivos.seek(posicion_actual)
	byte = sistema_archivos.read(5)
	info.append(byte)
	# Numero de clusters que mide el directorio
	posicion_actual = 47
	sistema_archivos.seek(posicion_actual)
	byte = sistema_archivos.read(2)
	info.append(byte)
	# Numero de clusters que mide el directorio
	posicion_actual = 52
	sistema_archivos.seek(posicion_actual)
	byte = sistema_archivos.read(8)
	info.append(byte)
	# se cierra el archivo para no seguir utitilizando recursos innecesarios
	sistema_archivos.close()


# Volvemos a abrir el sistema de archivos para extraer listas con los NOMBRES DE LOS ARCHIVOS, TAMAÑOS y CLUSTER inicial de cada archivo
def obtenerArchivos():
    # abrimos el archivo en modo lectura
	sistema_archivos = open('fiunamfs.img','r')
    # nos ubicamos en la posición competente para extraer la información que buscamos, aunque desconozco porqué es este número en específico
	posicion_actual = 2048
    # procurando no "pasarnos" usamos una función WHILE para controlar el flujo
	while posicion_actual < 10240:
        # apuntamos dentro del archivo en la posición actual
		sistema_archivos.seek(posicion_actual)
		# obtenemos el NOMBRE DEL ARCHIVO y lo almacenamos en una variable byte
        # delimitamos en la funcion READ() que queremos leer únicamente 15 CARACTERES a partir de la posición en la que nos encontramos
		byte = sistema_archivos.read(15)
        # nos aseguramos que el archivo siendo leído no tenga algún tipo de error
		if byte != 'Xx.xXx.xXx.xXx.':
            # agregamos al arreglo de ARCHIVOS, eliminamos todos los espacios que puedan haber
			archivos.append(byte.replace(" ",""))
            # nos ubicamos en donde comienza la información acerca del tamaño del archivo
			sistema_archivos.seek(posicion_actual+16)
			# tamano del archivo
            # lo convertimos de CARACTER en un NÚMERO ENTERO
			tamanio.append(int(sistema_archivos.read(8)))
            # nos ubicamos donde comienza la info acerca de la ubicación del archivo
			sistema_archivos.seek(posicion_actual+25)
			# ubicacion del archivo
            # la convertimos en un numero entero y la agregamos al arreglo de localización
			localizacion.append(int(sistema_archivos.read(5)))
        # avanzamos al siguiente archivo agregando 64 bits(?) a la posición actual
		posicion_actual += 64
    # una vez extraído toda la info de cada archivo del sistema, redeterminamos la posición actual en la posicion 10240
	posicion_actual = 10240
    # cerramos el archivo
	sistema_archivos.close()


# función "copiar a" para copiar de mi PC al sistema de archivos
def copiarA(archivo):
	# abro mi imagen en MODO de LECTURA+ (lectura y escritura) BINARIO, abrimos el archivo binario en modo elctura y escritura
	sistema_archivos = open('fiunamfs.img', 'r+b')
	# obtengo la posicion donde se encuentra en la lista archivos
	posicion_arch = archivos.index(archivo)
	# obtengo el tamaño 
	tamanio_archivo_a_copiar = tamanio[posicion_arch] 
    # tomamos el tamaño del archivo y lo multiplicamos por 2048 para definir su nueva ubicación
	ubicacion = localizacion[posicion_arch]*2048
    # con SEEK nos ubicamos en el valor que contenga la variabel UBICACION
	sistema_archivos.seek(ubicacion) 

    # creamos un archivo NUEVO (copia) con el mismo nombre que la variable "archivo" en MODO ESCRITURA BINARIO
	copia = open(archivo,'wb') 
    # escribimos en el todo lo que leamos del archivo original respetando el tamaño de lo que queremos leer
	copia.write(sistema_archivos.read(tamanio_archivo_a_copiar)) 
    # cerramos ambos archivos
	copia.close()
	sistema_archivos.close()
	print("\n archivo copiado con exito ...\n")

# borrar archivos
def deleteFile(archivo_a_eliminar):
	with open('fiunamfs.img','r+') as sistema_archivos:
		posicion_actual = 2048
		sistema_archivos.seek(posicion_actual)
		# mientras la posicion este dentro del directorio puedo buscar el archivo
		while posicion_actual < 10240:
			# vamos a leer el nombre de los archivos en el arreglo de archivos: "sistema_archivos"
			nombre_arch = sistema_archivos.read(15)
			# hacemos una copia del arreglo quitando el primer y ultimo caracter del arreglo original (quitamos comillas)
			nombre_arch_stp = nombre_arch.strip()
			# compruebo que el nombre del archivo a eliminar exista en directorio en la posicion actual en fiunamfs.img
			if (nombre_arch_stp == archivo_a_eliminar):
				# si se encuentra, se eliminan metadatos del archivo
				sistema_archivos.seek(posicion_actual)
				sistema_archivos.write("               ")
				sistema_archivos.write('0'*49)
				print(" archivo eliminado ...\n")
				x = len(archivos)
				# actualizacion de las listas de informacion de los archivos
				for i in range(x):
					archivos.pop(0)
					tamanio.pop(0)
					localizacion.pop(0)
				obtenerArchivos()
				break
			else:
				# no se encuentra el archivo: se recorre nuestro puntero para encontrarlo
				posicion_actual += 64
				sistema_archivos.seek(posicion_actual)
				# si acabamos de recorrer el directorio y no se encuentra el archivo, no existe
				if(posicion_actual==10240):
					print(" error: el archivo no existe")

# funcion "copiarDesde" para copiar desde el sistema de archivos a mi PC
def copiarDesde(path):
	sistema_archivos = open('fiunamfs.img', 'r+b')
	# obtenemos el tamaño del archivo
	peso = os.path.getsize(path)
	# 
	t = datetime.datetime.strptime(time.ctime(os.path.getctime(path)),"%a %b %d %H:%M:%S %Y")
	fecha_creacion = str(t.year)+str(t.month).zfill(2) + str(t.hour).zfill(2)+ str(t.minute).zfill(2) + str(t.second).zfill(2) #obtengo fecha de creacion
	fm = datetime.datetime.now()
	fecha_modificacion = str(fm.year)+str(fm.month).zfill(2) + str(fm.hour).zfill(2)+ str(fm.minute).zfill(2) + str(fm.second).zfill(2) #obtengo fecha de modificacion
	x =localizacion.index(max(localizacion))
	# obtengo el cluster origen
	cluster_original = localizacion[x] 
	# obtener el tamano que ocupa en cluster el archivo
	cluster_tamanio = math.ceil(tamanio[x]/2048.00)
	# calculo la direccion del cluster
	total = (cluster_original + cluster_tamanio)*2048 
	path_archivo = open(path,'rb') 
	datos = path_archivo.read(peso) 
	sistema_archivos.seek(total) 
	sistema_archivos.write(datos) 
	sistema_archivos.close()
	# obtengo el nombre del archivo 
	name = path.rjust(15) 
	sistema_archivos = open('fiunamfs.img','r+b')
	posicion_actual = 2048

	while posicion_actual < 10240:
		sistema_archivos.seek(posicion_actual)
		byte = sistema_archivos.read(15)
		if byte == 'Xx.xXx.xXx.xXx.':
			# guardo la informacion 
			sistema_archivos.seek(posicion_actual+0)
			# nombre del archivo
			sistema_archivos.write(name.encode('ascii'))
			sistema_archivos.seek(posicion_actual+16)
			# Tamaño del archivo
			sistema_archivos.write(str(peso).encode('ascii'))
			sistema_archivos.seek(posicion_actual+25)
			# Cluster inicial
			sistema_archivos.write(str(total).encode('ascii'))
			sistema_archivos.seek(posicion_actual+31)
			# Hora y fecha de ultima modificacion 
			sistema_archivos.write(fecha_modificacion.encode('ascii'))
			sistema_archivos.seek(posicion_actual+46)
			# Hora y fecha de creación
			sistema_archivos.write(fecha_creacion.encode('ascii'))
			sistema_archivos.close()
			path_archivo.close()
			print("archivo copiado ...")
			return
		posicion_actual += 64
	posicion_actual = 10240

# funcion "salida"
def salida(texto_sin_split):
    # dividimos el mensaje de salida en palabras
    texto_despedida = texto_sin_split.split()
    # por palabra la imprimimos y dormimos al proceso .5 segundos para que el usuario observe el proceso con más detenimiento
    for palabra in texto_despedida:
        print(palabra)
        time.sleep(.5)

# funcion principal 
def main():
	#Abrimos el archivo y leemos donde se encuentra el nombre del sistema
	validacion=[]
	sistema_archivos = open('fiunamfs.img','r')
	posicion_actual = 0
	sistema_archivos.seek(posicion_actual)
	byte = sistema_archivos.read(8)
    # leemos el nombre del sistema de archivos para corroborar que en efecto es el archivo que queríamos leer y no otro
	validacion.append(byte)
	print("Bienvenido al sistema de archivos "+validacion[0])
	# Aqui validamos que el sistema de archivos es el tenga el nombre de FiUnamFS
	if (validacion[0] == 'FiUnamFS'): 
		sistema_archivos = open('fiunamfs.img', 'r+')
		sistema_archivos.close()
		obtenerArchivos()
		

		while(True):
			print("\nOpciones:\n1. Listar archivos\n2. Copiar un archivo a mi PC\n3. Copiar un archivo desde mi PC\n4. Eliminar un archivo\n5. Salir\n")
			opcion = input("Ingresa el número de la opción que deseas elegir: ")
			tipoDato = type(opcion)
			# Se obtine la informacion del sistema
			if(opcion==1):
                # os.system('clear') limpia la terminal
				os.system('clear')
				print("\n\nopcion: Listar archivos\n")
				x = len(archivos)
				for i in range(x):
                    # array.pop(0) para sacar el primer (indice "0") elemento del arreglo
					archivos.pop(0)
					tamanio.pop(0)
					localizacion.pop(0)
				obtenerArchivos()
				for i in range(len(archivos)):
					print(archivos[i])
				x = len(archivos)
				for i in range(x):
					archivos.pop(0)
					tamanio.pop(0)
					localizacion.pop(0)
				obtenerArchivos()
			elif(opcion==2):
				os.system('clear')
				print("\n\nopcion: Copiar archivo a mi ordenador\n")
				nombreArchivo = raw_input("Ingresa el nombre del archivo: ")
				copiarA((nombreArchivo))
			elif(opcion==3):
				os.system('clear')
				print("\n\nopcion: Copiar archivo desde mi ordenador\n")
				nombreArchivo = raw_input("Ingresa el nombre del archivo: ")
				copiarDesde((nombreArchivo))
			elif(opcion==4):
				os.system('clear')
				print("\n\nopcion: Eliminar un archivo\n")
				archivo_a_eliminar = raw_input("\nArchivo a eliminar: ")
				deleteFile(archivo_a_eliminar)
			elif(opcion==5):
				os.system('clear')
				salida (" cerrando . . .")
				os.system('clear')
				break
			elif (tipoDato==str):
				print('no se puede esa opcion intentalo de nuevo')
				main()
				
	else:
		print("error: no se logró abrir el sistema de archivos")
		return

#funcion para obtener la informacion del sistema de archivos
obtenerInformacion()
print("Información:\nNombre: "+info[0] + "\nVersion: "+info[1] +"\nEtiqueta Volumen:"+info[2]+"\nTamano Cluster: "+info[3]+"\nNumero de Clusters: "+info[4]+ "\nNumero Total de Clusters: "+info[5]+"\n\n")

#funcion principal
main()