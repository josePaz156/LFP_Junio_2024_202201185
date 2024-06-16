from tokens import Token
from error import Error
import graphviz
import tkinter as tk
from tkinter import filedialog

class Lexer:
    def __init__(self, entrada) -> None:
        self.entrada = entrada
        self.tokens = []
        self.grafos = []
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
        contador_errores = 0

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
    
    def seleccionar_ruta(self):
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal de Tkinter
        ruta = filedialog.askdirectory(title="Selecciona la carpeta donde se guardarán los reportes")
        return ruta + '/' if ruta else ''

    def generar_reporte_tokens(self):
        ruta = self.seleccionar_ruta()
        if not ruta:
            print("No se seleccionó una carpeta. Operación cancelada.")
            return

        contenido = "<!DOCTYPE html>\n<html>\n<head>\n<title>Reporte de Tokens</title>\n</head>\n<body>\n"
        contenido += "<h1>Reporte de Tokens</h1>\n"
        contenido += "<table border='1'>\n<tr><th>#</th><th>Tipo</th><th>Valor</th><th>Columna</th><th>Fila</th></tr>\n"
        for i, token in enumerate(self.tokens):
            contenido += f"<tr><td>{i+1}</td><td>{token.tipo}</td><td>{token.valor}</td><td>{token.columna}</td><td>{token.fila}</td></tr>\n"
        contenido += "</table>\n</body>\n</html>"

        with open(f"{ruta}reporte_tokens.html", "w") as f:
            f.write(contenido)

    def generar_reporte_errores(self):
        ruta = self.seleccionar_ruta()
        if not ruta:
            print("No se seleccionó una carpeta. Operación cancelada.")
            return

        contenido = "<!DOCTYPE html>\n<html>\n<head>\n<title>Reporte de Errores</title>\n</head>\n<body>\n"
        contenido += "<h1>Reporte de Errores</h1>\n"
        contenido += "<table border='1'>\n<tr><th>#</th><th>Mensaje</th><th>Columna</th><th>Fila</th><th>Valor</th></tr>\n"
        for i, error in enumerate(self.errores):
            contenido += f"<tr><td>{i+1}</td><td>{error.mensaje}</td><td>{error.columna}</td><td>{error.fila}</td><td>{error.valor}</td></tr>\n"
        contenido += "</table>\n</body>\n</html>"

        with open(f"{ruta}reporte_errores.html", "w") as f:
            f.write(contenido)

    def generar_imagenes(self):
        # Verificar todos los tokens
        print("Lista completa de tokens:")
        for t in self.tokens:
            print(t)

        nombres_archivos = []
        grafo = None
        nodos = {}
        conexiones = []

        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            print(f"Token actual: {token}")

            if token.tipo == "Palabra reservada" and token.valor == "nombre":
                if i + 2 < len(self.tokens) and self.tokens[i + 1].tipo == "Asignación" and self.tokens[i + 2].tipo == "String":
                    nombre_grafo = self.tokens[i + 2].valor.strip("'")
                    grafo = graphviz.Digraph(nombre_grafo)
                    i += 3
                    print(f"Nombre del grafo: {nombre_grafo}")

            elif token.tipo == "Palabra reservada" and token.valor == "nodos":
                if i + 2 < len(self.tokens) and self.tokens[i + 1].tipo == "Asignación" and self.tokens[i + 2].tipo == "Signo" and self.tokens[i + 2].valor == "[":
                    i += 3
                    while i < len(self.tokens) and not (self.tokens[i].tipo == "Signo" and self.tokens[i].valor == ";"):
                        if i + 3 < len(self.tokens) and self.tokens[i].tipo == "String" and self.tokens[i + 1].tipo == "Signo" and self.tokens[i + 1].valor == ":" and self.tokens[i + 2].tipo == "String":
                            nodo_id = self.tokens[i].valor.strip("'")
                            nodo_label = self.tokens[i + 2].valor.strip("'")
                            nodos[nodo_id] = nodo_label
                            grafo.node(nodo_id, label=nodo_label)
                            i += 4
                            print(f"Agregado nodo: {nodo_id} con etiqueta: {nodo_label}")
                        elif self.tokens[i].tipo == "Signo" and self.tokens[i].valor == ",":
                            i += 1
                        else:
                            i += 1

            elif token.tipo == "Palabra reservada" and token.valor == "conexiones":
                print("Encontrado token de conexiones")
                if i + 2 < len(self.tokens) and self.tokens[i + 1].tipo == "Asignación" and self.tokens[i + 2].valor == "[":
                    i += 3
                    while i < len(self.tokens) and not (self.tokens[i].tipo == "Signo" and self.tokens[i].valor == ";"):
                        if i + 5 < len(self.tokens) and self.tokens[i].valor == "{" and self.tokens[i + 1].tipo == "String" and self.tokens[i + 2].valor == ">" and self.tokens[i + 3].tipo == "String" and self.tokens[i + 4].valor == "}":
                            origen = self.tokens[i + 1].valor.strip("'")
                            destino = self.tokens[i + 3].valor.strip("'")
                            conexiones.append((origen, destino))
                            grafo.edge(origen, destino)
                            i += 5
                            print(f"Agregada conexión: {origen} -> {destino}")
                        elif self.tokens[i].tipo == "Signo" and self.tokens[i].valor == ",":
                            i += 1
                        else:
                            i += 1

            elif token.tipo == "Separacion":
                if grafo:
                    grafo.render(f'grafo_{grafo.name}', format='png', cleanup=True)
                    print(f"Grafo {grafo.name} generado.")
                    nombre_archivo = f'grafo_{grafo.name}.png'
                    nombres_archivos.append(nombre_archivo)
                grafo = None
                nodos = {}
                conexiones = []
                i += 1
            else:
                i += 1

        if grafo:
            grafo.render(f'grafo_{grafo.name}', format='png', cleanup=True)
            nombre_archivo = f'grafo_{grafo.name}.png'
            nombres_archivos.append(nombre_archivo)
        else:
            print("No se ha definido el nombre del grafo.")

        return nombres_archivos