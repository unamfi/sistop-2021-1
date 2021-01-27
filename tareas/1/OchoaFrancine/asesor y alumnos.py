import random
import time
import threading

def Asesor():
    
    while True:
        semafo_preguntas.acquire()#se le hizo pregunta

        alumno=alumno_preguntas[0][0]
        pregunta=alumno_preguntas[0][1]
        del alumno_preguntas[0]

        print("Profesor respondio al alumno [",alumno,"] la pregunta numero #",pregunta)

        mutex_atendido.release()#profe se desocupa
        
    
def Alumnos(x):

    semafo_cubiculo.acquire()#Alumno usa silla
    preguntas_finales=random.randint(1,num_preguntas)#Las preguntas que hace el alumno 
  
    print("Alumno [",x,"] ha usado una silla y tiene",preguntas_finales,"preguntas")

    for i in range(1,preguntas_finales+1):
        
        alumno_preguntas.append((x,i))#guarda al num de alumno y num de pregunta en una lista de tuplas

        mutex_atendido.acquire()#maestro esta ocupado

        print("Alumno [",x,"] hace pregunta #",i,"de",preguntas_finales,"preguntas (¿¿??)")

        semafo_preguntas.release()#responde pregunta
        time.sleep(1)

    semafo_cubiculo.release()#alumno i desocupa silla
    print("Profesor le respondio al alumno [",x,"] todas sus",preguntas_finales,"preguntas.")

    
    
alumno_preguntas=[]#lista de tuplas
num_sillas=10 #Numero de sillas del cubiculo
num_preguntas=7 #Preguntas maximas por estudiante
semafo_cubiculo=threading.Semaphore(num_sillas)#Contador sillas
semafo_preguntas=threading.Semaphore(0)
mutex_atendido=threading.Semaphore(1)

print("Profe esta dormido en las", num_sillas, "sillas.")
print("Profe despierta.")

hilo_profe=threading.Thread(target=Asesor)
hilo_profe.start()

alumnos_esperando=random.randint(1,100)
k=1
while k<alumnos_esperando:
    hilo_alumnos=threading.Thread(target=Alumnos,args=[k])
    hilo_alumnos.start()
    k+=1
