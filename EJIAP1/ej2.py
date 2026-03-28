import tkinter as tk
from tkinter import messagebox

visitantes = []

def calcular_soles(juegos):
    return juegos * 50

def calcular_descuento(edad, total):
    if edad < 10:
        return total * 0.25
    elif edad <= 17:
        return total * 0.10
    return 0

def abrir_ej2(root):
    ej2 = tk.Toplevel(root)
    ej2.title("Pago en Parque")

    tk.Label(ej2, text="Sistema de Pago en Parque").pack(pady=10)

    frame = tk.Frame(ej2)
    frame.pack(padx=20, pady=10)

    tk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(frame)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Edad:").grid(row=1, column=0, padx=10, pady=5)
    entry_edad = tk.Entry(frame)
    entry_edad.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Juegos usados:").grid(row=2, column=0, padx=10, pady=5)
    entry_juegos = tk.Entry(frame)
    entry_juegos.grid(row=2, column=1, padx=10, pady=5)

    resultado = tk.Label(ej2, text="")
    resultado.pack(pady=10)

    def calcular():
        nombre = entry_nombre.get()
        try:
            edad = int(entry_edad.get())
            juegos = int(entry_juegos.get())
        except ValueError:
            messagebox.showerror("Error", "Datos invalidos")
            return

        total = calcular_soles(juegos)
        descuento = calcular_descuento(edad, total)
        pagar = total - descuento

        visitantes.append((nombre, edad, juegos, pagar))

        resultado.config(text=f"Total a pagar: {pagar:.2f}")

    def mostrar_total():
        if not visitantes:
            messagebox.showinfo("Total", "No hay datos")
            return

        total_suma = sum(v[3] for v in visitantes)

        messagebox.showinfo("Total", f"{total_suma:.2f}")

    btn_frame = tk.Frame(ej2)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Calcular", width=15, command=calcular).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Total Parque", width=15, command=mostrar_total).grid(row=0, column=1, padx=10)

    tk.Button(ej2, text="Cerrar", width=32,
              command=ej2.destroy).pack(pady=10)