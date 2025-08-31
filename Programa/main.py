import tkinter as tk
from tkinter import messagebox

# Importar tus módulos reales
from socios import abrir_ventana_socios
from libros import abrir_ventana_libros
from prestamos import abrir_ventana_prestamos

# 🎨 Paleta inspirada en el logo
COLOR_FONDO = "#FCE7A5"         # Amarillo claro
COLOR_TEXTO = "#552113"         # Marrón oscuro
COLOR_TITULO = "#000000"        # Negro
COLOR_BOTON = "#E64B3C"         # Rojo libro
COLOR_HOVER = "#a47149"         # Marrón claro
COLOR_CAJA = "#FFFFFF"          # Fondo caja

# Tipografías
FUENTE_TITULO = ("Georgia", 24, "bold")
FUENTE_SUBTITULO = ("Georgia", 16, "bold")
FUENTE_LABEL = ("Georgia", 12)
FUENTE_BOTON = ("Georgia", 12, "bold")

# Credenciales
CREDENCIALES = {"admin": "1997"}

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# 📋 Menú Principal
class MenuPrincipal(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Menú Principal – Biblioteca José H. Porto")
        self.configure(bg=COLOR_FONDO)
        centrar_ventana(self, 500, 420)
        self.resizable(False, False)

        tk.Label(self, text="Menú Principal", font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

        # Botones
        btn_socios = self.crear_boton("Gestión de Socios", abrir_ventana_socios)
        btn_libros = self.crear_boton("Gestión de Libros", abrir_ventana_libros)
        btn_prestamos = self.crear_boton("Gestión de Préstamos", abrir_ventana_prestamos)
        btn_cerrar = self.crear_boton("Cerrar Sesión", self.cerrar_sesion, color=COLOR_TEXTO)

        for btn in [btn_socios, btn_libros, btn_prestamos, btn_cerrar]:
            btn.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)

    def crear_boton(self, texto, comando, color=COLOR_BOTON):
        btn = tk.Button(self, text=texto, font=FUENTE_LABEL, width=25,
                        bg=color, fg="white", activebackground=COLOR_HOVER,
                        command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    def cerrar_sesion(self):
        if messagebox.askokcancel("Cerrar sesión", "¿Deseas cerrar sesión?"):
            self.destroy()
            root.deiconify()

# 🔐 Verificación de login
def verificar_login(event=None):
    usuario = entrada_usuario.get().strip()
    contraseña = entrada_contraseña.get().strip()

    if not usuario or not contraseña:
        messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
        return

    if usuario in CREDENCIALES and contraseña == CREDENCIALES[usuario]:
        root.withdraw()
        MenuPrincipal(root)
    else:
        messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")

def toggle_password():
    entrada_contraseña.config(show="" if entrada_contraseña.cget("show") == "*" else "*")

# 🖥️ Ventana principal de login
root = tk.Tk()
root.title("Biblioteca José H. Porto – Login")
root.configure(bg=COLOR_FONDO)
centrar_ventana(root, 600, 500)
root.resizable(False, False)

tk.Label(root, text="BIBLIOTECA JOSÉ H. PORTO", font=FUENTE_TITULO, bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=(30, 5))
tk.Label(root, text="Sistema de Gestión Interna", font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()

# 📦 Caja formulario
frame = tk.Frame(root, bg=COLOR_CAJA, bd=2, relief="ridge", padx=20, pady=20)
frame.pack(pady=30)

tk.Label(frame, text="Usuario:", font=FUENTE_LABEL, bg=COLOR_CAJA, fg=COLOR_TEXTO).grid(row=0, column=0, sticky="w")
entrada_usuario = tk.Entry(frame, width=30)
entrada_usuario.grid(row=0, column=1, pady=10)

tk.Label(frame, text="Contraseña:", font=FUENTE_LABEL, bg=COLOR_CAJA, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="w")
entrada_contraseña = tk.Entry(frame, width=30, show="*")
entrada_contraseña.grid(row=1, column=1, pady=10)

check = tk.Checkbutton(frame, text="Mostrar contraseña", bg=COLOR_CAJA, fg=COLOR_TEXTO,
                       font=("Georgia", 10), command=toggle_password)
check.grid(row=2, column=1, sticky="w")

# 🔘 Botón login
btn_login = tk.Button(root, text="INICIAR SESIÓN", font=FUENTE_BOTON,
                      bg=COLOR_BOTON, fg="white", width=20, command=verificar_login)
btn_login.pack(pady=20)

btn_login.bind("<Enter>", lambda e: btn_login.config(bg=COLOR_HOVER))
btn_login.bind("<Leave>", lambda e: btn_login.config(bg=COLOR_BOTON))

# Pie
tk.Label(root, text="Villa Carlos Paz – Córdoba", font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(10, 0))

# Eventos
root.bind("<Return>", verificar_login)
entrada_usuario.focus_set()

# Ejecutar app
root.mainloop()
