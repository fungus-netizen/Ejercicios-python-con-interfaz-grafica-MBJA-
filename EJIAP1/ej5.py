import tkinter as tk
from tkinter import messagebox

def abrir_ej5(root):
    ej5 = tk.Toplevel(root)
    ej5.title("Validación 0 < n < 20")

    tk.Label(ej5, text="Validación de Numero").pack(pady=10)

    frame = tk.Frame(ej5)
    frame.pack(padx=20, pady=10)

    tk.Label(frame, text="Ingrese un numero:").grid(row=0, column=0, padx=10, pady=5)
    entry_num = tk.Entry(frame)
    entry_num.grid(row=0, column=1, padx=10, pady=5)

    resultado = tk.Label(ej5, text="")
    resultado.pack(pady=10)

    intentos = [0]
    incorrectos = [0]
    numeros_ej5 = []  # Ej 6

    def verificar_num():
        intentos[0] += 1

        try:
            num = int(entry_num.get())
        except:
            messagebox.showerror("Error", "Ingrese un numero valido")
            return

        numeros_ej5.append(num) # Ej 6

        if 0 < num < 20:
            resultado.config(
                text=f"Numero correcto: {num}\nIntentos: {intentos[0]}\nIncorrectos: {incorrectos[0]}"
            )
        else:
            incorrectos[0] += 1
            messagebox.showerror("Error", "El numero debe estar entre 1 y 19")
            entry_num.delete(0, tk.END)

#   Ej6
    def mostrar_historial():
        if not numeros_ej5:
            messagebox.showinfo("Historial", "No hay intentos")
            return

        texto = "Numeros ingresados:\n"
        for n in numeros_ej5:
            texto += f"{n}, "

        messagebox.showinfo("Historial", texto)

    tk.Button(ej5, text="Verificar", width=20, command=verificar_num).pack(pady=10)

#  Ej6
    tk.Button(ej5, text="Historial", width=20,command=mostrar_historial).pack(pady=5)

    tk.Button(ej5, text="Cerrar", width=32,command=ej5.destroy).pack(pady=10)