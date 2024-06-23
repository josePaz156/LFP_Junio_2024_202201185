class ErrorStx:
    def __init__(self, valor, esperado, fila, columna):
        self.valor = valor 
        self.esperado = esperado
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return f'{self.valro}, {self.esperado}, ({self.fila}, {self.columna})'