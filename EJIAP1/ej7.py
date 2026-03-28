import tkinter as tk
from tkinter import messagebox

def suma_numeros(n):
    return sum(range(1, n + 1))

def secuencia_sum(n):
    return " + ".join(str(i) for i in range(1, n + 1))

def abrir_ej7(root):
    ej7 = tk.Toplevel(root)
    ej7.title("Suma de Enteros")

    tk.Label(ej7, text="Suma de los primeros n numeros").pack(pady=10)

    frame = tk.Frame(ej7)
    frame.pack(padx=20, pady=10)

    tk.Label(frame, text="Ingrese n:").grid(row=0, column=0, padx=10, pady=5)
    entry_num = tk.Entry(frame)
    entry_num.grid(row=0, column=1, padx=10, pady=5)

    resultado = tk.Label(ej7, text="")
    resultado.pack(pady=10)

    def calcular():
        try:
            num = int(entry_num.get())
            if num <= 0 or num > 999999:
                raise ValueError
        except:
            messagebox.showerror("Error", "Ingrese un numero entero positivo ",
            "(No mayor a 999999)") # Peta pc
            return

        sec = secuencia_sum(num)
        total = suma_numeros(num)

        resultado.config(
            text=f"Secuencia:\n{sec}\nResultado: {total}"
        )

    tk.Button(ej7, text="Calcular", width=20, command=calcular).pack(pady=10)

    tk.Button(ej7, text="Cerrar", width=32, command=ej7.destroy).pack(pady=10)