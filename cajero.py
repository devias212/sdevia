import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

# Conexión a la base de datos SQLite
conn = sqlite3.connect('cajero.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE,
    contraseña TEXT,
    saldo REAL
)
''')

# Crear tabla para el historial de transacciones si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    tipo TEXT,
    cantidad REAL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
)
''')

conn.commit()

def crear_cuenta():
    ventana_crear_cuenta = tk.Toplevel(root)
    ventana_crear_cuenta.title('Crear cuenta')

    lbl_nombre = tk.Label(ventana_crear_cuenta, text='Nombre de usuario')
    lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(ventana_crear_cuenta)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    lbl_contraseña = tk.Label(ventana_crear_cuenta, text='Contraseña')
    lbl_contraseña.grid(row=1, column=0, padx=10, pady=10)
    entry_contraseña = tk.Entry(ventana_crear_cuenta, show="*")
    entry_contraseña.grid(row=1, column=1, padx=10, pady=10)

    def guardar_cuenta():
        nombre = entry_nombre.get()
        contraseña = entry_contraseña.get()

        if not nombre or not contraseña:
            messagebox.showerror("Error", "Nombre de usuario y contraseña son obligatorios.")
            return

        hashed_password = hashlib.sha256(contraseña.encode()).hexdigest()

        try:
            cursor.execute('INSERT INTO usuarios (nombre, contraseña, saldo) VALUES (?, ?, ?)', (nombre, hashed_password, 0))
            conn.commit()
            messagebox.showinfo("Éxito", "Cuenta creada exitosamente.")
            ventana_crear_cuenta.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya está en uso.")

    btn_guardar = tk.Button(ventana_crear_cuenta, text='Guardar', command=guardar_cuenta)
    btn_guardar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def iniciar_sesion():
    ventana_inicio_sesion = tk.Toplevel(root)
    ventana_inicio_sesion.title('Iniciar sesión')

    lbl_nombre = tk.Label(ventana_inicio_sesion, text='Nombre de usuario')
    lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(ventana_inicio_sesion)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    lbl_contraseña = tk.Label(ventana_inicio_sesion, text='Contraseña')
    lbl_contraseña.grid(row=1, column=0, padx=10, pady=10)
    entry_contraseña = tk.Entry(ventana_inicio_sesion, show="*")
    entry_contraseña.grid(row=1, column=1, padx=10, pady=10)

    def verificar_credenciales():
        nombre = entry_nombre.get()
        contraseña = entry_contraseña.get()

        cursor.execute('SELECT * FROM usuarios WHERE nombre = ? AND contraseña = ?', (nombre, contraseña))
        usuario = cursor.fetchone()

        if usuario:
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario[1]}")
            ventana_inicio_sesion.destroy()
            mostrar_operaciones(usuario)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    btn_iniciar_sesion = tk.Button(ventana_inicio_sesion, text='Iniciar sesión', command=verificar_credenciales)
    btn_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def mostrar_operaciones(usuario):
    ventana_operaciones = tk.Toplevel(root)
    ventana_operaciones.title("Operaciones en el cajero")

    lbl_saldo = tk.Label(ventana_operaciones, text=f"Saldo actual: {usuario[3]:.2f}")
    lbl_saldo.pack(padx=10, pady=5)

    lbl_destino = tk.Label(ventana_operaciones, text='Cuenta destino:')
    lbl_destino.pack(padx=10, pady=5)
    entry_destino = tk.Entry(ventana_operaciones)
    entry_destino.pack(padx=10, pady=5)

    lbl_cantidad_transferir = tk.Label(ventana_operaciones, text='Cantidad a transferir:')
    lbl_cantidad_transferir.pack(padx=10, pady=5)
    entry_cantidad_transferir = tk.Entry(ventana_operaciones)
    entry_cantidad_transferir.pack(padx=10, pady=5)

    lbl_cantidad_retirar = tk.Label(ventana_operaciones, text='Cantidad a retirar:')
    lbl_cantidad_retirar.pack(padx=10, pady=5)
    entry_cantidad_retirar = tk.Entry(ventana_operaciones)
    entry_cantidad_retirar.pack(padx=10, pady=5)

    def realizar_operaciones():
        destino = entry_destino.get()
        cantidad_transferir = float(entry_cantidad_transferir.get())
        cantidad_retirar = float(entry_cantidad_retirar.get())

        if cantidad_transferir > 0:
            cursor.execute('SELECT * FROM usuarios WHERE nombre = ?', (destino,))
            usuario_destino = cursor.fetchone()

            if usuario_destino:
                if usuario[3] >= cantidad_transferir:
                    nuevo_saldo_origen = usuario[3] - cantidad_transferir
                    nuevo_saldo_destino = usuario_destino[3] + cantidad_transferir

                    cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (nuevo_saldo_origen, usuario[0]))
                    cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (nuevo_saldo_destino, usuario_destino[0]))
                    cursor.execute('INSERT INTO transacciones (usuario_id, tipo, cantidad) VALUES (?, ?, ?)', (usuario[0], 'Transferencia salida', cantidad_transferir))
                    cursor.execute('INSERT INTO transacciones (usuario_id, tipo, cantidad) VALUES (?, ?, ?)', (usuario_destino[0], 'Transferencia entrada', cantidad_transferir))
                    conn.commit()

                    messagebox.showinfo("Éxito", f"Transferencia exitosa de {cantidad_transferir} a {destino}.")
                    lbl_saldo.config(text=f"Saldo actual: {nuevo_saldo_origen}")
                else:
                    messagebox.showerror("Error", "Saldo insuficiente.")
            else:
                messagebox.showerror("Error", "La cuenta destino no existe.")

        if cantidad_retirar > 0:
            if usuario[3] >= cantidad_retirar:
                nuevo_saldo = usuario[3] - cantidad_retirar
                cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (nuevo_saldo, usuario[0]))
                cursor.execute('INSERT INTO transacciones (usuario_id, tipo, cantidad) VALUES (?, ?, ?)', (usuario[0], 'Retiro', cantidad_retirar))
                conn.commit()

                messagebox.showinfo("Éxito", f"Retiro exitoso de {cantidad_retirar}.")
                lbl_saldo.config(text=f"Saldo actual: {nuevo_saldo}")
            else:
                messagebox.showerror("Error", "Saldo insuficiente.")

    btn_realizar_operaciones = tk.Button(ventana_operaciones, text='Realizar Operaciones', command=realizar_operaciones)
    btn_realizar_operaciones.pack(padx=10, pady=10)

