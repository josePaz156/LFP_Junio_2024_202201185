from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import random
import webbrowser
from analizador import AnalizadorLexico  # Asegúrate de que este import esté aquí, no dentro del método

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.contenido = ""  # Variable de instancia para almacenar el contenido del archivo
        self.imagenes = []  # Lista para almacenar las imágenes generadas
        self.imagen_actual = None  # Variable para almacenar la imagen actualmente mostrada
        self.construir_interfaz()
    
    def construir_interfaz(self):
        # Configurar la raíz para expandirse
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Crear el frame principal
        frm = ttk.Frame(self.root, padding="10")
        frm.grid(row=0, column=0, sticky="nsew")

        # Configurar el frame para expandirse
        frm.grid_rowconfigure(1, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        # Crear el título y centrarlo
        Titulo = ttk.Label(frm, text="Proyecto 1", font=("Arial", 24))
        Titulo.grid(row=0, column=0, pady=20)

        # Crear un frame para los botones
        button_frame = ttk.Frame(frm)
        button_frame.grid(row=1, column=0, pady=20, sticky="nsew")

        # Crear y colocar los botones
        cargar_btn = ttk.Button(button_frame, text="Cargar Archivo", command=self.cargar_archivo)
        cargar_btn.grid(row=0, column=0, padx=10, pady=10)

        analizar_btn = ttk.Button(button_frame, text="Analizar", command=self.compilar)
        analizar_btn.grid(row=0, column=1, padx=10, pady=10)

        abrir_html_btn = ttk.Button(button_frame, text="Ver Reportes", command=self.abrir_html)
        abrir_html_btn.grid(row=0, column=2, padx=10, pady=10)

        # Asegurarse de que los botones se centren
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        # Crear un frame para la selección de imágenes
        self.imagen_frame = ttk.Frame(frm)
        self.imagen_frame.grid(row=2, column=0, pady=20, sticky="nsew")

        # Crear un label para el título de las imágenes
        self.imagen_titulo = ttk.Label(self.imagen_frame, text="Imágenes", font=("Arial", 16))
        self.imagen_titulo.grid(row=0, column=0, padx=10, pady=10)

        # Crear un combobox para seleccionar imágenes
        self.imagen_selector = ttk.Combobox(self.imagen_frame, state='readonly')
        self.imagen_selector.grid(row=0, column=1, padx=10, pady=10)
        self.imagen_selector.bind('<<ComboboxSelected>>', self.mostrar_imagen)

        # Crear un label para mostrar la imagen seleccionada
        self.imagen_label = ttk.Label(self.imagen_frame)
        self.imagen_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Archivos HTML", "*.html"), ("Archivos de código", "*.code")])
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                self.contenido = f.read()
            print(self.contenido)

    def compilar(self):
        print("Compilando...")
        analizador = AnalizadorLexico()
        analizador.analizar(self.contenido)

        # Generar una imagen aleatoria para el ejemplo
        ancho, alto = 100, 100
        imagen = Image.new('RGB', (ancho, alto), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        # Convertir la imagen a un formato que Tkinter pueda usar
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagenes.append(imagen_tk)

        # Actualizar el combobox con la nueva imagen
        self.imagen_selector['values'] = [f'Imagen {i+1}' for i in range(len(self.imagenes))]

    def abrir_html(self):
        archivo_html = filedialog.askopenfilename(filetypes=[("Archivos HTML", "*.html")])
        if archivo_html:
            webbrowser.open_new_tab(archivo_html)
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo HTML")

    def mostrar_imagen(self, event):
        # Obtener el índice de la imagen seleccionada
        seleccion = self.imagen_selector.current()
        if seleccion >= 0:
            self.imagen_actual = self.imagenes[seleccion]
            self.imagen_label.config(image=self.imagen_actual)

def main():
    root = Tk()
    root.geometry("600x400")
    ventana = VentanaPrincipal(root)
    root.mainloop()
    return ventana

if __name__ == "__main__":
    main()

