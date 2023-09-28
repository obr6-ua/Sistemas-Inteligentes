# Un objeto de esta clase está formado por un número (tamaño) ,
# una posicion , dada por fila y columna y una direccion , que puede ser vertical u horizontal
class Variable:
    def __init__(self, tam , fila , columna , direccion):
        self.tam=tam    
        self.fila = fila
        self.columna = columna
        self.direccion = direccion 
        self.palabra = palabra
            
    def getTam(self):
        return self.tam
    
    def getColumna(self):
        return self.columna

    def getFila(self):
        return self.fila

    def getFila(self):
        return self.direccion

    def setPalabra(self , pal):
        self.palabra = pal