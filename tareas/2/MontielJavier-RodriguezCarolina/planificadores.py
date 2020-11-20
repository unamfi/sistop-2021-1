from time import time

"""
Integrantes
    -Montiel Martínez Luis Javier
    -Rodriguez Davalos Carolina

Descipcion: Programa con el objetivo de implementar los algoritmos de comparacion de planificadores 
"""

"""
Contasntes usadas con el fin de dar una mejor comprension a la logica planeada
"""
DURACION_QUANTUM = 1

ESTADO_LISTO = 0
ESTADO_EJECUCION = 1
ESTADO_BLOQUEADO = 2
ESTADO_FINALIZADO = 3

class Tiempo:
    """
    Clase con el fin de simular el tiempo en la ejecucion de los procesos 

    Se tuvo como objetivo de esta clase respresentar la linea del tiempo el que se movian los procesos
    """

    def __init__(self, procesos):
        '''
        Metodo constructor
        -->Parametros
        -procesos: lista que contiene a los objetos de tipo proceso
        '''
        self.procesos = procesos = sorted(procesos, key = lambda x : x.quantum_inicio,reverse=True)   
        self.procesos_creados = []
    
    def retorna_ordenados(self):
        """
        Metodo encargado de regresar la lista de procesos ordenada con base al quantum de inicio perteneciente a cada uno 
        """
        return self.procesos 

    def corre_tiempo(self):
        """
        Metodo en el cual se inicia la simulacion del tiempo en el que interactuan los procesos

        La logica consistio en considerar el tiempo que ha pasado desde un cierto punto. Para esto se definio la variable 
        tiempo_salida que alamcena el valor retornado por la funcion time() como el punto de partida.

        Continuamos creando un ciclo while infinito en el cual se obtiene una actualizacion del tiempo transcurrirdo y se
        almacena en la variable tiempo_actual. Con estos valores calculamos la diferencia entre tiempo_cero y tiempo_actual
        para conocer el tiempo real que ha estado en ejecucion el programa.

        Posteriormente revisamos con base al tiempo calculado si algun proceso debia iniciar. Realizada esta confirmacion 
        se procede a simular la solicitud por parte del proceso para consumir ejecucion del CPU
        """
        tiempo_salida = 0
        tiempo_actual = 0

        tiempo_salida = time()

        while True:
            tiempo_actual = time()
            tiempo_actual = tiempo_actual - tiempo_salida

            if len(self.procesos) > 0 and tiempo_actual >= self.procesos[0].quantum_inicio:
                elemento = self.procesos.pop()
                self.procesos_creados.append(elemento)
                print('Despertando al proceso ',elemento.nombre_proceso)

            
            if len(self.procesos_creados) > 0:
                for i in self.procesos_creados:
                    if i.estado == ESTADO_FINALIZADO:
                        fin = self.procesos_creados.pop(self.procesos_creados.index(i))

                    i.solicitar_cpu(tiempo_salida)



class Proceso:
    """
    Clase encargada de simular un proceso

    --->Parametros
    -quantum_inicio: Momento en el cual deberia de iniciar el proceso 
    -quantum_duracion: Total de tiempo que debio consumir el proceso recursos en el CPU
    -nombre_proceso: identificador del proceso
    -planificador: referencia al objeto planificador para verificar el acceso al CPU
    """
    def __init__(self, quantum_inicio, quantum_duracion, nombre_proceso,planificador):
        self.estado = ESTADO_LISTO
        self.planificador = planificador
        self.quantum_duracion = quantum_duracion * DURACION_QUANTUM
        self.quantum_inicio = quantum_inicio * DURACION_QUANTUM
        self.nombre_proceso = nombre_proceso
        self.tiempo_respuesta = 0
        self.tiempo_espera = 0
        self.proporcion_penalizacion = 0
        self.tiempo_anterior = 0
        self.tiempo_en_ejecucion = 0
        self.tiempo_bloqueado = 0

    def set_estado(self, estado):
        self.estado = estado
    
    def solicitar_cpu(self,tiempo_salida):
        if self.estado != ESTADO_FINALIZADO:
            self.planificador.revisar_cpu(self)

            tiempo_actual_proceso = time()

            if self.estado == ESTADO_EJECUCION:
                self.tiempo_en_ejecucion = self.tiempo_en_ejecucion + (tiempo_actual_proceso-tiempo_salida)

            elif self.estado == ESTADO_BLOQUEADO:
                #print("bloqueado")
                self.tiempo_bloqueado = self.tiempo_bloqueado + (tiempo_actual_proceso-tiempo_salida)
        
            if (self.tiempo_en_ejecucion >= self.quantum_duracion):
                self.set_estado(ESTADO_FINALIZADO)
                

            self.tiempo_anterior = tiempo_actual_proceso

class Planificador:
    """
    Clase encargada de simular un planificador de corto plazo que implementase los algoritmos de planificacion
    """
    def __init__(self):
        self.proceso_actual = None 

    def revisar_cpu(self,proceso):
        #print("voy a dar acceso")
        if self.proceso_actual == None or self.proceso_actual == proceso:
            self.ejecutando_proceso(proceso)
        else:
            self.detener_proceso(proceso)
    
    def ejecutando_proceso(self,proceso):
        self.proceso_actual = proceso
        proceso.estado = ESTADO_EJECUCION

    def detener_proceso(self,proceso):
        self.proceso_actual = None
        proceso.estado = ESTADO_BLOQUEADO

    
"""
--->Casos de prueba:

Se probo la simulacion con 3 procesos que iniciaban en tiempo cercanos con el fin de probar que estos podian distinguir
el momento en el cual estuviesen en ejecucion o bloqueados.

Los resultados arrojaron inconsistencias a lo esperado. Una posibilidad podria ser el uso de la funcion time() ya que al ser muy variable
genero inconsistencias 

"""
procesos = [] 
planificador = Planificador()
procesos.append(Proceso(0,3,'C',planificador))
procesos.append(Proceso(2,6,'A',planificador))
procesos.append(Proceso(1,5,'B',planificador))
tiempo = Tiempo(procesos)
procesos = tiempo.retorna_ordenados()
tiempo.corre_tiempo()
    
