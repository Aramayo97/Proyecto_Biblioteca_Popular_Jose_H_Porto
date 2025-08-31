import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar

# 🎨 Paleta personalizada
COLOR_FONDO = "#FCE7A5"         # Amarillo claro
COLOR_TEXTO = "#552113"         # Marrón oscuro
COLOR_TITULO = "#000000"        # Negro
COLOR_BOTON = "#E64B3C"         # Rojo libro
COLOR_HOVER = "#a47149"         # Marrón claro
COLOR_CAJA = "#FFFFFF"          # Fondo caja

FUENTE_TITULO = ("Georgia", 16, "bold")
FUENTE_NORMAL = ("Georgia", 12)
ANCHO_ENTRADA = 40


def abrir_ventana_libros():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Libros")
    ventana.configure(bg=COLOR_FONDO)
    ventana.geometry("1200x700")
    ventana.resizable(True, True)

    # --- 🎨 Estilo ttk para Treeview ---
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background=COLOR_CAJA,
                    foreground=COLOR_TEXTO,
                    rowheight=25,
                    fieldbackground=COLOR_CAJA)
    style.map("Treeview", background=[("selected", COLOR_HOVER)])

    # --- 🔍 Barra de búsqueda ---
    frame_buscar = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_buscar.pack(pady=5)

    tk.Label(frame_buscar, text="Buscar:", font=FUENTE_NORMAL,
             bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side="left", padx=5)

    entrada_buscar = tk.Entry(frame_buscar, font=FUENTE_NORMAL, width=30,
                              bg=COLOR_CAJA, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO)
    entrada_buscar.pack(side="left", padx=5)

    def buscar_libro():
        termino = entrada_buscar.get().strip()
        tabla.delete(*tabla.get_children())
        try:
            con = conectar()
            cursor = con.cursor()
            sql = """SELECT isbn, titulo, categoria, subcategoria, autor, editorial, descripcion
                     FROM libros
                     WHERE titulo LIKE %s OR autor LIKE %s OR isbn LIKE %s"""
            like = f"%{termino}%"
            cursor.execute(sql, (like, like, like))
            for fila in cursor.fetchall():
                tabla.insert("", "end", values=fila)
            con.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda.\n{e}")

    tk.Button(frame_buscar, text="Buscar", font=FUENTE_NORMAL,
              bg=COLOR_BOTON, fg="white", command=buscar_libro).pack(side="left", padx=5)

    # --- 📑 Tabla ---
    frame_tabla = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tabla.pack(pady=10, padx=10, fill="both", expand=True)

    columnas = ("isbn", "titulo", "categoria", "subcategoria", "autor", "editorial", "descripcion")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    # Encabezados
    encabezados = ["ISBN", "Título", "Categoría", "Subcategoría", "Autor", "Editorial", "Descripción"]
    for col, text in zip(columnas, encabezados):
        tabla.heading(col, text=text)
        tabla.column(col, width=150, anchor="center")

    # Scrollbars
    scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabla.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    frame_tabla.grid_rowconfigure(0, weight=1)
    frame_tabla.grid_columnconfigure(0, weight=1)

    # --- 📋 Formulario ---
    frame_form = tk.LabelFrame(ventana, text="Datos del Libro", font=FUENTE_TITULO,
                               bg=COLOR_FONDO, fg=COLOR_TEXTO, padx=10, pady=10)
    frame_form.pack(pady=15)

    campos = [
        ("Título", "titulo"),
        ("Autor", "autor"),
        ("Editorial", "editorial"),
        ("ISBN", "isbn"),
        ("Categoría", "categoria"),
        ("Subcategoría", "subcategoria"),
    ]

    entradas = {}

    for idx, (label_texto, var) in enumerate(campos):
        tk.Label(frame_form, text=label_texto + ":", font=FUENTE_NORMAL,
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=idx, column=0, sticky="e", pady=5, padx=10)
        entrada = tk.Entry(frame_form, font=FUENTE_NORMAL, width=ANCHO_ENTRADA,
                           bg=COLOR_CAJA, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO)
        entrada.grid(row=idx, column=1, pady=5, padx=10, sticky="w")
        entradas[var] = entrada

    # Campo Descripción
    tk.Label(frame_form, text="Descripción:", font=FUENTE_NORMAL,
             bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=len(campos), column=0, sticky="ne", pady=5, padx=10)

    text_descripcion = tk.Text(frame_form, font=FUENTE_NORMAL, width=ANCHO_ENTRADA, height=4,
                               bg=COLOR_CAJA, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO)
    text_descripcion.grid(row=len(campos), column=1, pady=5, padx=10, sticky="w")

    # --- Funciones internas ---
    def cargar_libros():
        tabla.delete(*tabla.get_children())
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("SELECT isbn, titulo, categoria, subcategoria, autor, editorial, descripcion FROM libros")
            for fila in cursor.fetchall():
                tabla.insert("", "end", values=fila)
            con.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los libros.\n{e}")

    def guardar_libro():
        for key, entrada in entradas.items():
            if key != "descripcion" and not entrada.get().strip():
                messagebox.showwarning("Campo vacío", f"El campo '{key.capitalize()}' no puede estar vacío.")
                return
        try:
            con = conectar()
            cursor = con.cursor()
            sql = """INSERT INTO libros (isbn, titulo, categoria, subcategoria, autor, editorial, descripcion)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            datos = (
                entradas["isbn"].get().strip(),
                entradas["titulo"].get().strip(),
                entradas["categoria"].get().strip(),
                entradas["subcategoria"].get().strip(),
                entradas["autor"].get().strip(),
                entradas["editorial"].get().strip(),
                text_descripcion.get("1.0", tk.END).strip()
            )
            cursor.execute(sql, datos)
            con.commit()
            con.close()
            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            limpiar_campos()
            cargar_libros()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el libro.\n{e}")

    def actualizar_libro():
        item = tabla.selection()
        if not item:
            messagebox.showwarning("Seleccionar", "Seleccione un libro para actualizar.")
            return
        try:
            con = conectar()
            cursor = con.cursor()
            sql = """UPDATE libros SET titulo=%s, categoria=%s, subcategoria=%s,
                                        autor=%s, editorial=%s, descripcion=%s
                     WHERE isbn=%s"""
            datos = (
                entradas["titulo"].get().strip(),
                entradas["categoria"].get().strip(),
                entradas["subcategoria"].get().strip(),
                entradas["autor"].get().strip(),
                entradas["editorial"].get().strip(),
                text_descripcion.get("1.0", tk.END).strip(),
                entradas["isbn"].get().strip()
            )
            cursor.execute(sql, datos)
            con.commit()
            con.close()
            messagebox.showinfo("Éxito", "Libro actualizado correctamente")
            limpiar_campos()
            cargar_libros()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el libro.\n{e}")

    def eliminar_libro():
        item = tabla.selection()
        if not item:
            messagebox.showwarning("Seleccionar", "Seleccione un libro de la tabla.")
            return
        isbn = tabla.item(item, "values")[0]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar libro con ISBN {isbn}?"):
            return
        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("DELETE FROM libros WHERE isbn=%s", (isbn,))
            con.commit()
            con.close()
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")
            cargar_libros()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el libro.\n{e}")

    def limpiar_campos():
        for entrada in entradas.values():
            entrada.delete(0, tk.END)
        text_descripcion.delete("1.0", tk.END)

    def rellenar_campos(event):
        item = tabla.selection()
        if not item:
            return
        valores = tabla.item(item, "values")
        entradas["isbn"].delete(0, tk.END)
        entradas["isbn"].insert(0, valores[0])
        entradas["titulo"].delete(0, tk.END)
        entradas["titulo"].insert(0, valores[1])
        entradas["categoria"].delete(0, tk.END)
        entradas["categoria"].insert(0, valores[2])
        entradas["subcategoria"].delete(0, tk.END)
        entradas["subcategoria"].insert(0, valores[3])
        entradas["autor"].delete(0, tk.END)
        entradas["autor"].insert(0, valores[4])
        entradas["editorial"].delete(0, tk.END)
        entradas["editorial"].insert(0, valores[5])
        text_descripcion.delete("1.0", tk.END)
        text_descripcion.insert("1.0", valores[6])

    # --- Botones ---
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.pack(pady=15)

    btn_agregar = tk.Button(frame_botones, text="Agregar Libro", font=FUENTE_NORMAL,
                            bg=COLOR_BOTON, fg="white", width=15, command=guardar_libro)
    btn_actualizar = tk.Button(frame_botones, text="Actualizar Libro", font=FUENTE_NORMAL,
                               bg=COLOR_BOTON, fg="white", width=15, command=actualizar_libro)
    btn_eliminar = tk.Button(frame_botones, text="Eliminar Libro", font=FUENTE_NORMAL,
                             bg=COLOR_BOTON, fg="white", width=15, command=eliminar_libro)
    btn_volver = tk.Button(frame_botones, text="Volver", font=FUENTE_NORMAL,
                           bg=COLOR_BOTON, fg="white", width=15, command=ventana.destroy)

    btn_agregar.grid(row=0, column=0, padx=10)
    btn_actualizar.grid(row=0, column=1, padx=10)
    btn_eliminar.grid(row=0, column=2, padx=10)
    btn_volver.grid(row=0, column=3, padx=10)

    # Hover en botones
    for btn in (btn_agregar, btn_actualizar, btn_eliminar, btn_volver):
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BOTON))

    # 📌 Eventos
    tabla.bind("<<TreeviewSelect>>", rellenar_campos)

    # 📌 Cargar datos al abrir
    cargar_libros()
