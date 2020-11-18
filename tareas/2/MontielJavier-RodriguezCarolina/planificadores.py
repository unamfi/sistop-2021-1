from timeit import default_timer
import threading
import time

def carga(id_proceso,tiempo_duracion):
    tiempo_inicial = default_timer()
    tiempo_en_ejecucion = 0
    tiempo_final = 0

    print('iniciando ciclo...')
    
    while(tiempo_en_ejecucion < tiempo_duracion):
        tiempo_final = default_timer()
        tiempo_en_ejecucion = tiempo_final - tiempo_inicial
    
    print('Fin del proceso',id_proceso)
    print("Tiempo total", tiempo_en_ejecucion, "segundos")

hilo_prueba = threading.Thread(target = carga,args = []) 

