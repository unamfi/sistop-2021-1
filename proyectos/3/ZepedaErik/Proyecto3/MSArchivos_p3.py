
# Ejecución: 
#	pip3 install -r requirements.txt
#	micro_sistema_archivos -h
#	Ejemplo para listar contenido: micro_sistema_archivos -l fiunamfs.img 
#								   micro_sistema_archivos fiunamfs.img --list  

import argparse
import binascii
import struct
import os

#############################################################################################################################################################################################
#   CONSIDERACIONES DEL PROGRAMA
#
#	Sistema de archivos cabe en diskette => floppy device de 1440 kb (1.44M)
#	Las cadenas de texto deben ser de los caracateres en ASCII 8-bit
#	En las estructuras del disco los enteros de 32 bits se representan en little endian
#	Tam de sector: 512 bytes
#	Tam cluster: 2 sectores => 1024 bytes
#	No maneja tabla de particiones
#	Es directamente un volumen 
#	Maneja unicamente un directorio plano
#	Cluster #0 es el superbloque
#	El sistema de archivos es de asignación contigua => toda la info de los archivos esta en el directorio [clusters 1 al 4] 
#	El directorio está ubicado en los clusters 1 a 4 
#		=> cada entrada del directorio mide 64 bytes
#		=> las entradas no utilizadas se identifican con el nombre de archivo: Xx.xXx.xXx.xXx.
#	Después del directorio (clusters a partir del 5) es espacio de datos => => se refiere a que el contenido de cada archivo está en los bytes de los clusters a partir del 5to.
##############################################################################################################################################################################################


def addOptions():
    """
    Función para agregar las opciones al script e instrucciones de ejecucion
    Recibe: 
    	void
    Devuelve:
    	opts => namespace: valores asignados a las variables que se requieren para su ejecucion y que se 
    			leen como argumentos del script
    """
    parser = argparse.ArgumentParser(allow_abbrev=False, add_help=False,
        description='Programa para listar cotenido, extraer, agregar o eliminar archivos de la imagen de un sistema de archivos.')
    parser.add_argument('imagen_fs', type=str, help='imagen de sistema de archivos')

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Muestra este mensaje de ayuda')
    parser.add_argument('-i', '--info', dest='info', action='store_true', help='Muestra informacion general de la imagen del sistema de archivos \'imagen_fs\'')

    parser.add_argument('-l', '--list', dest='list', action='store_true', help='lista los contenidos del directorio')
    parser.add_argument('-g', '--get', dest='getf', action='store', help='copia uno de los archivos de dentro del \'imagen_fs\' hacia tu sistema')
    parser.add_argument('-p', '--put', dest='putf', action='store', help='copia un archivo de tu computadora hacia tu \'imagen_fs\'')
    parser.add_argument('-r', '--remove', dest='rmf', action='store', help='elimina un archivo del \'imagen_fs\'')
    # parser.add_argument('-d', '--defragment', dest='defragment', action='store', help='Elimina un archivo del [FiUnamFS]')


    opts = parser.parse_args()
    return opts 


def read_fs(imagen_fs):
	"""
	Funcion para leer el contenido de la imagen del sistema de archivos que recibe como argumento.
	Recibe: 
		imagen_fs => str: nombre de la imagen del FS
	Devuelve: 
		hex_data => list: representacion en hexadecimal del contenido de la imagen del FS
	"""
	with open(imagen_fs, 'rb') as fs:
		data = fs.read()
		hex_data = [ hex(byte).split('x')[-1].zfill(2) for byte in data ]
	return hex_data

def get_info_cluster0(bytes_data):
	"""
	Función para obtener información del superbloque (cluster #0 de 1024 bytes) de la imagen analizada.
	Recibe: 
		bytes_data => list: lista de bytes leidos de la imagen que se analiza
	Devuelve: 
		fs_name, fs_version, fs_label, fs_clustersize_BE, 
		fs_numclusters_dir_BE, fs_numclusters_complete_BE 	
					=> tuple: tupla con la informacion interpretada de los bytes del superbloque
	"""
	fs_name = binascii.unhexlify(''.join(bytes_data[0:8]))  # Byte 0-8: nombre del sistema de archivos
															# Byte 8 => es un bad char: "\x00"
	#fs_name = fs_name.decode().replace('\x00','')  # se elimina bad char \x00 del nombre y se decodifican los bytes
	fs_name = fs_name.decode()  # se decodifican los bytes

	#fs_version = binascii.unhexlify(''.join(bytes_data[10:14])).decode().replace('\x00','')  # Byte 10-13: version de la implementacion
	fs_version = binascii.unhexlify(''.join(bytes_data[10:13])).decode()  # Byte 10-13: version de la implementacion
																 		  # Byte 13 => es un bad char: "\x00"
	#fs_label = binascii.unhexlify(''.join(bytes_data[20:36])).decode().replace('\x00','')  # Byte 20-35: etiqueta del volumen
	fs_label = binascii.unhexlify(''.join(bytes_data[20:35])).decode()    # Byte 20-35: etiqueta del volumen
																		  # Byte 35 => es un bad char: "\x00"
	fs_clustersize = binascii.unhexlify(''.join(bytes_data[40:44]))       # Byte 40-43: tamanio del cluster en bytes
	# como están representados en formato little endian, debemos pasarlo primero a big endian y despues hacer la conversión a decimal
	fs_clustersize_BE = struct.unpack("<L", fs_clustersize)[0]            # Convierte el valor fs_clustersize (little endian) a formato big endian en decimal
	
	fs_numclusters_dir = binascii.unhexlify(''.join(bytes_data[44:48]))   # Byte 44-47: numero de clusters que mide el directorio
	fs_numclusters_dir_BE = struct.unpack("<L", fs_numclusters_dir)[0]
	
	fs_numclusters_complete = binascii.unhexlify(''.join(bytes_data[48:52])) # Byte 48-51: numero de clusters que mide la unidad completa
	fs_numclusters_complete_BE = struct.unpack("<L", fs_numclusters_complete)[0]
	
	return fs_name, fs_version, fs_label, fs_clustersize_BE, fs_numclusters_dir_BE, fs_numclusters_complete_BE

