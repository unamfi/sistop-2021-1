import random
import time
import threading


def SantaClaus():
    despertar_santa.acquire()

    print('Sata descansa mientras no sea despertado')

    while True:
        if regalo_entregado==False:
            print('Santa ayuda a elfos')
            print('Santa a dormir')
            despertar_santa.acquire()
        else:
            print('Hay %d renos, se entregaran regalos'%renos_usados)
            break
    print('Terminado')
 

def Elfos(i):
    global num_elfos
    print ('Elfo %d, trabajando'%i)

    num_problemas=random.randint(1,30)
    time.sleep(num_problemas)

    print('Elfo %d tiene problema'%i)

    mutex_elfos.acquire()
    num_elfos=num_elfos+1

    print('Hay %d elfos con problemas'% num_elfos)

    if num_elfos==elfos_problematicos:
        for j in range (1,elfos_problematicos):
            elfo_ayudado.release()
        num_elfos=0
        print('Hay 3 elfos, Santa sera despertado.')

        despertar_santa.release()

    mutex_elfos.release()
    elfo_ayudado.acquire()


def Renos(i):
    global num_renos,regalo_entregado
    print('Reno %d se va a la playa.'%(i) )

    playa=random.randint(1,30)
    time.sleep(playa)

    print('Reno %d, ha vuelto'%i)
    
    mutex_renos.acquire()
    num_renos=num_renos+1

    if num_renos==renos_usados:

        for j in range (1,renos_usados):
            semafo_renos.release()
        num_renos=0

    mutex_renos.release()
    semafo_renos.acquire()
    regalo_entregado=True
    despertar_santa.release()



#Elfos
elfos= 200
elfos_problematicos= 3
num_elfos=0
elfo_ayudado=threading.Semaphore(0)
mutex_elfos=threading.Semaphore(1)

#Renos
renos= 9
renos_usados= 9
num_renos=0
semafo_renos=threading.Semaphore(0)
mutex_renos=threading.Semaphore(1)

regalo_entregado = False
despertar_santa=threading.Semaphore(0)

#Hilo santa
hilo=threading.Thread(target=SantaClaus)  
hilo.start()

#Hilos Renos
k=0
while k<renos:
    hilo=threading.Thread(target = Renos, args = [k])
    hilo.start()
    k=k+1

#Hilos Elfos
l=0
while l<elfos:
    hilo=threading.Thread(target = Elfos, args = [l])
    hilo.start()
    l=l+1
