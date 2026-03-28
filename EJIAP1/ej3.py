import tkinter as tk
from tkinter import messagebox

compras = []

def validar_mes(mes):
    meses_validos = [
        "enero","febrero","marzo","abril","mayo","junio",
        "julio","agosto","septiembre","octubre","noviembre","diciembre"
    ]
    return mes.lower() in meses_validos

def calcular_descuento(mes, importe):
    mes = mes.lower()

    if mes == "octubre":
        return importe * 0.15
    elif mes == "diciembre":
        return importe * 0.20
    elif mes == "julio":
        return importe * 0.10
    return 0

def abrir_ej3(root):
    ej3 = tk.Toplevel(root)
    ej3.title("Descuentos por Mes")

    tk.Label(ej3, text="Sistema de Descuentos").pack(pady=10)

    frame = tk.Frame(ej3)
    frame.pack(padx=20, pady=10)

    tk.Label(frame, text="Cliente:").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(frame)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Mes:").grid(row=1, column=0, padx=10, pady=5)
    entry_mes = tk.Entry(frame)
    entry_mes.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Importe:").grid(row=2, column=0, padx=10, pady=5)
    entry_importe = tk.Entry(frame)
    entry_importe.grid(row=2, column=1, padx=10, pady=5)

    resultado = tk.Label(ej3, text="", font=("Arial", 11))
    resultado.pack(pady=10)

    def calcular():
        nombre = entry_nombre.get()
        mes = entry_mes.get()

        if not validar_mes(mes):
            messagebox.showerror("Error", "Mes invalido")
            return

        try:
            importe = float(entry_importe.get())
        except:
            messagebox.showerror("Error", "Importe invalido")
            return

        descuento = calcular_descuento(mes, importe)
        total = importe - descuento

        compras.append((nombre, mes, importe, total))

        resultado.config(text=f"Total a pagar: {total:.2f}")

    def mostrar_total():
        if not compras:
            messagebox.showinfo("Total", "No hay datos")
            return

        total_dia = sum(c[3] for c in compras)

        messagebox.showinfo("Total vendido", f"{total_dia:.2f}")

    btn_frame = tk.Frame(ej3)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Calcular", width=15, command=calcular).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Total del dia", width=15, command=mostrar_total).grid(row=0, column=1, padx=10)

    tk.Button(ej3, text="Cerrar", width=32,command=ej3.destroy).pack(pady=10)