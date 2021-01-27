class Ninio:
    def __init__(self,tablero):
        self.tablero = tablero
        self.x = 0
        self.y = 0
        self.puntos = 0

    def objeto_no_tomado(self):
        return False if self.tablero[self.x][self.y] == "X" else False 

    def suma_puntos(self,puntos):
        self.puntos += puntos

    def agarra_objeto(self):
        """
        Variable global que representa que solo uno puede tomar 
        el objeto
        """
        mutex_objeto.acquire()

        if self.objeto_no_tomado():
            self.tablero[self.x][self.y] == "X"
            self.suma_puntos(PUNTOS)

    
