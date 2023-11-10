class Variable:
    def __init__(self, tam , fila , columna , direccion , dominio=None):
        self.tam = tam    
        self.fila = fila
        self.columna = columna
        self.direccion = direccion 
        self.palabra = ['-'] * tam  # Inicializa con guiones según el tamaño
        self.dominio = dominio
    
    def setDominio(self, dominio):
        self.dominio = dominio
            
    def getTam(self):
        return self.tam
    
    def getColumna(self):
        return self.columna

    def getFila(self):
        return self.fila

    def setPalabra(self, pal):
        if len(pal) == self.tam:
            self.palabra = list(pal)
        else:
            raise ValueError("La palabra no coincide con el tamaño de la variable.")

    def getDireccion(self):
        return self.direccion

    def getPalabra(self):
        return self.palabra
    
    def intersecta_con(self, otra_variable, tablero):
        # No se intersectan si están en la misma dirección
        if self.getDireccion() == otra_variable.getDireccion():
            return None

        # Si 'self' es horizontal y 'otra_variable' es vertical
        if self.getDireccion() == 'H':
            if (self.getFila() >= otra_variable.getFila() and
                self.getFila() < otra_variable.getFila() + otra_variable.getTam() and
                otra_variable.getColumna() >= self.getColumna() and
                otra_variable.getColumna() < self.getColumna() + self.getTam()):
                # El índice de la intersección en 'self' es la columna de 'otra_variable' - columna de 'self'
                # El índice de la intersección en 'otra_variable' es la fila de 'self' - fila de 'otra_variable'
                return (otra_variable.getColumna() - self.getColumna(), self.getFila() - otra_variable.getFila())
        else:
            # Si 'self' es vertical y 'otra_variable' es horizontal
            if (otra_variable.getFila() >= self.getFila() and
                otra_variable.getFila() < self.getFila() + self.getTam() and
                self.getColumna() >= otra_variable.getColumna() and
                self.getColumna() < otra_variable.getColumna() + otra_variable.getTam()):
                return (self.getColumna() - otra_variable.getColumna(), otra_variable.getFila() - self.getFila())

        return None
    