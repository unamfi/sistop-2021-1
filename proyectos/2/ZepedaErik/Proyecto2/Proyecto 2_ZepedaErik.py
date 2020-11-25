#Tareas del hogar
#Librerias
import threading
import time

#Inicializando

SolicitudTarea = 0
RemoverTarea   = 0

realizada      = 0
remover        = 0

realizadaLock  = threading.Lock()
removerLock    = threading.Lock()

# El numero de tareas 10

TareasDisponibles = threading.Semaphore(10)

#Para TareaDom

def TareaDom():

       TareasDisponibles.acquire()
       global realizadaLock
       realizadaLock.acquire()

       global realizada
       realizada = realizada+1
       realizadaLock.release()
       print("Realizada: %d"%(realizada))



#Para Removtarea

def RemovTarea():

       TareasDisponibles.release()
       global removerLock
       removerLock.acquire()

       global remover
       remover = remover+1
       removerLock.release()
       print("Remover: %d"%(remover))


#----------------------------------------
def TareaEntrante():

       while(True):

              time.sleep(4)

              TareaenCamino= threading.Thread(target=TareaDom)
              TareaenCamino.start()

              global SolicitudTarea
              SolicitudTarea = SolicitudTarea+1
              print("Solicitud de Tarea: %d"%(SolicitudTarea))

#-----------------------------------------
def TareaSalida():

       while(True):

              time.sleep(6)

              TareaSaliente = threading.Thread(target=RemovTarea)
              TareaSaliente.start()

              global RemoverTarea
              RemoverTarea = RemoverTarea+1
              print("Remover Tarea: %d"%(RemoverTarea))

#Iniciando Sistema

TareaEntranteThread      = threading.Thread(target=TareaEntrante)
TareaSalidaThread       = threading.Thread(target=TareaSalida)


TareaEntranteThread.start()
TareaSalidaThread.start()
