import tkinter as tk
from tkinter import messagebox
import ej5

def abrir_ej4(root):
    ej4 = tk.Toplevel(root)
    ej4.title("Validacion < 10")

    tk.Label(ej4, text="Validación de Numero").pack(pady=10)

    frame = tk.Frame(ej4)
    frame.pack(padx=20, pady=10)

    tk.Label(frame, text="Ingrese un numero:").grid(row=0, column=0, padx=10, pady=5)
    entry_num = tk.Entry(frame)
    entry_num.grid(row=0, column=1, padx=10, pady=5)

    resultado = tk.Label(ej4, text="")
    resultado.pack(pady=10)

    intentos = [0]
    numeros_ej4 = []  # Ej 6

    def verificar_num():
        intentos[0] += 1

        try:
            num = int(entry_num.get())
        except:
            messagebox.showerror("Error", "Ingrese un numero valido")
            return

        numeros_ej4.append(num) # Ej 6

        if num < 10:
            resultado.config(text=f"Numero: {num}\nIntentos: {intentos[0]}")
        else:
            messagebox.showerror("Error", "El numero debe ser menor que 10")
            entry_num.delete(0, tk.END)

    tk.Button(ej4, text="Verificar", width=20, command=verificar_num).pack(pady=10)

#   Ej6
    def mostrar_historial():
        if not numeros_ej4:
            messagebox.showinfo("Historial", "No hay intentos")
            return

        texto = "Numeros ingresados:\n"
        for n in numeros_ej4:
            texto += f"{n}, "

        messagebox.showinfo("Historial", texto)


#   Ej6
    tk.Button(ej4, text="Historial", width=20,command=mostrar_historial).pack(pady=5)

    # Enlace a Ejercicio 5
    tk.Button(ej4, text="Ir a Ejercicio 5", width=20,command=lambda: ej5.abrir_ej5(root)).pack(pady=5)

    tk.Button(ej4, text="Cerrar", width=32,command=ej4.destroy).pack(pady=10)