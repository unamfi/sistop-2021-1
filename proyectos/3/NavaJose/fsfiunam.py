#Se importan las librerias necesarias para el funcionamiento del programa
import struct
import os, os.path
#Variable que controla el ciclo que ejecuta el programa
ejecutando = True

class Fiunamfs:
    def __init__(self):
        #Se abre el sistema de archivos en modo lectura 
        self.fiunamfs = open("fiunamfs.img", "r+b")
        #Variable que permitira el manejar los nuumeros representados como valores de 32 bits en formato little endian
        #obtenidos de la lectura defragmentos del sistema con ayuda de la funcion unpack() 
        a_32 = struct.Struct("<L")
        #Fijamos la posicion de lectura en el rango que se encuentra el nombre y obtenemos el mismo
        self.fiunamfs.seek(0)
        self.nombreFS = self.fiunamfs.read(8).decode()
        #Comprobamos que se trate del archivo correcto
        if self.nombreFS != "FiUnamFS":
            #Si el valor obtenido como nombre del archivo .img no corresponde con el sistema de archivos
            #Se cierra el sistema y se lanza un error
            print("Error: El archivo .img no corresponde al sistema de archivos")
            self.fiunamfs.close()
            exit(-1)
        else:
            #Se fijan las posiciones donde se tiene grabado
            #la version, la etiqueda de volumen, el tamaño del cluster
            #el tamaño del cluster, el numero de clusters
            #y el numero de clusters que mide la unidad completa
            #Y se recuperan dichos valores con la funcion read y unpack() 
            #para el manejo de los valores hexadecimales
            self.fiunamfs.seek(10)           
            self.versionFS = self.fiunamfs.read(4).decode()         
            self.fiunamfs.seek(21)
            self.etiquetaFS = self.fiunamfs.read(15).decode() 
            self.fiunamfs.seek(40)
            self.tamanioCFS = a_32.unpack(self.fiunamfs.read(4))[0]
            self.fiunamfs.seek(44)
            self.numCDFS = a_32.unpack(self.fiunamfs.read(4))[0]
            self.fiunamfs.seek(48)
            self.numCFS = a_32.unpack(self.fiunamfs.read(4))[0]


 
    #Funcion que recupera todos los archivos que esten drento del sistema
    #Y posteriormente los imprime con formato de color
    def listarArchivos(self):
        archivos = []
        #Se buscan los archivos qdentro de los directorios del sistema
        #La entrada deñ direcotio mide 64 bytes  
        for i in range(0,64):
            posicion = self.tamanioCFS+(i*64)
            #Se fija la posicion en la cual se puede encontrar un archivo y se recupera el nombre de este
            self.fiunamfs.seek(posicion)
            archivo = self.fiunamfs.read(15)
            #Se guardara el nombre del archivo siempre y cuando no se trate de 
            #Una entrada no utilizada del directorio
            if archivo != b'Xx.xXx.xXx.xXx.':
                archivos.append(archivo)
        #Se imprimen todos los archivos encontrados
        for i in archivos:
            print("\x1b[1;36m"+i.decode()+"\033[0;m")



    #Funcion que copia un archivo de la computadora al sistema de arcivos
    def copiaAfs(self,archivo):
        #Se obtiene el tamaño de la cadena ingresada
        #y se recupera la ruta del archivo que se quiere copiar a FiUNAMFS
        final=len(archivo)
        rutaArchivo = archivo[3:final]
        print(rutaArchivo)
        #Se debe comprobar que existe un archivo con el nombre recibido y en la ruta especificada
        if(os.path.isfile(rutaArchivo)):
            print("Se encontro el archivo")
        else:
            print("ERROR no el arhivo no existe en la ruta especificada")

    #Funcion que elimina un archivo dentro de FiUNAMFS
    def borrar(self,comando):
        a_32 = struct.Struct("<L")
        #Se obtiene el tamaño de la cadena ingresada
        #y se recupera la ruta del archivo que se quiere copiar a FiUNAMFS
        final=len(comando)
        nombre = comando[3:final]
        #Primero se debe de validar si el archivo se encuentra dentro de FiUNAMFS
        for i in range(0,64):
            ubicacion = self.tamanioCFS+(i*64)
            #Se fija la posicion en la cual se puede encontrar un archivo y se recupera el nombre de este
            self.fiunamfs.seek(ubicacion)
            #Se leen 15 caracteres puesto que el nombre del archivo va del 0 al 14
            nombreArchivo = self.fiunamfs.read(15)
            #Si ambos nombres coinciden se procede al borrado
            if(nombre == nombreArchivo.decode()[0:final-3]):
                #Se obtiene la ubicacion del archivo y se coloca en la misma
                estaEn = self.tamanioCFS+(i*64)
                self.fiunamfs.seek(estaEn)
                #Se sobre escribe con el nombre que llevan las entradas no utilizadas por default
                #Y se borra el registro de fecha y hora
                self.fiunamfs.write(b'Xx.xXx.xXx.xXx.')
                self.fiunamfs.seek(ubicacion+15)
                self.fiunamfs.write(a_32.pack(0000))
                self.fiunamfs.seek(ubicacion+24)
                self.fiunamfs.write("0000000000000000000000000000".encode())
                
                break
            i = i+1
            #Si se recorre todo el directorio sin encontrar coincidencia
            #Se lanza el error
            if(i == 64):
                print("Error el archivo ",nombre," no existe en FiUNAMFS")

    #Funcion que se ejecuta mientras se haga uso del programa
    def sistema(self):
        #Bucle que se ejecutara hasta que se ingrese el comando que salga del sistema de archivos
        while ejecutando:
            #Se esperara un comando como entrada con un formato similar al de una terminal
            comando = input("josenava@FiUNAMFS:~$ ")
            #Dependiendo del valor de la entrada se ejecutaran diferentes acciones
            if(comando == "ls"):
                #Se accede a la funcion que lista los archivos que se encientran dentro del sistema
                self.listarArchivos()
            if(comando[0:2] == "cp"):
                #Si el inicio de la cadena es cp se accede a la funcion que copia un archivo
                #de la computadora al sistema de archivos
                self.copiaAfs(comando)
            if(comando[0:2] == "rm"):
                #Se accede a la funcion que borra un archivo dentro del sistema
                self.borrar(comando)
            if(comando == "clear"):
                #Se limpia la pantalla
                os.system("clear")
            if(comando == "exit"):
                #Se cierra el sistema de archivos, se limpia la pantalla y finaliza la ejecucion del programa
                self.fiunamfs.close()
                os.system('clear')
                return False
            if(comando == "help"):
                #En caso de solicitar ayuda, se muestran los comandos que admite el programa
                #Con un formato similar a cuando se ingresa el mismo comando en un sistema UNIX como Ubuntu
                print("")
                print("")
                print(self.nombreFS,"",self.versionFS)
                print("Estos comandos se definen internamente. Escriba ""help"" para ver esta lista.")
                print("")
                print("")
                print("\x1b[1;33m"+"ls"+"\033[0;m""                             Listar archivos")
                print("\x1b[1;33m"+"cp"+"\033[0;m""\x1b[1;35m"+" [ruta del archivo]"+"\033[0;m""          Copiar archivos de la computadora a FiUNAMFS")
                print("\x1b[1;33m"+"rm"+"\033[0;m""\x1b[1;35m"+" nombre del archivo"+"\033[0;m""          Borrar archivos")
                print("\x1b[1;33m"+"clear"+"\033[0;m""                          Limpiar pantalla")
                print("\x1b[1;33m"+"exit"+"\033[0;m""                           Salir")
                print("")

    

    #Funcion en la que inicia el programa, en esta se muestra un mensaje de bienvenida
    def arranque(self):
            #Limpiamos la pantalla por darle un toque estetico
            os.system('clear')
            print("\x1b[1;32m"+"+-----------------------------------------------------------------+")
            print("+                                                                 +")
            print("+    @@@@@@    @@   @@ @@@    @@  @@@@  @@@   @@@ @@@@@@ @@@@@    +")
            print("+    @@     @@ @@   @@ @@ @   @@ @@  @@ @@ @ @ @@ @@    @@        +")
            print("+    @@@@      @@   @@ @@  @  @@ @@@@@@ @@  @  @@ @@@@   @@@@     +")
            print("+    @@     @@ @@   @@ @@   @ @@ @@  @@ @@     @@ @@        @@    +")
            print("+    @@     @@  @@@@   @@    @@@ @@  @@ @@     @@ @@    @@@@@     +")
            print("+                                                                 +")
            print("+-----------------------------------------------------------------+"+"\033[0;m")
            #Una vez mostrada la pantalla de bienvenida se llama a la funcion principal del programa
            self.sistema()
    
if __name__ == '__main__':
    sistemaArchivos = Fiunamfs()
    sistemaArchivos.arranque()