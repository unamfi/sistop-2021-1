from timeit import default_timer
DURACION_QUANTUM = 1
CPU_CONCEDIDO = 1
CPU_NEGADO = 0
ESTADO_LISTO = 1
ESTADO_FINALIZADO = 0
ESTADO_EJECUCION = 2

class Tiempo:
    def __init__(self, procesos):
        self.procesos = procesos
        self.procesos = sorted(self.procesos, key = lambda x : x.quantum_inicio,reverse=False)
        procesos = self.procesos

    def corre_tiempo(self):
        tiempo_cero = default_timer()
        tiempo_actual = 0
        siguiente_ejecucion = 0
        
        while len(self.procesos) > 0 :
            tiempo_actual = default_timer()
            tiempo_actual -= tiempo_cero
            if tiempo_actual >= procesos[siguiente_ejecucion].quantum_inicio and procesos[siguiente_ejecucion].estado == ESTADO_LISTO:
                procesos[siguiente_ejecucion].solicitar_cpu()
                print("Entre al IF....")
                siguiente_ejecucion += 1
        print("Sali del IF")        

class Proceso:
    def __init__(self, quantum_inicio, quantum_duracion, nombre_proceso):
        self.estado = ESTADO_LISTO
        self.quantum_duracion = quantum_duracion * DURACION_QUANTUM
        self.quantum_inicio = quantum_inicio * DURACION_QUANTUM
        self.nombre_proceso = nombre_proceso
        self.tiempo_respuesta = 0
        self.tiempo_espera = 0
        self.proporcion_penalizacion = 0

    def set_estado(self, estado):
        self.estado = estado
    
    def solicitar_cpu(self):
        tiempo_actual = 0
        tiempo_anterior = 0
        tiempo_en_ejecucion = 0
        tiempo_bloqueado = 0

        self.set_estado(ESTADO_EJECUCION)

        print('inicia el ciclo...')

        tiempo_anterior = default_timer()
        while tiempo_en_ejecucion < self.quantum_duracion:

            tiempo_actual = default_timer()

            if planificador.respuesta(self.nombre_proceso) == CPU_CONCEDIDO:
                tiempo_en_ejecucion += tiempo_actual-tiempo_anterior
            else:
                tiempo_bloqueado += tiempo_actual-tiempo_anterior
            
            tiempo_anterior = tiempo_actual

        print("Finaliza WHILE_PROCESO")  
        self.set_estado(ESTADO_FINALIZADO)

class Planificador:
    def __init__(self,procesos):
        self.procesos = procesos
        self.procesos_en_espera = []
        self.proceso_actual = None 

    def respuesta(self,nombre_proceso):
        if self.proceso_actual == None or self.proceso_actual == nombre_proceso:
            return CPU_CONCEDIDO
        else:
            return CPU_NEGADO
    
    def ejecutando_proceso(self,nombre_proceso):
        self.proceso_actual = nombre_proceso

    def detener_proceso(self,nombre_proceso):
        self.proceso_actual = None

    def FCFS(self):
        procesos = self.procesos[:]
        tiempo = Tiempo(procesos)
        tiempo.corre_tiempo()
        
        while len(self.procesos) > 0:
            indice = self.detector()
            if indice >= 0:
                print("hola")
                self.procesos.pop(indice)
                print("Hice pop")

    
    def detector(self):
        indice = 0
        for x in self.procesos:
            if x.estado == ESTADO_FINALIZADO:
                print("retorne: ",x.nombre_proceso)
                return indice
        indice += 1
        print("No hay nada")
        return -1
    
        
procesos = [] #1,0
B = Proceso(1,5,'B')
procesos.append(B)
A = Proceso(0,3,'A')
procesos.append(A)
C = Proceso(3,2,'C')
procesos.append(C)
planificador = Planificador(procesos)
planificador.FCFS()

        

    
    # def get_tipo_aviso(self):
    


"""
------------->Responsabilidades
===>Tiempo
+el lleva la cuenta del tiempo general
+el avisa a cada proceso cuando iniciar
+saber el tiempo de finalizacion del proceso

-proceso
+solicitar cpu
+detener ejecucion 

-planificador
+avisar cuando iniciar
+avisar cuando detenerse 


------------->metodos
=====> Tiempo
*llamar: Avisa al hilo que sebe de solicitar algo(ya sea pedir CPU o avisar que finaliza)
-tiene 3 colas ordenadas 
una para almacenar q inicio
una para almacenar q fin
una para almacenar a que proceso pertenece

======>Planificador
*respuesta: avisar a proceso que lo llamo si puede o no usar CPU
*checarquantums: ver si cada x q debe de verificar disponibilidad de CPU
-proceso actual: espacio para almacenar que proceso esta en ejecucion
-procesos pendientes: cola para saber el proximo proceso a ejecutar
*colocar proceso actual en ejec
*quitar al proc actual en ejec
*colocar proceso en espera
*quitar proceso en espera
"""

"""
OBJETIVO GENERAL: DEFINIR LA LOGICA DE CADA COSA

objetivo presente: ¿Quien debe empezar?

PENDIETES 
-REVISAR LA LOGICA ACTUAL PARA SPN(,FB,SRR)
-METER CODIGO
-VER COMO OBTENER TABLA DE PROMEDIOS
-ESQUEMA VISUAL

***

"""