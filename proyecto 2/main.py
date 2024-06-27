from tkinter import filedialog, ttk, messagebox
from tkinter import *
from lexer import Lexer
import webbrowser
from sintactico import Parser

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.construir_interfaz()
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        
    def construir_interfaz(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        frm = ttk.Frame(self.root, padding="10")
        frm.grid(row=0, column=0, sticky="nsew")

        frm.grid_rowconfigure(2, weight=1)  # Ajustar el peso para permitir que el textArea crezca
        frm.grid_columnconfigure(0, weight=1)

        Titulo = ttk.Label(frm, text="Proyecto 2", font=("Arial", 24))
        Titulo.grid(row=0, column=0, pady=20)

        button_frame = ttk.Frame(frm)
        button_frame.grid(row=1, column=0, pady=20, sticky="nsew")

        cargar_btn = ttk.Button(button_frame, text="Cargar Archivo", command=self.cargar_archivo)
        cargar_btn.grid(row=0, column=0, padx=10, pady=10)

        analizar_btn = ttk.Button(button_frame, text="Analizar", command=self.compilar)
        analizar_btn.grid(row=0, column=1, padx=10, pady=10)

        abrir_html_btn = ttk.Button(button_frame, text="Ver Reportes", command=self.abrir_html)
        abrir_html_btn.grid(row=0, column=2, padx=10, pady=10)

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        self.textArea = Text(frm, width=90, height=30)
        self.textArea.grid(row=2, column=0, sticky="nsew")  # Colocar textArea en la fila 2

    def cargar_archivo(self):
        self.textArea.insert(1.0, "")
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.lfp")])
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                self.contenido = f.read()
                self.textArea.delete(1.0, END)
                self.textArea.insert(1.0, self.contenido)  # Insertar el contenido en el textArea

    def compilar(self):
        texto = self.textArea.get("1.0", "end-1c")
        analizador = Lexer(texto)
        lst_tokens = analizador.analizar()
        analizador.generar_reporte_errores()
        analizador.generar_reporte_tokens()
        parser = Parser(lst_tokens)
        parser.parse()
        parser.generar_reporte_errores()

    def abrir_html(self):
        archivo_html = filedialog.askopenfilename(filetypes=[("Archivos HTML", "*.html")])
        if archivo_html:
            webbrowser.open_new_tab(archivo_html)
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo HTML")
    
    def cerrar_ventana(self):
        self.root.quit()  # Finalizar el mainloop de Tkinter
        self.root.destroy()
        
def main():
    root = Tk()
    root.geometry("800x600")  # Ajustar el tamaño de la ventana
    ventana = VentanaPrincipal(root)
    root.mainloop()
    return ventana

if __name__ == "__main__":
    main()
