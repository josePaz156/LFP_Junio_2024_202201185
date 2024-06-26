class Token:
    def __init__(self, tipo, valor, columna, fila):
        self.tipo = tipo
        self.valor = valor
        self.columna = columna
        self.fila = fila

    def __str__(self):
        return f'{self.tipo} {self.valor} ({self.fila}, {self.columna})'