def ver_historial(usuario):
    ventana_historial = tk.Toplevel(root)
    ventana_historial.title('Historial de transacciones')

    lbl_titulo = tk.Label(ventana_historial, text='Historial de transacciones', font=("Arial", 12, "bold"))
    lbl_titulo.pack(padx=10, pady=10)

    scrollbar = tk.Scrollbar(ventana_historial)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    historial_text = tk.Text(ventana_historial, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    historial_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    scrollbar.config(command=historial_text.yview)

    cursor.execute('SELECT * FROM transacciones WHERE usuario_id = ?', (usuario[0],))
    transacciones = cursor.fetchall()

    for transaccion in transacciones:
        historial_text.insert(tk.END, f"ID: {transaccion[0]}\n")
        historial_text.insert(tk.END, f"Tipo: {transaccion[2]}\n")
        historial_text.insert(tk.END, f"Cantidad: {transaccion[3]}\n")
        historial_text.insert(tk.END, f"Fecha: {transaccion[4]}\n\n")

    historial_text.config(state=tk.DISABLED)

def main():
    global root
    root = tk.Tk()
    root.title("Cajero Automático")

    lbl_bienvenida = tk.Label(root, text='¡Bienvenidos al Cajero Automático!', bg="#F0F0F0", fg="#333333", font=("Arial", 14, "bold"))
    lbl_bienvenida.pack(padx=10, pady=10)

    btn_crear_cuenta = tk.Button(root, text='Crear cuenta', command=crear_cuenta, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    btn_crear_cuenta.pack(padx=10, pady=5)

    btn_iniciar_sesion = tk.Button(root, text='Iniciar sesión', command=iniciar_sesion, bg="#008CBA", fg="white", font=("Arial", 10, "bold"))
    btn_iniciar_sesion.pack(padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
