from class_token import Token
from class_funcionalidad import Arreglo, Ordenamiento, Guardar
import csv

class Parser():
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.arreglos = []
        self.ordenados = []
        self.guardados = []
        self.tokens.append(Token("EOF", "$", -1, -1))


    def recuperar_modo_panico(self, valor_token_de_sincronizacion):
        while self.tokens[0].valor != "$":
            token = self.tokens.pop(0)
            if token.tipo == valor_token_de_sincronizacion:
                break

    def parse(self):
        self.inicio()
        self.funcionalidad()
    
    #<inicio> ::= <instrucciones>
    def inicio(self):
        #crean nodo <inicio>
        #crean nodo <instrucciones>
        #nodo <inicio> apunta a nodo <instrucciones>
        self.instrucciones()

    #<instrucciones> ::= <instruccion> <instrucciones>
    #                  | ε
    def instrucciones(self):
        if self.tokens[0].valor == "$":
            return
        self.instruccion()
        self.instrucciones()

    #<instruccion> ::= <declaracion>
    #                | <instruccionID>
    def instruccion(self):
        if self.tokens[0].valor == "Array":
            self.declaracion()
            return
        else:
            self.instruccionID()
            return

    #<declaracion> ::= tk_palabraArray tk_id tk_igual tk_palabraNew tk_palabraArray tk_corcheteA <listaElementos> tk_corcheteC tk_PyC
    def declaracion(self):
        if self.tokens[0].valor == "Array":
            self.tokens.pop(0)
            if self.tokens[0].tipo == "Id":
                id = self.tokens.pop(0)
                if self.tokens[0].tipo == "Asignacion":
                    self.tokens.pop(0)
                    if self.tokens[0].valor == "new":
                        self.tokens.pop(0)
                        if self.tokens[0].valor == "Array":
                            self.tokens.pop(0)
                            if self.tokens[0].tipo == "CorcheteA":
                                self.tokens.pop(0)
                                elementos = self.listaElementos()
                                if self.tokens[0].tipo == "CorcheteC":
                                    self.tokens.pop(0)
                                    if self.tokens[0].tipo == "PyC":
                                        self.tokens.pop(0)
                                        #Aquí se debe manejar la instruccion
                                        print("ID: ", id.valor)
                                        print("Lista: ")
                                        new_arreglo = []
                                        for e in elementos:
                                            new_arreglo.append(e.valor)
                                            print(e.valor)
                                        self.arreglos.append(Arreglo(id.valor, new_arreglo))
                                        return
                                        #Ya tenemos el id del nuevo arreglo y el valor (el arreglo como tal)
                                    else:
                                        print(f"Error sintactico: Se esperaba un ; en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
                                else:
                                    print(f"Error sintactico: Se esperaba un ] en la fila {self.tokens[0].fila}")
                            else:
                                print(f"Error sintactico: Se esperaba un [ en la fila {self.tokens[0].fila}")
                        else:
                            print(f"Error sintactico: Se esperaba la palabra Array en la fila {self.tokens[0].fila}")
                    else:
                        print(f"Error sintactico: Se esperaba la palabra New en la fila {self.tokens[0].fila}")
                else:
                    print(f"Error sintactico: Se esperaba un = en la fila {self.tokens[0].fila}")
            else: 
                print(f"Error sintactico: Se esperava un id en la fina {self.tokens[0].fila}")
        else:
            print(f"Error sintactico: Se esperava Array en la fina {self.tokens[0].fila}")
        self.recuperar_modo_panico("PyC")

    #<listaElementos> ::= <elemento> <masElementos>
    #                   | epsilon
    def listaElementos(self):
        item = self.elemento()
        if item == None:
            return []
        lista = [item]
        masElementos = self.mas_elementos()
        lista.extend(masElementos)
        return lista
    
    #<masElementos> ::= tk_coma <tk_elemento> <masElementos>
    #                 | epsilon
    def mas_elementos(self):
        if self.tokens[0].tipo == "Coma":
            self.tokens.pop(0)
            item = self.elemento()
            if item == None:
                return []
            lista = [item]
            lista.extend(self.mas_elementos())
            return lista
        else:
            return []

    # <elemento> ::= tk_entero
    #              | tk_decimal
    def elemento(self):
        if self.tokens[0].tipo == "Numero" or self.tokens[0].tipo == "Numero Decimal":
            return self.tokens.pop(0)
        elif self.tokens[0].tipo == "String":
            return self.tokens.pop(0)
        else:
            return None
        
    #<instruccionID> ::= tk_id tk_punto <accionArreglo>
    def instruccionID(self):
        if self.tokens[0].tipo == "Id":
            id = self.tokens.pop(0)
            if self.tokens[0].tipo == "Metodo":
                self.tokens.pop(0)
                resultado = self.accionArreglo()
                if resultado is not None:
                    if resultado[0] == "sort":
                        self.ordenados.append(Ordenamiento(id.valor, resultado[1]))
                        print("La instrucción es un ordenamiento para el arreglo", id.valor, "con asc =", resultado[1])
                        return
                    elif resultado[0] == "save":
                        self.guardados.append(Guardar(id.valor, resultado[1]))
                        print("La instrucción es guardar el arreglo", id.valor, "en el path", resultado[1])
                        return
                else:
                    print(f"Error sintactico: Acción de arreglo inválida en la fila {self.tokens[0].fila}")
            else:
                print(f"Error sintactico: Se esperaba un . en la fila {self.tokens[0].fila}")
                # Recuperación de errores en modo pánico
                self.recuperar_modo_panico("PyC")
        else:
            print(f"Error sintactico: Se esperaba un id en la fila {self.tokens[0].fila}")
        self.recuperar_modo_panico("PyC")


    
    #<accionArreglo> ::= ordenamiento>
    #                  | <guardar>
    def accionArreglo(self):
        if self.tokens[0].valor == "sort":
            return ["sort", self.ordenamiento()]
        elif self.tokens[0].valor == "save":
            return self.guardar()
        else:
            print(f"Error sintactico: Acción de arreglo inválida en la fila {self.tokens[0].fila}")
            self.recuperar_modo_panico("PyC")
            return None


    #<ordenamiento> ::= tk_palabraSort tk_parentesisAbre tk_palabraAsc tk_igual tk_booleano tk_parentesisCierra tk_PyC
    def ordenamiento(self):
        if self.tokens[0].valor == "sort":
            self.tokens.pop(0)
            if self.tokens[0].tipo == "ParentesisA":
                self.tokens.pop(0)
                if self.tokens[0].valor == "asc":
                    self.tokens.pop(0)
                    if self.tokens[0].tipo == "Asignacion":
                        self.tokens.pop(0)
                        if self.tokens[0].tipo == "Boolean":
                            asc = self.tokens.pop(0)
                            if self.tokens[0].tipo == "ParentesisC":
                                self.tokens.pop(0)
                                if self.tokens[0].tipo == "PyC":
                                    self.tokens.pop(0)
                                    # Aquí se debe manejar la instrucción
                                    return asc.valor
                                else:
                                    print(f"Error sintactico: Se esperaba un ; en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
                            else:
                                print(f"Error sintactico: Se esperaba un ) en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
                        else:
                            print(f"Error sintactico: Se esperaba TRUE/FALSE en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
                    else:
                        print(f"Error sintactico: Se esperaba un = en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
                else:
                    print(f"Error sintactico: Se esperaba ASC en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
            else:
                print(f"Error sintactico: Se esperaba un ( en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
        else:
            print(f"Error sintactico: Se esperaba SORT en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
        self.recuperar_modo_panico("PyC")
        return None

    #<guardar> ::= tk_palabraSave tk_parentesisAbre tk_string tk_parentesisCierra tk_PyC
    def guardar(self):
        if self.tokens[0].valor == "save":
            self.tokens.pop(0)
            if self.tokens[0].tipo == "ParentesisA":
                self.tokens.pop(0)
                if self.tokens[0].tipo == "String":
                    path = self.tokens.pop(0)
                    if self.tokens[0].tipo == "ParentesisC":
                        self.tokens.pop(0)
                        if self.tokens[0].tipo == "PyC":
                            self.tokens.pop(0)
                            # Aquí se debe manejar la instrucción
                            return ["save", path.valor]
                        else:
                            print(f"Error sintactico: Se esperaba ; en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
                    else:
                        print(f"Error sintactico: Se esperaba ) en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
                else:
                    print(f"Error sintactico: Se esperaba un string en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
            else:
                print(f"Error sintactico: Se esperaba ( en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
        else:
            print(f"Error sintactico: Se esperaba SAVE en la fila {self.tokens[0].fila}, pero se obtuvo {self.tokens[0].valor}")
        self.recuperar_modo_panico("PyC")
        return None
    
    def es_numero(self, cadena):
        try:
            float(cadena)
            return True
        except ValueError:
            return False

    def funcionalidad(self):

        for i in self.ordenados:
            for arreglo in self.arreglos:
                if i.id == arreglo.id:
                    if self.es_numero(arreglo.items[0]):
                        if i.valor == "TRUE":
                            arreglo.items.sort(key=float)
                            print("Ordenar asendentemente")
                        elif i.valor == "FALSE":
                            arreglo.items.sort(key=float, reverse=True)
                            print("Ordenar desendentemente")
                    
                    else:
                        # Si todos los elementos son cadenas
                        if i.valor == "TRUE":
                            arreglo.items.sort()
                            print("Ordenar ascendentemente:", arreglo.items)
                        elif i.valor == "FALSE":
                            arreglo.items.sort(reverse=True)
                            print("Ordenar descendentemente:", arreglo.items)
        
        for i in self.guardados:
            for arreglo in self.arreglos:
                if i.id == arreglo.id:
                    filename = f"{i.valor.replace('\"', '')}"
                    with open(filename, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        for item in arreglo.items:
                            writer.writerow([item])
                    print(f"Archivo {filename} guardado con éxito.")
        