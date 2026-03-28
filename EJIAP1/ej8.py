import tkinter as tk
from tkinter import messagebox

def abrir_ej8(root):
    ej8 = tk.Toplevel(root)
    ej8.title("Suma de suma Acumulativa")

    tk.Label(ej8, text="Suma Acumulativa").pack(pady=10)

    frame = tk.Frame(ej8)
    frame.pack(padx=20, pady=10)

    tk.Label(frame, text="Ingrese un numero (0 para terminar):").grid(row=0, column=0, padx=10, pady=5)
    entry_num = tk.Entry(frame)
    entry_num.grid(row=0, column=1, padx=10, pady=5)

    resultado = tk.Label(ej8, text="")
    resultado.pack(pady=10)

    numeros = []
    suma = [0]

    def sumar():
        try:
            num = float(entry_num.get())
        except:
            messagebox.showerror("Error", "Ingrese un numero válido")
            return

        if num == 0:
            if not numeros:
                messagebox.showinfo("Resultado", "No se ingresaron numeros")
                return

            lista_texto = ", ".join(str(n) for n in numeros)
            cantidad = len(numeros)

            messagebox.showinfo(
                "Resultado final",
                f"Lista: {lista_texto}\nCantidad: {cantidad}\nSuma total: {suma[0]:.2f}"
            )
            return

        numeros.append(num)
        suma[0] += num

        resultado.config(text=f"Suma: {suma[0]:.2f}")

        entry_num.delete(0, tk.END)

    tk.Button(ej8, text="Agregar", width=20, command=sumar).pack(pady=10)

    tk.Button(ej8, text="Cerrar", width=32,command=ej8.destroy).pack(pady=10)