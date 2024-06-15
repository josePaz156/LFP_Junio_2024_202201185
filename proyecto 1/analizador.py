from tokens import Token
from error import Error

class Lexer:
    def __init__(self, entrada) -> None:
        self.entrada = entrada
        self.tokens = []
        self.errores = []

    def isCaracterValido(self, caracter):
        return caracter in [';', '[', ']', ':', ',', '{', '}', '>']

    def estado0(self, caracter, linea, columna):
        if caracter.isalpha():
            return 1
        elif caracter == "-":
            return 2
        elif caracter == "'":
            return 3
        elif self.isCaracterValido(caracter):
            return 4
        elif caracter == ".":
            return 5
        else:
            if ord(caracter) in [32, 10, 9]:  # Espacio, nueva línea, tabulación
                pass
            else:
                self.errores.append(Error("Caracter inválido", columna, linea, caracter))
            return 0

    def analizar(self):
        linea = 1
        columna = 1
        lexema = ""

        estado = 0
        estado_anterior = 0

        for caracter in self.entrada:
            if estado == 0:
                estado = self.estado0(caracter, linea, columna)
                if estado == 0:
                    lexema = ""
                else:
                    lexema += caracter

            elif estado == 1:
                if caracter.isalpha():
                    lexema += caracter
                else:
                    if lexema in ["nombre", "nodos", "conexiones"]:
                        self.tokens.append(Token("Palabra reservada", lexema, columna - len(lexema), linea))
                    else:
                        self.errores.append(Error(f"Palabra no reconocida: {lexema}", columna, linea, lexema))

                    lexema = ""
                    estado = self.estado0(caracter, linea, columna)
                    if estado != 0:
                        lexema += caracter
                    
            elif estado == 2:
                if caracter == ">":
                    lexema += caracter
                    estado = 10
                    estado_anterior = 2
                else:
                    self.errores.append(Error(f"Error en asignación: {lexema}{caracter}", columna, linea, lexema + caracter))
                    estado = 0
                    lexema = ""

            elif estado == 3:
                if caracter == "'":
                    lexema += caracter
                    estado = 10
                    estado_anterior = 3
                elif caracter == "\n":
                    self.errores.append(Error(f"Error en string: {lexema}", columna, linea, lexema))
                    estado = 0
                    lexema = ""
                else:
                    lexema += caracter

            elif estado == 4:
                self.tokens.append(Token("Signo", lexema, columna - len(lexema), linea))
                lexema = ""
                estado = self.estado0(caracter, linea, columna)
                if estado != 0:
                    lexema += caracter

            elif estado == 5:
                if caracter == ".":
                    lexema += caracter
                    if lexema == "...":
                        self.tokens.append(Token("Separacion", lexema, columna, linea))
                        lexema = ""
                        estado = self.estado0(caracter, linea, columna)
                else:
                    self.errores.append(Error(f"Error en separacion: {lexema}{caracter}", columna, linea, lexema + caracter))
                    estado = 0
                    lexema = ""
                    
        
            elif estado == 10:
                if estado_anterior == 2:
                    self.tokens.append(Token("Asignación", lexema, columna - len(lexema), linea))
                elif estado_anterior == 3:
                    self.tokens.append(Token("String", lexema, columna - len(lexema), linea))
                estado_anterior = 0

                lexema = ""
                estado = self.estado0(caracter, linea, columna)
                if estado != 0:
                    lexema += caracter

            if caracter == "\n":
                linea += 1
                columna = 1
            elif caracter == "\t":
                columna += 4
            else:
                columna += 1
    
    def generar_reporte_tokens(self):
        contenido = "<!DOCTYPE html>\n<html>\n<head>\n<title>Reporte de Tokens</title>\n</head>\n<body>\n"
        contenido += "<h1>Reporte de Tokens</h1>\n"
        contenido += "<table border='1'>\n<tr><th>#</th><th>Tipo</th><th>Valor</th><th>Columna</th><th>Fila</th></tr>\n"
        for i, token in enumerate(self.tokens):
            contenido += f"<tr><td>{i+1}</td><td>{token.tipo}</td><td>{token.valor}</td><td>{token.columna}</td><td>{token.fila}</td></tr>\n"
        contenido += "</table>\n</body>\n</html>"

        with open("reporte_tokens.html", "w") as f:
            f.write(contenido)

    def generar_reporte_errores(self):
        contenido = "<!DOCTYPE html>\n<html>\n<head>\n<title>Reporte de Errores</title>\n</head>\n<body>\n"
        contenido += "<h1>Reporte de Errores</h1>\n"
        contenido += "<table border='1'>\n<tr><th>#</th><th>Mensaje</th><th>Columna</th><th>Fila</th><th>Valor</th></tr>\n"
        for i, error in enumerate(self.errores):
            contenido += f"<tr><td>{i+1}</td><td>{error.mensaje}</td><td>{error.columna}</td><td>{error.fila}</td><td>{error.valor}</td></tr>\n"
        contenido += "</table>\n</body>\n</html>"

        with open("reporte_errores.html", "w") as f:
            f.write(contenido)
