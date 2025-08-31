import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from db import conectar
import datetime

# 🎨 Colores y fuentes
COLOR_FONDO = "#FCE7A5"
COLOR_TEXTO = "#552113"
COLOR_TITULO = "#000000"
COLOR_BOTON = "#E64B3C"
COLOR_HOVER = "#a47149"
COLOR_CAJA = "#FFFFFF"
COLOR_BOTON_ACTUALIZAR = "#4CAF50"
COLOR_BOTON_ACTUALIZAR_HOVER = "#66bb6a"
COLOR_BOTON_CARGAR = "#2196F3"
COLOR_BOTON_CARGAR_HOVER = "#64b5f6"
COLOR_BOTON_LIMPIAR = "#9E9E9E"
COLOR_BOTON_LIMPIAR_HOVER = "#bdbdbd"

FUENTE_TITULO = ("Georgia", 18, "bold")
FUENTE_NORMAL = ("Georgia", 12)
ANCHO_ENTRADA = 50


def abrir_ventana_socios():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Socios")
    ventana.configure(bg=COLOR_FONDO)
    ventana.geometry("1500x700")
    ventana.resizable(False, False)

    # --- Título
    tk.Label(ventana, text="Gestión de Socios", font=FUENTE_TITULO,
             bg=COLOR_FONDO, fg=COLOR_TITULO).place(x=30, y=15)

    # --- Formulario
    frame_form = tk.Frame(ventana, bg=COLOR_CAJA, bd=3, relief="ridge")
    frame_form.place(x=20, y=60, width=420, height=460)

    tk.Label(frame_form, text="Formulario de Socio", font=("Georgia", 14, "bold"),
             bg=COLOR_CAJA, fg=COLOR_TEXTO).pack(pady=(10, 15))

    frame_campos = tk.Frame(frame_form, bg=COLOR_CAJA)
    frame_campos.pack(padx=20, fill=tk.BOTH, expand=True)

    campos = [
        ("Nombre", "nombre"),
        ("Apellido", "apellido"),
        ("DNI", "dni"),
        ("Domicilio", "domicilio"),
        ("Teléfono", "telefono")
    ]

    entradas = {}

    for idx, (etiqueta, var) in enumerate(campos):
        tk.Label(frame_campos, text=etiqueta + ":", font=FUENTE_NORMAL,
                 bg=COLOR_CAJA, fg=COLOR_TEXTO, anchor="w").grid(row=idx, column=0, sticky="w", pady=6)
        entrada = tk.Entry(frame_campos, font=FUENTE_NORMAL, width=ANCHO_ENTRADA,
                           bg=COLOR_CAJA, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO, relief="solid", bd=1)
        entrada.grid(row=idx, column=1, pady=6, padx=(10, 0))
        entradas[var] = entrada

    # Sexo
    tk.Label(frame_campos, text="Sexo:", font=FUENTE_NORMAL,
             bg=COLOR_CAJA, fg=COLOR_TEXTO, anchor="w").grid(row=len(campos), column=0, sticky="w", pady=6)
    sexo_combo = ttk.Combobox(frame_campos, font=FUENTE_NORMAL,
                              width=ANCHO_ENTRADA - 3,
                              values=["Masculino", "Femenino", "Otro"],
                              state="readonly")
    sexo_combo.grid(row=len(campos), column=1, pady=6, padx=(10, 0))
    entradas["sexo"] = sexo_combo

    # Fecha Último Pago
    tk.Label(frame_campos, text="Último Pago:", font=FUENTE_NORMAL,
             bg=COLOR_CAJA, fg=COLOR_TEXTO, anchor="w").grid(row=len(campos) + 1, column=0, sticky="w", pady=6)

    fecha_entry = DateEntry(frame_campos, font=FUENTE_NORMAL, width=ANCHO_ENTRADA - 8,
                            background='darkblue', foreground='white',
                            borderwidth=2, date_pattern='yyyy-MM-dd')
    fecha_entry.grid(row=len(campos) + 1, column=1, pady=6, padx=(10, 0))
    entradas["ultimop"] = fecha_entry

    # --- Referencias
    nombre, apellido, dni = entradas["nombre"], entradas["apellido"], entradas["dni"]
    domicilio, telefono, sexo, ultimop = entradas["domicilio"], entradas["telefono"], entradas["sexo"], entradas["ultimop"]

    socio_seleccionado_id = tk.IntVar(value=0)

    # --- Funciones internas
    def validar_campos():
        if not nombre.get().strip() or not apellido.get().strip() or not dni.get().strip():
            messagebox.showwarning("Validación", "Nombre, Apellido y DNI son obligatorios")
            return False
        if not dni.get().isdigit():
            messagebox.showwarning("Validación", "El DNI debe ser numérico")
            return False
        if telefono.get().strip() and not telefono.get().isdigit():
            messagebox.showwarning("Validación", "El teléfono debe ser numérico")
            return False
        return True

    def limpiar_campos():
        socio_seleccionado_id.set(0)
        for entrada in entradas.values():
            if isinstance(entrada, ttk.Combobox):
                entrada.set("")
            elif isinstance(entrada, DateEntry):
                entrada.set_date(datetime.date.today())
            else:
                entrada.delete(0, tk.END)
        nombre.focus_set()

    def cargar_datos_evento(event):
        try:
            item = tabla.focus()
            if not item:
                return
            datos = tabla.item(item, "values")
            socio_seleccionado_id.set(int(datos[0]))
            apellido.delete(0, tk.END)
            apellido.insert(0, datos[1])
            nombre.delete(0, tk.END)
            nombre.insert(0, datos[2])
            dni.delete(0, tk.END)
            dni.insert(0, datos[3])
            domicilio.delete(0, tk.END)
            domicilio.insert(0, datos[4])
            telefono.delete(0, tk.END)
            telefono.insert(0, datos[5])
            sexo.set(datos[6])
            ultimop.set_date(datetime.datetime.strptime(datos[7], "%Y-%m-%d").date())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")

    def guardar():
        if not validar_campos():
            return
        con = conectar()
        try:
            cursor = con.cursor()
            sql = """
            INSERT INTO socios (apellido, nombre, dni, direccion, fecha_pago, telefono, sexo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            sexo_map = {"Femenino": "F", "Masculino": "M", "Otro": "O"}
            sexo_db = sexo_map.get(sexo.get(), "O")
            datos = (
                apellido.get(), nombre.get(), dni.get(),
                domicilio.get(), ultimop.get_date().strftime("%Y-%m-%d"), telefono.get(), sexo_db
            )
            cursor.execute(sql, datos)
            con.commit()
            messagebox.showinfo("Éxito", "Socio registrado correctamente")
            limpiar_campos()
            cargar_socios_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el socio: {e}")
        finally:
            con.close()

    def actualizar():
        id_socio = socio_seleccionado_id.get()
        if id_socio == 0:
            messagebox.showwarning("Advertencia", "Primero seleccioná un socio para editar")
            return
        if not validar_campos():
            return
        con = conectar()
        try:
            cursor = con.cursor()
            sql = """
            UPDATE socios
            SET apellido=%s, nombre=%s, dni=%s, direccion=%s, fecha_pago=%s, telefono=%s, sexo=%s
            WHERE id=%s
            """
            sexo_map = {"Femenino": "F", "Masculino": "M", "Otro": "O"}
            sexo_db = sexo_map.get(sexo.get(), "O")
            datos = (
                apellido.get(), nombre.get(), dni.get(),
                domicilio.get(), ultimop.get_date().strftime("%Y-%m-%d"), telefono.get(), sexo_db,
                id_socio
            )
            cursor.execute(sql, datos)
            con.commit()
            messagebox.showinfo("Éxito", "Socio actualizado correctamente")
            limpiar_campos()
            cargar_socios_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el socio: {e}")
        finally:
            con.close()

    def eliminar():
        id_socio = socio_seleccionado_id.get()
        if id_socio == 0:
            messagebox.showwarning("Advertencia", "Seleccioná un socio para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar socio seleccionado?"):
            return
        con = conectar()
        try:
            cursor = con.cursor()
            cursor.execute("DELETE FROM socios WHERE id=%s", (id_socio,))
            con.commit()
            messagebox.showinfo("Éxito", "Socio eliminado correctamente")
            limpiar_campos()
            cargar_socios_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el socio: {e}")
        finally:
            con.close()

    # --- Estilo Treeview
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview",
                    background=COLOR_CAJA,
                    foreground=COLOR_TEXTO,
                    rowheight=28,
                    fieldbackground=COLOR_CAJA,
                    font=FUENTE_NORMAL)
    style.map('Treeview', background=[('selected', COLOR_BOTON)])

    columnas = ("id", "apellido", "nombre", "dni", "direccion", "telefono", "sexo", "fecha_pago")
    titulos = ("ID", "Apellido", "Nombre", "DNI", "Dirección", "Teléfono", "Sexo", "Último Pago")
    anchos = [50, 130, 130, 100, 150, 120, 100, 100]

    frame_tabla = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tabla.place(x=460, y=60, width=710, height=610)

    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")

    scrollbar_v = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
    scrollbar_h = ttk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL, command=tabla.xview)
    tabla.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

    scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
    tabla.pack(fill=tk.BOTH, expand=True)

    for col, title, ancho in zip(columnas, titulos, anchos):
        tabla.heading(col, text=title)
        tabla.column(col, width=ancho, anchor=tk.W)

    def cargar_socios_tabla():
        tabla.delete(*tabla.get_children())
        con = conectar()
        try:
            cursor = con.cursor()
            cursor.execute("SELECT id, apellido, nombre, dni, direccion, telefono, sexo, fecha_pago FROM socios")
            for registro in cursor.fetchall():
                sexo_legible = {"M": "Masculino", "F": "Femenino", "O": "Otro"}.get(registro[6], "Otro")
                registro_legible = list(registro)
                registro_legible[6] = sexo_legible
                tabla.insert("", tk.END, values=registro_legible)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los socios: {e}")
        finally:
            con.close()

    cargar_socios_tabla()
    tabla.bind("<<TreeviewSelect>>", cargar_datos_evento)

    # --- Botones
    def crear_boton(texto, x, y, bg, fg, hover_bg, comando):
        btn = tk.Button(ventana, text=texto, bg=bg, fg=fg, font=FUENTE_NORMAL,
                        width=18, height=2, relief="flat", cursor="hand2", command=comando)
        btn.place(x=x, y=y)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    crear_boton("Guardar Nuevo", 50, 530, COLOR_BOTON, "white", COLOR_HOVER, guardar)
    crear_boton("Actualizar", 230, 530, COLOR_BOTON_ACTUALIZAR, "white", COLOR_BOTON_ACTUALIZAR_HOVER, actualizar)
    crear_boton("Eliminar", 50, 590, COLOR_BOTON, "white", COLOR_HOVER, eliminar)
    crear_boton("Limpiar Campos", 230, 590, COLOR_BOTON_LIMPIAR, "white", COLOR_BOTON_LIMPIAR_HOVER, limpiar_campos)

    # Inicializar fecha actual
    limpiar_campos()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    abrir_ventana_socios()
    root.mainloop()
