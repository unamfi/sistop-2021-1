from timeit import default_timer
ESTADO_LISTO = 1
ESTADO_EN_EJECUCION = 0
ESTADO_EN_BLOQUEO = 1
DURACION_QUANTUM = 0.001
CPU_CONCEDIDO = 1
CPU_NEGADO = 0

class Tiempo:
    def __init__(self, procesos):
        self.procesos = procesos
        self.procesos.sorted(self.procesos, key = lambda x : x.quantum_inicio)
    
class Proceso:
    def __init__(self, quantum_inicio, quantum_duracion, nombre_proceso):
        self.estado = ESTADO_LISTO
        self.quantum_duracion = quantum_duracion * DURACION_QUANTUM
        self.quantum_inicio = quantum_inicio * DURACION_QUANTUM
        self.nombre_proceso = nombre_proceso

    def set_tipo_aviso(self, estado):
        self.estado = estado
    
    def solicitar_cpu():
        if planificador.respuesta() == CPU_CONCEDIDO:

    
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