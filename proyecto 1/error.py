class Error:
    def __init__(self, valor, columna, fila):
        self.mensaje = valor
        self.columna = columna
        self.fila = fila