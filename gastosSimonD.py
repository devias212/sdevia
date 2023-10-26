from tkinter import *


def mostrar_placeholder1(event):
    if entrada1.get() != "":
        entrada1.delete(0, END)
        entrada1.config(fg="black")


def mostrar_placeholder2(event):
    if entrada2.get() != "":
        entrada2.delete(0, END)
        entrada2.config(fg="black")


def ocultar_placeholder1(event):
    if entrada1.get() == "":
        entrada1.insert(0, "Ingrese el producto")
        entrada1.config(fg="gray")


def ocultar_placeholder2(event):
    if entrada2.get() == "":
        entrada2.insert(0, "Ingrese el precio")
        entrada2.config(fg="gray")


def agregar_elemento():
    global lista, total
    
    try:
        total += float(entrada2.get())
        lista.append(
            (str(entrada1.get()).lower().title(), float(entrada2.get())))
    except ValueError:
        lbl2.config(text="Ingrese :")
    else:
        actualizar_lista()
        entrada1.delete(0, END)
        entrada2.delete(0, END)


def actualizar_lista():
    lista_label.config(text="Lista de compras:\n" +
                       "\n".join([f"{item[0]}: ${item[1]:.2f}" for item in lista]) + f"\nTotal: ${total:.2f}")


ventana = Tk()
ventana.title("App")
lista = []
total = 0
lbl1 = Label(ventana, text="Ingrese :")
entrada1 = Entry(ventana, fg="gray")
entrada1.insert(0, "Ingrese un producto")
entrada1.bind("<FocusIn>", mostrar_placeholder1)
entrada1.bind("<FocusOut>", ocultar_placeholder1)
entrada2 = Entry(ventana, fg="gray")
entrada2.insert(0, "Ingrese el precio")
entrada2.bind("<FocusIn>", mostrar_placeholder2)
entrada2.bind("<FocusOut>", ocultar_placeholder2)
btn1 = Button(ventana, text="Ingresar", command=agregar_elemento)
lbl2 = Label(ventana, text="")
lista_label = Label(ventana, text="")


entrada2.grid(row=0, column=2, sticky="w")
lista_label.grid(row=2, column=0, padx=1, pady=5, sticky="w")
lbl1.grid(row=0, column=0, padx=1, pady=10, sticky="w")
entrada1.grid(row=0, column=1, padx=1, pady=10, sticky="w")
btn1.grid(row=0, column=3, padx=1, pady=10, sticky="w")
lbl2.grid(row=1, column=0, padx=1, pady=10, sticky="w")
ventana.mainloop()
