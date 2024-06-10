from tokens import Token
from error import Error

class AnalizadorLexico:
    def __init__(self):
        self.tokens = []
        self.errores = []

    def analizar(self, contenido):
        self.tokens.clear()
        self.errores.clear()
        palabra = ""
        fila = 1
        columna = 0
        i = 0
        texto = contenido
        
        while i < len(texto):
            char = texto[i]
            columna += 1

            if char.isalnum():
                palabra = ""
                start_col = columna
                while i < len(texto) and texto[i].isalnum():
                    palabra += texto[i]
                    i += 1
                if palabra.lower() in ['nombre', 'nodos', 'conexiones']:
                    self.tokens.append(Token('PALABRA RESERVADA', palabra, start_col, fila))
                elif palabra.isdigit():
                    self.tokens.append(Token('NUMERO', palabra, start_col, fila))
                else:
                    self.tokens.append(Token('PALABRA', palabra, start_col, fila))
                columna += len(palabra) - 1  # Ajustar la columna después del bucle
            elif char == ':':
                self.tokens.append(Token("DOS PUNTOS", char, columna, fila))
            elif char == '.':
                self.tokens.append(Token("PUNTO", char, columna, fila))
            elif char == ';':
                self.tokens.append(Token("PUNTO Y COMA", char, columna, fila))
            elif char == '{':
                self.tokens.append(Token("LLAVE ABRIR", char, columna, fila))
            elif char == '}':
                self.tokens.append(Token("LLAVE CERRAR", char, columna, fila))  
            elif char == '[':
                self.tokens.append(Token("CORCHETE ABRIR", char, columna, fila))
            elif char == ']':
                self.tokens.append(Token("CORCHETE CERRAR", char, columna, fila))
            elif char == '<':
                self.tokens.append(Token("SIGNO MENOR", char, columna, fila))
            elif char == '>':
                self.tokens.append(Token("SIGNO MAYOR", char, columna, fila))
            elif char == ',':
                self.tokens.append(Token("COMA", char, columna, fila))
            elif char == '#':
                self.tokens.append(Token("NUMERAL", char, columna, fila))  
            elif char == '"':
                self.tokens.append(Token("COMILLAS", char, columna, fila))
            elif char == '"':
                self.tokens.append(Token("COMILLAS DOBLES", char, columna, fila))
            elif char == "'":
                self.tokens.append(Token("COMILLAS SIMPLES", char, columna, fila))
            elif char == '-':
                self.tokens.append(Token("MENOS", char, columna, fila))
            elif char in [' ', '\n', '\t', '\r']:
                if char == '\n':
                    fila += 1
                columna = 0
            else:
                self.errores.append(Error(f"Carácter inesperado: {char}", columna, fila))

            i += 1
        self.generar_reporte_tokens()
        self.generar_report_errores()
    
    def generar_reporte_tokens(self):
        contenido = "<!DOCTYPE html>\n<html>\n<head>\n<title>Reporte de Tokens y Errores</title>\n</head>\n<body>\n"
        contenido += "<h1>Reporte de Tokens</h1>\n"
        contenido += "<h2>Tokens</h2>\n"
        contenido += "<table border='1'>\n<tr><th>#</th><th>Tipo</th><th>Valor</th><th>Columna</th><th>Fila</th></tr>\n"
        for i, token in enumerate(self.tokens):
            contenido += f"<tr><td>{i+1}</td><td>{token.tipo}</td><td>{token.valor}</td><td>{token.columna}</td><td>{token.fila}</td></tr>\n"
        contenido += "</table>\n"

        with open("reporte_tokes.html", "w") as f:
            f.write(contenido)

    
    def generar_report_errores(self):
        contenido = "<!DOCTYPE html>\n<html>\n<head>\n<title>Reporte de Tokens y Errores</title>\n</head>\n<body>\n"
        contenido += "<h1>Reporte de Errores</h1>\n"
        contenido += "<h2>Errores</h2>\n"
        contenido += "<table border='1'>\n<tr><th>#</th><th>Mensaje</th><th>Columna</th><th>Fila</th></tr>\n"
        for i, error in enumerate(self.errores):
            contenido += f"<tr><td>{i+1}</td><td>{error.mensaje}</td><td>{error.columna}</td><td>{error.fila}</td></tr>\n"
        contenido += "</table>\n"

        contenido += "</body>\n</html>"

        with open("reporte_errores.html", "w") as f:
            f.write(contenido)
