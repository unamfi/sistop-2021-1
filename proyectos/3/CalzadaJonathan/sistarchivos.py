# -*- encoding: Latin-1
"""
Created on Thu Jan 8 15:37:48 2021

@author: Jonathan
"""

import os.path # Se utiliza para asignar rutas en el sistema 
from math import ceil#Se utiliza ceil para asignar el valor del cluster 



#Cuerpo del programa
if os.path.exists("fiunam.img"):# verificar si la ruta especificada existe
	pass
else:
	print("Creamos Sistema de Archivos")
	file=open("fiunam.img","w")
	file.write("FiUnamFS")
	file.seek(10)
	file.write("0.4")
	file.seek(20)
	file.write("Sistema Archivo")
	file.seek(40)
	file.write("01024")
	file.seek(47)
	file.write("04")
	file.seek(52)
	file.write("00001440")
	file.seek(1024)
	for i in range(64):
		file.write("AQUI_NO_VA_NADA")
		file.seek(file.tell()+1)
		file.write("00000000")
		file.seek(file.tell()+1)
		file.write("00000")
		file.seek(file.tell()+1)
		file.write("00000000000000")
		file.seek(file.tell()+1)
		file.write("00000000000000")
		file.seek(file.tell()+4)
	file.close()
 

#Funcion para agregar archivo de la computadora al sistema de archivos
def agregar(nombre):
	size=os.path.getsize(nombre)# os.path verificamos la ruta existente
	cluster_ant=0
	tamanio=0
	cluster=ceil(size/1024)
	file=open("fiunam.img","r+")
	file.seek(0,os.SEEK_SET)
	file.seek(1024)
	aux=file.read(15)
	while aux != 'AQUI_NO_VA_NADA':
		file.seek(file.tell()+49)
		aux=file.read(15)
	#Si es el primer archivo en directorio
	if file.tell()==1039:#Se verifica si es el primer archivo dentro del sistema de archivos
		cluster_act=4
		ahora=file.tell()
	else:
		ahora=file.tell()
		anterior=file.seek(file.tell()-63)
		tamanio=file.read(8)
		file.seek(file.tell()+1)
		cluster_ant=file.read(5)
		cluster_act=ceil(int(tamanio)/1024)+int(cluster_ant)-1
		file.seek(file.tell()+49)
	if (1440-(cluster_act+cluster))>0:
		temp=15-len(nombre)
		if(temp>0):
			file.seek(file.tell()-15)
			for i in range(temp):
				file.write(" ")
			file.write(nombre)			
		else:
			return ("El archivo tiene un nombre demasiado grande")
		#Escribimos tamanio archivo nuevo
		file.seek(file.tell()+1)
		temp=8-len(str(size))
		for i in range(temp):
			file.write("0")
		file.write(str(size))
		#Escribimos cluster inicial
		file.seek(file.tell()+1)
		temp=5-len(str(cluster_act+cluster))
		for i in range(temp):
			file.write("0")
		file.write(str(cluster_act+cluster))

#Funcion que copia archivo del sistema a la computadora
def copy(nombre):
	size=0
	cluster=0
	name=nombre
	copia=""
	while name==nombre:
		print("Introduce el nombre del nuevo archivo")
		name=input()
	file=open("fiunam.img","r+",encoding="Latin-1")
	file.seek(1024)
	aux=file.read(15)
	while aux.replace(" ","")!=nombre:
		file.seek(file.tell()+49)
		aux=file.read(15)
	file.seek(file.tell()+1)
	size=int(file.read(8))
	file.seek(file.tell()+1)
	cluster=int(file.read(5))	
	file.seek(cluster*1024)
	copia=file.read(size)
	archivo=open(""+name,"w",encoding="Latin-1")
	archivo.write(copia)
	archivo.close()
	file.close()
	return("Archivo copiado con exito")

#Muestra el contenido del FS
def listar():
	file=open("fiUnam.img","r")
	file.seek(1024)
	for i in range(64):
		archivoAux=file.read(15)
		if archivoAux != 'AQUI_NO_VA_NADA':
			print(archivoAux.replace(' ',''))
		file.seek(file.tell()+49)
	file.close()

#Esta funcion elimina del sistema de archivos
def eliminar(nombre):#Recibe el nombre del archivo a eliminar
	file=open("fiUnam.img","r+")
	file.seek(1024)
	for i in range(64):
		archivoAux=file.read(15)
		if archivoAux.replace(' ','') == nombre:
			#Recupera informacion necesaria del archivo a eliminar
			file.seek(file.tell()+1)
			tam=int(file.read(8))
			file.seek(file.tell()+1)
			ini=int(file.read(5))
			#Borra del directorio
			file.seek(file.tell()-30)
			file.write("AQUI_NO_VA_NADA")
			file.seek(file.tell()+1)
			file.write("00000000")
			file.seek(file.tell()+1)
			file.write("00000")
			file.seek(file.tell()+1)
			file.write("00000000000000")
			file.seek(file.tell()+1)
			file.write("00000000000000")
			file.seek(file.tell()+4)
			file.close()
			#Limpia la memoria
			limpiar(ini,ceil(tam/1024))#El tamaño se envia en clusters
			return 'Se borro el archivo'
		else:
			file.seek(file.tell()+49)
	file.close()
	return 'No se encontro el archivo'

#Esta funcion limpia la memoria con el inicio y la magnitud.(EStara en clusters)
def limpiar(ini,tam):
	file=open("fiUnam.img","r+")
	file.seek(ini*1024)
	vacio='\x00'
	for i in range(0,tam):
		file.write(vacio*1024)
	file.close()


a=True
while a==True:
   
    print("_____________________ ")
    print("|1. Listar contenido.|")
    print("|2. añadir archivo.|")
    print("|3. Copiar archivo a su computadora. |")
    print("|4. Eliminar archivo.   |")#CHECK
    print("|5. Salir.              |")
    print("| Seleccione un opcion: |")
    print("                    ")
    op=int(input("Ingrese una opcion: \n"))
    if op == 1:
        listar()
    elif op == 2:
        print("añadir archivo")
        arg=input("Ingrese el nombre del archivo :")
        agregar(arg)
        print("Añadido")
    elif op == 3:
        print("Copiar del FiUnamFs a la computadora")
        arg=input("Ingrese el nombre del archivo :")
        copy(arg)
        print("copiado")
    elif op == 4:
        arg=input("Ingrese el nombre del archivo :")
        eliminar(arg)
        print("Eliminado")
    elif op == 5:
        a= False
    