def list_dir_content(bytes_data, tam_dir_entry=64):
	"""
	Función para listar los contenidos de los directorio [ubicados en el cluster 1-4] y
	donde cada entrada del directorio es de 64 bytes
	Recibe: 
		bytes_data => list: lista de bytes leidos de la imagen que se analiza [correspondientes a los cluster 
						    donde se ubican los directorios]
		tam_dir_entry => int: entero que indica el tamaño de cada entrada de directorio [por defecto: 64]
	Devuelve:
		content_dir => dict: diccionario cuya "llave" es una entrada del directorio y su "valor" es una tupla que representa 
							 la informacion de cada archivo existente (y tambien entradas no utilizadas) 
							 en los clusters donde se ubica el directorio
	"""
	
	# Agrupa las N entradas del directorio de 64 bytes:
	num_dir_entries = int(len(bytes_data) / tam_dir_entry)
	dir_entry = {}
	content_dir = {}
	initial_byte = 0
	# Asigna los 64 bytes corrrespondientes a cada una de las entradas del directorio
	for i in range(0, num_dir_entries):
		final_byte = initial_byte + tam_dir_entry
		dir_entry[i] = bytes_data[initial_byte:final_byte]
		initial_byte = final_byte
	# Interpreta los valores hexadecimales del sistema de archivos correspondiente a cada archivo y los asginamos en un diccionario
	
	for i in range(0, num_dir_entries):
		# Byte 0-14: nombre del archivo => compuestos de cualquier caracter dentro del ASCII de 7 bits
		filename = binascii.unhexlify(''.join(dir_entry[i][0:15])).decode()
		# Byte 15: tipo de archivo => el sistema de archivos actual unicamente soporta archivos regulares, 
		# por lo tanto su valor siempre debe ser el caracter "-" [0x2d => hex | 45 => dec]
		filetype = binascii.unhexlify(''.join(dir_entry[i][15])).decode()
		# Byte 16-19: tamaño del archivo en bytes
		filesize = binascii.unhexlify(''.join(dir_entry[i][16:20]))
		filesize_BE = struct.unpack("<L", filesize)[0]
		# Byte 20-23: cluster inicial
		initial_cluster = binascii.unhexlify(''.join(dir_entry[i][20:24]))
		initial_cluster_BE = struct.unpack("<L", initial_cluster)[0]
		# Byte 24-37: hora y fecha de creación del archivo [AAAAMMDDHHMMSS]
		creation_date = format_date(dir_entry[i][24:38])
		# Byte 38-51: hora y fecha de última modificación del archivo [AAAAMMDDHHMMSS]
		modification_date = format_date(dir_entry[i][38:52])
		# Byte 52-63: espacio no utilizado => reservado para expansion futura?
		# unused_space = binascii.unhexlify(''.join(dir_entry[i][52:64]))
		# unused_space_BE = struct.unpack("<L", unused_space)[0]
		content_dir[i] = filename, filetype, filesize_BE, initial_cluster_BE, creation_date, modification_date
	return content_dir

def format_date(bytes_date):
	"""
	Función para formatear la fecha en una forma fácil y legible
	Recibe: 
		date => str: hora y fecha en formato: "AAAAMMDDHHMMSS"
	Devuelve: 
		format_datetime => str: hora y fecha con formato: "AAAA-MM-DD HH:MM:SS"
	"""
	date = binascii.unhexlify(''.join(bytes_date)).decode()
	return f'{date[0:4]}-{date[4:6]}-{date[6:8]} {date[8:10]}:{date[10:12]}:{date[12:14]}'

def copy_to_local_machine(getFilename, bytes_data):
	"""
	Función para copiar un archivo existente dentro de la imagen del FS hacia nuestra maquina
	Recibe: 
		getFilename => str: nombre del archivo que se va a copiar
		bytes_data => list: lista de bytes que le corresponden al contenido del archivo que se va a copiar
	Devuelve:
		Escribe el contenido del getFilename (archivo a copiar) en un arcihvo de nuestra maquina, donde el 
			nombre del nuevo archivo es el mismo: getFilename
	"""
	file_content = binascii.unhexlify(''.join(bytes_data))
	with open(getFilename, "wb") as dest_file:
		dest_file.write(file_content)

