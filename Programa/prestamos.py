import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from db import conectar

# 🎨 Paleta personalizada
COLOR_FONDO = "#FCE7A5"         # Amarillo claro
COLOR_TEXTO = "#552113"         # Marrón oscuro
COLOR_TITULO = "#000000"        # Negro
COLOR_BOTON = "#E64B3C"         # Rojo libro
COLOR_HOVER = "#a47149"         # Marrón claro
COLOR_CAJA = "#FFFFFF"          # Fondo blanco para formularios

FUENTE_TITULO = ("Georgia", 16, "bold")
FUENTE_NORMAL = ("Georgia", 12)


def abrir_ventana_prestamos():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Préstamos")
    ventana.configure(bg=COLOR_FONDO)
    ventana.geometry("1000x500")
    ventana.resizable(False, False)

    # --- Sección de lista de préstamos ---
    frame_lista = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame_lista, text="Préstamos Registrados", 
             font=FUENTE_TITULO, fg=COLOR_TITULO, bg=COLOR_FONDO).pack(anchor="w")

    columnas = ("Nombre", "Apellido", "DNI", "ISBN", "Fecha Devolución", "Estado")
    tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", height=10)
    tree.pack(fill="both", expand=True)

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # --- Barra inferior con botones ---
    frame_botones = tk.Frame(ventana, bg=COLOR_BOTON, height=80)
    frame_botones.pack(fill="x")

    def on_enter(e, b): b.config(bg=COLOR_HOVER)
    def on_leave(e, b): b.config(bg=COLOR_BOTON)

    botones = [
        ("Modificar Préstamo", lambda: messagebox.showinfo("Modificar", "Función modificar aquí")),
        ("Nuevo Préstamo", lambda: messagebox.showinfo("Nuevo", "Función nuevo aquí")),
        ("Eliminar Préstamo", lambda: messagebox.showinfo("Eliminar", "Función eliminar aquí"))
    ]

    for texto, comando in botones:
        btn = tk.Button(frame_botones, text=texto, font=FUENTE_NORMAL,
                        bg=COLOR_BOTON, fg="white", activebackground=COLOR_HOVER,
                        width=20, command=comando)
        btn.pack(side="left", padx=20, pady=20)
        btn.bind("<Enter>", lambda e, b=btn: on_enter(e, b))
        btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))

    # --- Ejemplo de carga inicial (simulado) ---
    prestamos = [
        ("Nicolas", "Pucheta", "45692695", "21311", "2024-11-15", "Pendiente"),
        ("Juan", "Pérez", "28852323", "45682", "2024-11-14", "Pendiente")
    ]
    for p in prestamos:
        tree.insert("", tk.END, values=p)


# --- Para probar directamente ---
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta ventana principal
    abrir_ventana_prestamos()
    root.mainloop()
