import threading
import time
import random

class Elevador(threading.Thread):
    
    def __init__(self, piso_actual, piso_destino, capacidad):
        threading.Thread.__init__(self)
        self.pa = piso_actual
        self.pd = piso_destino
        self.cap = capacidad
        self.llamadas = []
        self.cap = threading.Semaphore(capacidad)

    def subir(self):
        self.pa+=1
        time.sleep(2)
        print("Elevador Subiendo")

    def bajar(self):
        self.pa-=1
        time.sleep(2)
        print("Elevador Bajando")

    def run(self):
        time.sleep(5)
        while(len(self.llamadas) != 0):
            self.pd = self.llamadas[0]
            print("Elevador piso destino ",self.pd)
            print("Elevador piso actual ",self.pa)
            while(self.pa != self.pd):
                if(self.pa < self.pd):
                    self.subir()
                elif(self.pa > self.pd):
                    self.bajar()
            self.llamadas.pop(0)
        
class Persona(threading.Thread):

    def __init__(self, piso_actual, piso_destino, identity, elevador):
        threading.Thread.__init__(self)
        self.pa = piso_actual
        self.pd = piso_destino
        self.id = identity
        self.e = elevador
        self.inside = False

    def pedir(self):
        self.e.pd = self.pa

    def viajar(self):
        check2 = False
        for i in self.e.llamadas:
            if(i == self.pa):
                check2 = True
        if (check2 == False):
            self.e.llamadas.append(self.pa)
        while (self.pd != self.e.pa):
            time.sleep(1)
            print(self.id, "Viajando en elevador")
        print(self.id, "Baja del elevador")
        self.e.cap.release()

    def esperar(self):
        while (self.e.pa != self.pa):
            time.sleep(1)
           # print(self.id, "Esperando elevador")

    def run(self):
        while(self.inside == False):
            check = False
            for i in self.e.llamadas:
                if(i == self.pa):
                    check = True
            if (check == False):
                tlock.acquire()
                self.e.llamadas.append(self.pa)
                tlock.release()
            self.esperar()
            if(self.e.cap.acquire()):
                print(self.id," Entra al elevador")
                self.e.cap.acquire()
                self.inside == True
                self.viajar()
        print(self.id, " LLego a su destino")

tlock = threading.Lock()
def main():

    #primera parte inicializar personas en cada piso 

    e1 = Elevador(1,1,5)
    personas = []
    for i in range(10):
        a = random.randint(1,5)
        b = random.randint(1,5)
        while(b == a):
            b = random.randint(1,5)
        personas.append(Persona(a,b,i,e1))

    e1.start()
    for i in personas:
        print(i.id,i.pa,i.pd)
        i.start()
    
    
    
        

if __name__ == "__main__":
    main()

