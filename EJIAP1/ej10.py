import tkinter as tk
from tkinter import messagebox

trabajadores = []

def calcular_pago(hora_normales, pago_hora, hora_extras, hijos):
    pago_normal = hora_normales * pago_hora
    pago_extra = hora_extras * (pago_hora * 1.5)
    bono = hijos * 0.5
    total = pago_normal + pago_extra + bono

    return pago_normal, pago_extra, bono, total

def abrir_ej10(root):
    ej10 = tk.Toplevel(root)
    ej10.title("Pago de Trabajadores")

    tk.Label(ej10, text="Sistema de Pago").pack(pady=10)

    frame = tk.Frame(ej10)
    frame.pack(padx=20, pady=10)

    tk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(frame)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Horas normales:").grid(row=1, column=0, padx=10, pady=5)
    entry_horan = tk.Entry(frame)
    entry_horan.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Pago por hora:").grid(row=2, column=0, padx=10, pady=5)
    entry_pago = tk.Entry(frame)
    entry_pago.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame, text="Horas extras:").grid(row=3, column=0, padx=10, pady=5)
    entry_horae = tk.Entry(frame)
    entry_horae.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame, text="Num. hijos:").grid(row=4, column=0, padx=10, pady=5)
    entry_hijos = tk.Entry(frame)
    entry_hijos.grid(row=4, column=1, padx=10, pady=5)

    resultado = tk.Label(ej10, text="")
    resultado.pack(pady=10)

    def calculo():
        nombre = entry_nombre.get()

        try:
            horan = float(entry_horan.get())
            pago = float(entry_pago.get())
            horae = float(entry_horae.get())
            hijos = int(entry_hijos.get())
        except:
            messagebox.showerror("Error", "Datos inválidos")
            return

        pagon, pagoe, bono, total = calcular_pago(horan, pago, horae, hijos)

        trabajadores.append((nombre, pagon, pagoe, bono, total))

        resultado.config(text=f"Normal: {pagon:.2f}\nExtra: {pagoe:.2f}\nBono: {bono:.2f}\nTotal: {total:.2f}")

    def mostrar_reporte():
        if not trabajadores:
            messagebox.showinfo("Reporte", "No hay datos")
            return

        texto = ""
        for t in trabajadores:
            texto += f"{t[0]} - Total: {t[4]:.2f}\n"

        messagebox.showinfo("Reporte de pagos", texto)

    btn_frame = tk.Frame(ej10)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Calcular", width=15, command=calculo).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Reporte", width=15, command=mostrar_reporte).grid(row=0, column=1, padx=10)

    tk.Button(ej10, text="Cerrar", width=32, command=ej10.destroy).pack(pady=10)