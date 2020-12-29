from random import choice, randint
import tablero

class Payaso: 
    def __init__(self, ninios, tablero):
      self.objetos = ["A","B","C"]
      self.ninios = ninios
      self.tablero = tablero

    def elegir_objeto(self):
        return choice(self.objetos)
    
    def elegir_coordenadas(self, rango_inicial,rango_final):
        return randint(rango_inicial,rango_final)
    
    def pasar_coordenadas(self, coordenada_x, coordenada_y):
        for ninio in self.ninios:
            ninio.x = coordenada_x
            ninio.y = coordenada_y

    def pon_tablero(self):
        objeto = self.elegir_objeto()
        objeto_x = self.elegir_coordenadas(0,2)
        objeto_y = self.elegir_coordenadas(0,2)
        self.pasar_coordenadas(objeto_x,objeto_y)
        self.tablero.lugares[objeto_x][objeto_y] = objeto



    