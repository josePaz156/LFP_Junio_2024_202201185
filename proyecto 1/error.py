class Error:
    def __init__(self, mensaje, columna, fila, valor=""):
        self.mensaje = mensaje
        self.columna = columna
        self.fila = fila
        self.valor = valor

    def __str__(self):
        return f'{self.mensaje} ({self.columna}, {self.fila})'