import tkinter as tk
from tkinter import messagebox

trabajadores = []

def calcular_aumento(sueldo):
    if sueldo < 4000:
        return sueldo * 0.15
    elif sueldo <= 7000:
        return sueldo * 0.10
    else:
        return sueldo * 0.08

def abrir_ej1(root):
    ej1 = tk.Toplevel(root)
    ej1.title("Sistema de Sueldos")
    tk.Label(ej1, text="Sistema de Sueldos").pack(pady=10)

    frame = tk.Frame(ej1)
    frame.pack(padx=20, pady=10)

    tk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(frame)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Sueldo:").grid(row=1, column=0, padx=10, pady=5)
    entry_sueldo = tk.Entry(frame)
    entry_sueldo.grid(row=1, column=1, padx=10, pady=5)

    resultado = tk.Label(ej1, text="")
    resultado.pack(pady=10)

    def calcular():
        nombre = entry_nombre.get()

        try:    
            sueldo = float(entry_sueldo.get())
        except ValueError:
            messagebox.showerror("Error", "Datos invalidos")
            return

        aumento = calcular_aumento(sueldo)
        nuevo = sueldo + aumento

        trabajadores.append((nombre, sueldo, nuevo))

        resultado.config(text=f"Nuevo sueldo: {nuevo:.2f}")

    def mostrar_historial():
        if not trabajadores:
            messagebox.showinfo("Historial", "No hay datos")
            return
        texto = ""

        for t in trabajadores:
            texto += f"{t[0]} - Antes: {t[1]} - Ahora: {t[2]:.2f}\n"

        messagebox.showinfo("Historial", texto)

    btn_frame = tk.Frame(ej1)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Calcular", width=15, command=calcular).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Historial", width=15, command=mostrar_historial).grid(row=0, column=1, padx=10)

    tk.Button(ej1, text="Cerrar", width=32,command=ej1.destroy).pack(pady=10)