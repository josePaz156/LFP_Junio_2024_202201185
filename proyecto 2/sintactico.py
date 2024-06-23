from class_errorStx import ErrorStx


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errores = []
    
    def obtener_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None
    
    def coincidir(self, tipo):
        token = self.obtener_token()
        if token and token.tipo == tipo:
            self.pos += 1
            return True
        else:
            if token:
                self.errores.append(f"Error de sintaxis: se esperaba {tipo} pero se encontró {token.tipo} en posición {self.pos}")
            else:
                self.errores.append(f"Error de sintaxis: se esperaba {tipo} pero se encontró fin de entrada")
            return False

    def programa(self):
        while self.obtener_token() is not None:
            if not self.declaracion and not self.metodo():
                break

    def declaracion(self):
        pos_inicial = self.pos
        if self.paralabra_reservada():
            if self.variable():
                if self.coincidir("Asignacion"):
                    if self.expresion():
                        if self.coincidir("Signo") and self.obtener_token().valor == ";":
                            self.pos += 1
                            return True


    def metodo(self):
        pass

    def paralabra_reservada(self):
        return self.coincidir("Palabra Reservada")
    
    def variable(self):
        return self.coincidir("Variable")
    
    def expresion(self):
        if self.cadena() or self.numero() or self.array():
            return True
        return False