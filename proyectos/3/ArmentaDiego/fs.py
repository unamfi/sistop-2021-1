import os,struct
from getpass import getuser

class FileSystem:
    def __init__(self):
        #Se inicializa el sector, el cluster y la imagen de disco  a leer
        self.sector = 512
        self.cluster = self.sector*2
        self.fs = open('fiunamfs.img','r+b')
        self.name_length = 15
        self.start_length = 4
        self.cluster_start = 4

    def listar(self):
        #Ciclo que itera en todos los archivos posibles
        self.fs.seek(0)
        files = []
        for i in range (0,64):
            self.fs.seek(self.cluster+(i*64))
            file_name = self.fs.read(self.name_length)
            if file_name != b'Xx.xXx.xXx.xXx.':
                files.append(file_name)

        for fil in files:
            print(fil.decode())
        self.fs.seek(0)

    def erase(self, erased):

        #Si el usuario busca un archivo mas grande de lo permitido se muestra este mensaje
        if len(erased)>16:
            print("El nombre de archivo no puede ser de esa longitud")
       # Se itera en cada archivo para ver si hay coincidencias con el archivo que se quiere eliminar
        else:
            for i in range(0,64):
                self.fs.seek(self.cluster+(i*64))
                file_name = self.fs.read(self.name_length)
                if file_name.decode().strip() == erased:
                        self.fs.seek(self.cluster+(i*64))
                        #Si el archivo se encuentra se reescribe con la cadena que indica que el espacio ya esta libre
                        self.fs.write(('Xx.xXx.xXx.xXx.').encode())
                        break
            if i == 63:
                print("El archivo no existe")

    # copia desde fiunamfs a el sistema
    def todesktop(self,name,path):
        #se itera para ver si el archivo buscado existe
        for i in range (0,64):
            self.fs.seek(self.cluster+(i*64))
            file_name = self.fs.read(self.name_length)
            self.fs.read(1)
            if file_name.decode().strip() == name:
                #una vez encontrado se copian los datos a un nuevo archivo
                length = struct.unpack('<L',self.fs.read(4))[0]
                start = struct.unpack('<L',self.fs.read(4))[0]
                self.fs.seek(self.cluster*start)
                data = self.fs.read(length)

                write_file = open(path+"/"+file_name.decode().strip(),"wb")
                write_file.write(data)
                write_file.close()
                break
        # si no se encuentra el archivo se envia un mensaje
        if i == 63:
            print("El archivo no existe")



    def defrag(self):
        #ESTA FUNCION NO ELIMINA LOS ESPACIOS VACIOS EN EL DIRECTORIO, LO HACE EN EL ESPACIO DONDE SE ALOJAN LOS ARCHIVOS

        file_start =[] #arreglo para almacenar los clusters de inicio de cada archivo
        file_length = [] #arreglo para almacenar las longitudes de cada archivo
        file_names = [] #arreglo de nombres en directorio

        #elciclo se encarga de guardar los datos de los archivos en el directorio
        for i in range (0,64):
            self.fs.seek(self.cluster+(i*64))
            file_name = self.fs.read(self.name_length)
            self.fs.read(1)
            length = self.fs.read(4)
            start = self.fs.read(4)

            if file_name != b'Xx.xXx.xXx.xXx.':
                
                file_names.append(file_name)
                file_start.append(struct.unpack('<L',start)[0])
                file_length.append(struct.unpack('<L',length)[0])

        #Se ordenan los arreglos de nombre y longitud con base en el cluster de inicio
        file_names_o = [x for y, x in sorted(zip(file_start,file_names))]
        file_length_o = [x for y, x in sorted(zip(file_start,file_length))]
        file_start_o=sorted(file_start)
    
        #Este arreglo se encarga de determinar la nueva posicion con espacio reducido entre los archivos
        ini = 5
    
        file_start_n = []
        file_start_n.append(5)

        for i in range(1,len(file_start_o)):
            if file_length_o[i-1] <= 1024:
                tam = 2
            else:
                tam = (file_length[i-1]//1024)+2
                if file_length_o[i-1]%1024 == 0:
                    tam -= 1
            file_start_n.append(file_start_n[i-1]+tam)

        #se reescriben los datos en orden para evitar la perdida de informacion

        for i in range(0,len(file_start_n)):
            self.fs.seek(file_start_o[i]*self.cluster)
            data = self.fs.read(file_length_o[i])
            self.fs.seek(file_start_n[i]*self.cluster)
            self.fs.write(data)
        #se actualiza la informacion en el directorio
        for j in range(0,len(file_names_o)):
            for i in range (0,64):
                self.fs.seek(self.cluster+(i*64))
                file_name = self.fs.read(self.name_length)
                self.fs.read(5)
                if file_name == file_names_o[j]:
                    self.fs.write(struct.pack('<L',file_start_n[j]))

    # metodo para la interfaz de usuario, simplemente imprime las opciones disponibles y permite la seleccion mediante un input
    def UI(self):
        user = getuser()
        while True:
            print("Lista de comandos:")
            print("--------rm <nombre_archivo>: Borrar")
            print("--------defrag: Desfrangmentar")
            print("--------cp <nombre_archivo> <ruta_archivo>: Copiar de Fiunamfs a sistema")
            print("--------ls: Listar archivos")
            print("------------------------------------------------------------------------")
            print("\n")
            print("\n")
            ent = input("Ingrese un comando: ")
            print("\n")
            print("\n")
            ents = ent.split()
            opciones = ['rm', 'defrag', 'cp' ,'ls']
            if ents[0] in opciones:
                if ents[0] == 'rm':
                    if len(ents)!=2:
                        print("La sentencia requiere de un argumentos")
                    else:
                        print("Eliminar \n")
                        self.erase(ents[1])
                        print("\n")
                        print("\n")
                        print("------------------------------------------------------------------------")
                elif ents[0] == 'ls':
                    if len(ents)!=1:
                        print("La sentencia no requiere argumentos")
                    else:
                        print("Lista de archivos: \n")
                        self.listar()
                        print("\n")
                        print("\n")
                        print("------------------------------------------------------------------------")
                elif ents[0] == 'defrag':
                    if len(ents)!=1:
                        print("La sentencia no requiere argumentos")
                    else:
                        print("Defragmentando \n")
                        print("\n")
                        print("\n")
                        print("------------------------------------------------------------------------")
                        self.defrag()
                else:
                    if len(ents)!=3:
                        print("La sentencia requiere de dos argumentos")
                    else:
                        print("Copiando desde FiunamFS a Sistema \n")
                        self.todesktop(ents[1],ents[2])
                        print("\n")
                        print("\n")
                        print("------------------------------------------------------------------------")

            else:
                print("Comando invalido")

if __name__ == '__main__':
    FS = FileSystem()
    FS.UI()
