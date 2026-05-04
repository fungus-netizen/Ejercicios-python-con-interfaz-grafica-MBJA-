import customtkinter as ctk
import numpy as np # para generar puntos de la grafica
import matplotlib
matplotlib.use('TkAgg') # para usar matplotlib con tkinter 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # para mostrar la grafica en tkinter (widget)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Nomas copie y pegue de la act2 c:
def mostrar_grafica(frame, fig):
    fig.set_size_inches(8.5, 4.5)

    # ajusta margenes
    # ya le sufri con margenes, ya NO
    fig.subplots_adjust(
        left=0.08,
        right=0.97,
        top=0.90,
        bottom=0.20
    )

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()

    widget = canvas.get_tk_widget()
    widget.pack(expand=True, fill="both")

# logica para la funcion
def graficar_funcion(frame, m, b):
    # puntos para graficar
    x = np.linspace(0, 10, 100) # rango de x (0-10)
    y = m * x + b # funcion lineal

    # graficar (crear figura y ejes)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    # lineas de ejes
    ax.axhline(0) 
    ax.axvline(0)

    # titulo y etiquetas
    ax.set_title(f"f(x) = {m}x + {b}") 
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    mostrar_grafica(frame, fig)

# App
class App(ctk.CTkFrame):
    # constructor
    def __init__(self, master=None):
        # hijo de CTkFrame
        super().__init__(master)

        # container para cambiar solo el contenido (NO todo el root (tkinter manda error si destruyes el root))
        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, fill="both")

        self.crear_menu()

    # limpiar solo el contenedor
    def limpiar_contenedor(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # menu principal
    def crear_menu(self):
        self.limpiar_contenedor()

        titulo = ctk.CTkLabel(self.container, text="Funciones lineales")
        titulo.pack(pady=10)

        frame_inputs = ctk.CTkFrame(self.container) 
        frame_inputs.pack(pady=10)

        # input m
        label_m = ctk.CTkLabel(frame_inputs, text="Pendiente (m):")
        label_m.grid(row=0, column=0, padx=5, pady=5)

        self.entry_m = ctk.CTkEntry(frame_inputs) 
        self.entry_m.grid(row=0, column=1, padx=5, pady=5)

        # input b
        label_b = ctk.CTkLabel(frame_inputs, text="Termino independiente (b):")
        label_b.grid(row=1, column=0, padx=5, pady=5)

        self.entry_b = ctk.CTkEntry(frame_inputs)
        self.entry_b.grid(row=1, column=1, padx=5, pady=5)

        # mensaje error
        self.label_error = ctk.CTkLabel(self.container, text="", text_color="red")
        self.label_error.pack()
        
        btn_graficar = ctk.CTkButton(frame_inputs, text="Graficar", command=self.abrir_grafica)
        btn_graficar.grid(row=2, column=0, columnspan=2, padx=5, pady=20, sticky="ew")

    # abrir grafica
    def abrir_grafica(self):
        m = self.entry_m.get()
        b = self.entry_b.get()

        # validaciones de datos
        try:
            # float -> es numero (con decimales)
            m = float(m)
            b = float(b)

            # dif de 0 (es lineal }, no constante)
            if m == 0:
                self.label_error.configure(text="Error: la pendiente no puede ser 0")
                return

            self.label_error.configure(text="")
        except:
            self.label_error.configure(text="Error: ingresa valores validos")
            return

        self.limpiar_contenedor()

        top = ctk.CTkFrame(self.container)
        top.pack(fill="x", pady=10)

        volver = ctk.CTkButton(top, text="Volver", command=self.crear_menu)
        volver.pack(side="left", padx=10)

        frame = ctk.CTkFrame(self.container)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        graficar_funcion(frame, m, b)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")

    def on_closing(): # tk manda error si cierras la ventana sin esta funcion (no se destruye root)
        root.quit() # aparece al cerrar al cerrar el programa sin cerrar la ventana
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing) #  .protocol es una funcion de tkinter para manejar eventos de cierre de ventana

    # lo peor es que bgerror sigue mandando error :/
    app = App(master=root)
    app.pack(expand=True, fill="both")

    root.mainloop()
