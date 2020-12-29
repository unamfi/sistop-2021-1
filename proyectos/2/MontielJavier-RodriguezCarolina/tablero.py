class Tablero:
    def __init__(self):
        self.lugares = [["X","X","X"],["X","X","X"],["X","X","X"]]

    def imprimir_tablero(self):
        for x in range(0,len(self.lugares)):
            for y in range(0,len(self.lugares[x])):
                print(self.lugares[x][y])
            print()
            