def copy_from_local_machine(localfile):
	"""
	"""

def delete_file_from_fs(filename):
	"""
	"""

def defragment_fs(img):
	"""
	"""

def print_info_superblock(values):
	"""
	Funcion para mostrar en salida estandar la informacion general del sistema de archivos leido desde la imagenFS.
	Recibe:
		values => tuple: tupla con los valores de la informacion general del sistema de archivos 
	Devuelve:
		Muestra en salida estandar la informacion extraida del cluster0
	"""
	fs_name, fs_version, fs_label, fs_clustersize_BE, fs_numclusters_dir_BE, fs_numclusters_complete_BE = values
	print(f'\nNombre del sistema de archivos: {fs_name}')
	print(f'Version de la implementacion: {fs_version}')
	print(f'Etiqueta del volumen: {fs_label}')
	print(f'Tamanio del cluster: {fs_clustersize_BE} bytes')
	print(f'Numero de clusters que mide el directorio: {fs_numclusters_dir_BE}')
	print(f'Numero de clusters que mide la unidad completa: {fs_numclusters_complete_BE}\n')

def print_list_dir_content(values):
	"""
	Funcion para mostrar en salida estandar en el listado del contenido hacia el directorio [ubicado del cluster 1 al 4].
	Recibe:
		values => dict: diccionario cuya "llave" es una entrada del directorio y su "valor" es una tupla que representa 
						la informacion de cada archivo existente (y tambien entradas no utilizadas) 
						en los clusters donde se ubica el directorio.
			La tupla tiene los valores: filename, filetype, filesize, initial_cluster, creation_date, modification_date 
	Devuelve:
		Muestra en salida estandar la informacion asociada a cada entrada del directorio
	"""
	for i in range(0, len(values)):
		filename, filetype, filesize, initial_cluster, creation_date, modification_date = values[i]
		if filename != 'Xx.xXx.xXx.xXx.':
			print(f'\nNombre del archivo: {filename}')
			print(f'Tipo de archivo: {filetype}')
			print(f'Tamanio del archivo: {filesize} bytes')
			print(f'Cluster inicial: {initial_cluster}')
			print(f'Hora y fecha de creación del archivo: {creation_date}')
			print(f'Hora y fecha de última modificación del archivo: {modification_date}\n')
			#print(f'Espacio no utilizado: {unused_space}')
			
if __name__ == '__main__':
	args = addOptions()
	hexdata_fs = read_fs(args.imagen_fs)
	info_cluster0 = get_info_cluster0(hexdata_fs[:1024])  # el cluster 0 es desde el byte 0 hasta el byte 1023
	fs_numclusters_dir = info_cluster0[4]
	cluster_size = 1024
	dir_content = {}
	initial_byte = 1024  # byte donde comienza el segundo cluster
	for i in range(1, fs_numclusters_dir + 1):
		final_byte = initial_byte + cluster_size
		info_dir_content = list_dir_content(hexdata_fs[initial_byte:final_byte])
		dir_content[i] = info_dir_content
		initial_byte = final_byte

	# Realiza la accion de la opcion elegida mediante los argumentos del script
	if args.info:
		print_info_superblock(info_cluster0)
	elif args.list:
		for i in range(1, fs_numclusters_dir + 1):
			print_list_dir_content(dir_content[i])
	elif args.getf:
		getFilename = args.getf
		file_exists = False
		for i in range(1, fs_numclusters_dir + 1):
			for dir_entry, info_file in dir_content[i].items():
				filename = info_file[0].strip()  # eliminamos espacios en blanco al inicio o final del nombre de archivo
				if getFilename == filename:
					file_exists = True
					filesize, initial_cluster = info_file[2], info_file[3]
					byte_begin_file = initial_cluster * cluster_size    # el byte inicial del archivo solicitado empieza a partir del intial_cluster
																		# que obtuvimos al analizar la informacion de cada entrada del directorio, 
																		# por lo que se multiplica por el tamanio fijo del cluster_size
					byte_end_file = byte_begin_file + filesize  # el byte final del archivo es: el byte inicial + el tamanio (num de bytes) del
																# archivo que representan el final de su contenido y que se obtuvo de la informacion 
																# de cada entrada del directorio
					try:
						copy_to_local_machine(getFilename, hexdata_fs[byte_begin_file:byte_end_file])
						print(f"\nEl archivo '{getFilename}' de '{args.imagen_fs}' se copio en: '{os.getcwd()}/{filename}'\n")
					except:
						print(f"\nOcurrio un error. No se pudo copiar el archivo {getFilename} a nuestro equipo\n")
					break
			if file_exists: break  # si el archivo ya se encontro, no es necesario seguir buscando en los otros clusters del directorio
		if not file_exists: print(f"\nEl archivo '{getFilename}' NO existe en '{args.imagen_fs}'\n")
