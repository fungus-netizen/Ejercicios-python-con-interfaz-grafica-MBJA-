import tkinter as tk
import ej1, ej2, ej3, ej4, ej7, ej8, ej9, ej10

main = tk.Tk()
main.title("ventana principal")

tk.Label(main, text="Ejercicios con interfaz gráfica").pack(padx=20,pady=20)

# Botones
button_frame = tk.Frame(main)
button_frame.pack(padx=10, pady=10)

tk.Button(button_frame, text="1. Sueldos", width=20, command=lambda: ej1.abrir_ej1(main)).grid(row=0, column=0, padx=10, pady=5)
tk.Button(button_frame, text="2. Pago en Parque", width=20, command=lambda: ej2.abrir_ej2(main)).grid(row=0, column=1, padx=10, pady=5)
tk.Button(button_frame, text="3. Descuentos en Tienda", width=20, command=lambda: ej3.abrir_ej3(main)).grid(row=1, column=0, padx=10, pady=5)
tk.Button(button_frame, text="4. #<10", width=20, command=lambda: ej4.abrir_ej4(main)).grid(row=1, column=1, padx=10, pady=5)
tk.Button(button_frame, text="5. Suma de Enteros", width=20, command=lambda: ej7.abrir_ej7(main)).grid(row=3, column=0, padx=10, pady=5)
tk.Button(button_frame, text="6. Suma Acumulativa", width=20, command=lambda: ej8.abrir_ej8(main)).grid(row=3, column=1, padx=10, pady=5)
tk.Button(button_frame, text="7. Suma de Numeros", width=20, command=lambda: ej9.abrir_ej9(main)).grid(row=4, column=0, padx=10, pady=5)
tk.Button(button_frame, text="8. Pago de Trabajadores", width=20, command=lambda: ej10.abrir_ej10(main)).grid(row=4, column=1, padx=10, pady=5)

tk.Button(button_frame, text="Salir", width=44, bg="red", fg="white", command=main.destroy).grid(row=5, column=0, columnspan=2, padx=10, pady=(15,5))

main.mainloop()