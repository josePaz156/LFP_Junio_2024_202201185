from class_token import Token
from class_errorLex import ErrorLex
from sintactico import Parser

class Lexer:
    def __init__(self, entrada):
        self.entrada = entrada
        self.tokens = []
        self.error_lex = []
    
    def estado0(self, caracter, fila, columna):
        if caracter.isalpha() or caracter == "_":  # Acepta letras y guiones bajos
            return 1
        elif caracter == "/":
            return 2
        elif caracter == '"':
            return 3
        elif caracter == "=":
            self.tokens.append(Token("Asignacion", caracter, columna, fila))
            return 0
        elif caracter == ";":
            self.tokens.append(Token("PyC", caracter, columna, fila))
            return 0
        elif caracter == "[":
            self.tokens.append(Token("CorcheteA", caracter, columna, fila))
            return 0
        elif caracter == "]":
            self.tokens.append(Token("CorcheteC", caracter, columna, fila))
            return 0
        elif caracter == "(":
            self.tokens.append(Token("ParentesisA", caracter, columna, fila))
            return 0
        elif caracter == ")":
            self.tokens.append(Token("ParentesisC", caracter, columna, fila))
            return 0
        elif caracter == ",":
            self.tokens.append(Token("Coma", caracter, columna, fila))
            return 0
        elif caracter == ".":
            self.tokens.append(Token("Metodo", caracter, columna, fila))
            return 0
        elif caracter.isdigit():
            return 7  # Estado de número
        else:
            if ord(caracter) in [32, 10, 9]:  # Espacio, nueva línea, tabulación
                return 0
            else:
                self.error_lex.append(ErrorLex("Caracter inválido", columna, fila, caracter))
                return 0
        
    def analizar(self):
        fila = 1
        columna = 1
        lexema = ""

        estado = 0

        i = 0
        while i < len(self.entrada):
            caracter = self.entrada[i]

            if estado == 0:
                estado = self.estado0(caracter, fila, columna)
                if estado == 0:
                    lexema = ""
                else:
                    lexema += caracter

            elif estado == 1:
                if caracter.isalnum() or caracter == "_":  # Acepta letras, números y guiones bajos
                    lexema += caracter
                else:
                    if lexema in ["Array", "new", "save", "sort", "asc"]:
                        self.tokens.append(Token("Palabra Reservada", lexema, columna - len(lexema), fila))
                    elif lexema in ["FALSE", "TRUE"]:
                        self.tokens.append(Token("Boolean", lexema, columna - len(lexema), fila))
                    else:
                        self.tokens.append(Token("Id", lexema, columna - len(lexema), fila))

                    lexema = ""
                    estado = self.estado0(caracter, fila, columna)
                    if estado != 0:
                        lexema += caracter

            elif estado == 2:
                if caracter == "/":
                    estado = 5  # Estado de comentario de una línea
                elif caracter == "*":
                    estado = 6  # Estado de comentario de múltiples líneas
                else:
                    self.error_lex.append(ErrorLex("Caracter inválido", columna, fila, '/'))
                    estado = 0

            elif estado == 3:
                lexema += caracter
                if caracter == '"':
                    self.tokens.append(Token("String", lexema, columna - len(lexema) + 1, fila))
                    estado = 0
                    lexema = ""
                elif caracter == '\n':
                    self.error_lex.append(ErrorLex(f"Error en string: {lexema}", columna, fila, lexema))
                    estado = 0
                    lexema = ""

            elif estado == 5:  # Estado de comentario de una línea
                if caracter == '\n':
                    estado = 0
                    fila += 1
                    columna = 0
                    lexema = ""
                else:
                    # Ignorar comentario de una línea
                    pass

            elif estado == 6:  # Estado de comentario de múltiples líneas
                if caracter == "*" and (i + 1) < len(self.entrada) and self.entrada[i + 1] == "/":
                    estado = 0
                    i += 1  # Saltar el '/' de cierre del comentario
                    lexema = ""
                elif caracter == '\n':
                    fila += 1
                    columna = 0

            elif estado == 7:  # Estado de número
                if caracter.isdigit():
                    lexema += caracter
                elif caracter == ".":
                    lexema += caracter
                    estado = 8  # Estado de número decimal
                else:
                    self.tokens.append(Token("Numero", lexema, columna - len(lexema), fila))
                    lexema = ""
                    estado = self.estado0(caracter, fila, columna)
                    if estado != 0:
                        lexema += caracter

            elif estado == 8:  # Estado de número decimal
                if caracter.isdigit():
                    lexema += caracter
                else:
                    self.tokens.append(Token("Numero Decimal", lexema, columna - len(lexema), fila))
                    lexema = ""
                    estado = self.estado0(caracter, fila, columna)
                    if estado != 0:
                        lexema += caracter

            if caracter == "\n":
                fila += 1
                columna = 1
            elif caracter == "\t":
                columna += 4
            else:
                columna += 1

            i += 1
        
        # Verificar si hay algún lexema pendiente al final de la entrada
        if lexema:
            if estado == 1:
                if lexema in ["Array", "new", "save", "sort", "asc"]:
                    self.tokens.append(Token("Palabra Reservada", lexema, columna - len(lexema), fila))
                elif lexema in ["FALSE", "TRUE"]:
                    self.tokens.append(Token("Boolean", lexema, columna - len(lexema), fila))
                else:
                    self.tokens.append(Token("Id", lexema, columna - len(lexema), fila))
            elif estado == 3:
                self.error_lex.append(ErrorLex(f"Error en string: {lexema}", columna, fila, lexema))
            elif estado == 7:
                self.tokens.append(Token("Numero", lexema, columna - len(lexema), fila))
            elif estado == 8:
                self.tokens.append(Token("Numero Decimal", lexema, columna - len(lexema), fila))
        
        return self.tokens

    def imprimir(self):
        print("=============tokens=============")
        for token in self.tokens:
            print(f"Tokens: {token}")
        print("=============errores=============")
        for error in self.error_lex:
            print(f"Errores: {error}")
