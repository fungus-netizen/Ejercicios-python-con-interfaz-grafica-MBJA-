import tkinter as tk
from tkinter import messagebox

def abrir_ej9(root):
    ej9 = tk.Toplevel(root)
    ej9.title("Suma hasta superar 100")

    tk.Label(ej9, text="Suma Acumulativa").pack(pady=10)

    frame = tk.Frame(ej9)
    frame.pack(padx=20, pady=10)

    tk.Label(frame, text="Ingrese un numero:").grid(row=0, column=0, padx=10, pady=5)
    entry_num = tk.Entry(frame)
    entry_num.grid(row=0, column=1, padx=10, pady=5)

    resultado = tk.Label(ej9, text="")
    resultado.pack(pady=10)

    numeros = []
    suma = [0]

    def sumar():
        try:
            num = int(entry_num.get())
        except:
            messagebox.showerror("Error", "Ingrese un numero entero valido")
            return
        
        # Lit todo el ejercicio
        if suma[0] > 100:
            return

        numeros.append(num)
        suma[0] += num

        resultado.config(text=f"Suma: {suma[0]}")

        entry_num.delete(0, tk.END)

        if suma[0] > 100:
            lista_texto = ", ".join(str(n) for n in numeros)
            cantidad = len(numeros)

            messagebox.showinfo("Resultado final", f"Cantidad: {cantidad}\nLista: {lista_texto}\nSuma final: {suma[0]}")

    tk.Button(ej9, text="Agregar", width=20, command=sumar).pack(pady=10)

    tk.Button(ej9, text="Cerrar", width=32,command=ej9.destroy).pack(pady=10)