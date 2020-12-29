import random, threading, time

doctores = 10
paciente = 0

multiplex = threading.Semaphore(doctores)

def llegada_pacientes(paciente, multiplex):

    nivel_urgencia_arreglo = random.choices(range(1,5), weights = [15, 20, 25, 15]) # generamos pacientes con niveles de urgencia ALEATRIOS con DISTINTOS PESOS DE PROBABILIDAD
    nivel_urgencia = int(nivel_urgencia_arreglo[0]) 
    multiplex.acquire()

    if nivel_urgencia == 4:
        adelantar_en_fila(paciente)
        print("Atendiendo al paciente " + str(paciente) +  " con nivel de urgencia MÁS ALTO: 4")
        time.sleep(random.random())
        time.sleep(random.random())
        time.sleep(random.random())
        time.sleep(random.random())
    
    else: 
        print("Atendiendo al paciente " + str(paciente) +  " con nivel de urgencia " + str(nivel_urgencia))
        time.sleep(random.random())
    
    multiplex.release()
    print("Libera al paciente %d" %(paciente))  


def adelantar_en_fila(paciente):
    print("Pasen al paciente " + str(paciente) +  " a urgencias" )

while True:
    paciente = paciente + 1
    threading.Thread(target=llegada_pacientes, args=[paciente, multiplex]).start()
