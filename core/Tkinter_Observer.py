import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import pandas as pd

# Importación desde tu carpeta core
from openYdelTablas import (
    iconAgregar, iconEliminar, iconCheck, iconBD, iconExcel, iconNube, ControladorDeEX
)

controlador = None
entradas = {}
labelName = None
ruta = ""

def seleccionar_y_cargar_archivo():
    global controlador
    global ruta
    ruta = filedialog.askopenfilename(filetypes=(("Excel", "*.xlsx *.xls"), ("Todos", "*.*")))
    if ruta:
        try:
            controlador = ControladorDeEX(ruta)
            renderizar_tabla()
            if labelName:
                labelName.config(text=f"ARCHIVO: {ruta.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {e}")


def renderizar_tabla():
    global entradas
    if not controlador: return
    for widget in frame_interior_tabla.winfo_children():
        widget.destroy()
    entradas = {}
    columnas = controlador.cabezeras()
    df = controlador.getExcel()

    # --- CABECERA DE LA COLUMNA N° ---
    tk.Label(frame_interior_tabla, text="N°", font=("Garamond", 10, "bold"),
             bg="#05080a", fg="#ffcc00", width=5, relief="raised", borderwidth=1).grid(row=0, column=0, sticky="nsew",
                                                                                       padx=1, pady=1)

    # Cabeceras normales del Excel (ahora empiezan en columna 1)
    for j, col in enumerate(columnas):
        lbl = tk.Label(frame_interior_tabla, text=col.upper(), font=("Garamond", 10, "bold"),
                       bg="#05080a", fg="#5da9ff", width=22, relief="raised", borderwidth=1)
        lbl.grid(row=0, column=j + 1, sticky="nsew", padx=1, pady=1)

    # --- CUERPO DE LA TABLA ---
    for i in range(len(df)):
        bg_color = "#1a242f" if (i + 1) % 2 == 0 else "#243447"

        # 1. Creamos el Label del número de fila (N°)
        lbl_num = tk.Label(frame_interior_tabla, text=str(i + 1), font=("Arial", 10, "bold"),
                           bg=bg_color, fg="#ffcc00", width=5, relief="solid", borderwidth=1)
        lbl_num.grid(row=i + 1, column=0, padx=1, pady=1, sticky="nsew")

        # 2. Creamos los Entrys de datos (ahora en j+1)
        for j in range(len(columnas)):
            valor = df.iloc[i, j]
            en = tk.Entry(frame_interior_tabla, font=("Arial", 10), bg=bg_color, fg="white",
                          insertbackground="white", relief="solid", borderwidth=1,
                          highlightthickness=1, highlightbackground="#3d4d5d",
                          highlightcolor="#5da9ff", width=22)
            en.insert(0, str(valor) if not pd.isna(valor) else "")
            en.grid(row=i + 1, column=j + 1, padx=1, pady=1)
            entradas[(i, j)] = en

    actualizar_scroll()


# --- FUNCIONES DE BOTONES ---

def validar_datos():
    """Función de validación corregida y funcional"""
    if not controlador:
        messagebox.showwarning("Atención", "Carga un archivo primero.")
        return

    txt_errores.delete("1.0", tk.END)
    hay_errores = False
    columnas = controlador.cabezeras()

    # Recorremos todas las entradas generadas en la tabla
    for (r, c), entry in entradas.items():
        contenido = entry.get().strip()

        if contenido == "":
            hay_errores = True
            # Resaltar la celda con error
            entry.config(highlightbackground="#ff6b6b", highlightthickness=2)
            # Escribir en el reporte
            txt_errores.insert(tk.END, f"❌ Campo vacío: {columnas[c]}, Registro {r + 1}\n", "error")
        else:
            # Restaurar borde si está bien
            entry.config(highlightbackground="#3d4d5d", highlightthickness=1)

    if not hay_errores:
        txt_errores.insert(tk.END, "✅ VALIDACIÓN EXITOSA:\nNo se encontraron campos vacíos.", "success")

    txt_errores.see(tk.END)

def crearCopia():
    if not controlador:
        txt_errores.insert(tk.END, f"\n ❌No se pudo Crear \n Copia de Seguridad", "error")
        return
    controlador.CopiaDeSeguridad(ruta)
    txt_errores.insert(tk.END, "\n 🟢 Copia de Seguridad \n Creada Con éxito.", "success")

def eliminar_registro_visual():
    if not controlador: return
    num = simpledialog.askstring("Eliminar", "Número de registro a eliminar:")
    if num and num.isdigit():
        if controlador.eliminarFilaPorIndice(int(num) - 1):
            renderizar_tabla()
            txt_errores.insert(tk.END, f"🔴 Registro {num} eliminado.\n", "error")
        else:
            messagebox.showwarning("Error", "Registro no encontrado.")


def eliminar_campo_visual():
    if not controlador: return
    nombre = simpledialog.askstring("Eliminar", "Nombre exacto de la columna:")
    if nombre:
        if controlador.eliminarColumnaPorNombre(nombre):
            renderizar_tabla()
            txt_errores.insert(tk.END, f"🔴 Campo '{nombre}' eliminado.\n", "error")
        else:
            messagebox.showwarning("Error", "Columna no encontrada.")


def guardar_datos_visual():
    if not controlador: return
    columnas = controlador.cabezeras()
    filas = [[entradas[(i, j)].get() for j in range(len(columnas))] for i in range(len(controlador.getExcel()))]
    controlador.setExcel(pd.DataFrame(filas, columns=columnas))
    try:
        controlador.guardaCambios(controlador.ruta_archivo)
        messagebox.showinfo("Éxito", "Cambios guardados.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")


def añadir_registro_visual():
    if not controlador: return
    # Añadimos fila vacía al DF interno
    df_actual = controlador.getExcel()
    nueva_fila = pd.DataFrame([[""] * len(controlador.cabezeras())], columns=controlador.cabezeras())
    controlador.setExcel(pd.concat([df_actual, nueva_fila], ignore_index=True))
    renderizar_tabla()
    txt_errores.insert(tk.END, "🟢 Registro añadido al final.\n", "success")


def añadir_campo_visual():
    if not controlador: return
    nombre = simpledialog.askstring("Nuevo Campo", "Nombre de la columna:")
    if nombre:
        controlador.addColumna(nombre)
        renderizar_tabla()
        txt_errores.insert(tk.END, f"🔵 Campo '{nombre}' creado.\n", "success")


def actualizar_scroll():
    frame_interior_tabla.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# --- INTERFAZ ---
root = tk.Tk()
root.title("Validador Excel Premium")
root.state('zoomed')
root.configure(bg="#101922")

# HEADER
frameSuperior = tk.Frame(root, bg="#1a242f")
frameSuperior.pack(side="top", fill="x")

imgBD = iconBD()
tk.Label(frameSuperior, image=imgBD, compound="left", text=" SISTEMA BD",
         font=("Garamond", 22, "bold"), bg="#1a242f", fg="#E6F1FF", padx=20).pack(side="left", padx=20)

imgExcel = iconExcel()
tk.Button(frameSuperior, image=imgExcel, text=" Cargar Excel", font=("Garamond", 11, "bold"),
          compound="left", bg="#1a242f", fg="#5da9ff", borderwidth=1, relief="solid",
          command=seleccionar_y_cargar_archivo, cursor="hand2").pack(side="left", padx=10, pady=20)
tk.Button(frameSuperior,text="Copia De Seguridad",font=("Garamond", 11, "bold")
          ,compound="left", bg="#1a242f",fg="#5da9ff",command=crearCopia,cursor="hand2").pack(side="left", padx=10, pady=20)

# CUERPO
frameInfo = tk.Frame(root, bg="#101922")
frameInfo.pack(fill="both", expand=True, padx=10, pady=10)

frameContenedorTabla = tk.Frame(frameInfo, bg="#1a242f", borderwidth=1, relief="solid")
frameContenedorTabla.pack(side="left", fill="both", expand=True)

labelName = tk.Label(frameContenedorTabla, text="SIN ARCHIVO CARGADO", font=("Garamond", 12, "bold"),
                     bg="#0a0f14", fg="#E6F1FF", pady=8)
labelName.pack(fill="x")

canvas = tk.Canvas(frameContenedorTabla, bg="#101922", highlightthickness=0)
scrY = tk.Scrollbar(frameContenedorTabla, orient="vertical", command=canvas.yview)
scrX = tk.Scrollbar(frameContenedorTabla, orient="horizontal", command=canvas.xview)
frame_interior_tabla = tk.Frame(canvas, bg="#101922")
canvas.create_window((0, 0), window=frame_interior_tabla, anchor="nw")
canvas.configure(yscrollcommand=scrY.set, xscrollcommand=scrX.set)
scrY.pack(side="right", fill="y")
scrX.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)

frameValidacion = tk.Frame(frameInfo, bg="#1a242f", width=320)
frameValidacion.pack(side="right", fill="y", padx=(10, 0))
tk.Label(frameValidacion, text="NOTIFICACIONES", font=("Garamond", 12, "bold"),
         bg="#0a0f14", fg="#E6F1FF", pady=8).pack(fill="x")
txt_errores = tk.Text(frameValidacion, width=35, bg="#05080a", fg="#E6F1FF", font=("Consolas", 10), borderwidth=0)
txt_errores.pack(fill="both", expand=True, padx=8, pady=8)
txt_errores.tag_config("error", foreground="#ff6b6b")
txt_errores.tag_config("success", foreground="#51cf66")

# FOOTER
frameInferior = tk.Frame(root, bg="#1a242f")
frameInferior.pack(side="bottom", fill="x")

imgAdd = iconAgregar()
imgDel = iconEliminar()

tk.Button(frameInferior, image=imgAdd, text=" Añadir Registro", font=("Garamond", 10, "bold"),
          compound="left", bg="#1a242f", fg="white", relief="ridge",
          command=añadir_registro_visual).pack(side="left", padx=10, pady=15)

tk.Button(frameInferior, image=imgAdd, text=" Añadir Campo", font=("Garamond", 10, "bold"),
          compound="left", bg="#1a242f", fg="white", relief="ridge",
          command=añadir_campo_visual).pack(side="left", padx=10, pady=15)

tk.Button(frameInferior, image=imgDel, text=" Eliminar Registro", font=("Garamond", 10, "bold"),
          compound="left", bg="#1a242f", fg="#ff6b6b", relief="ridge",
          command=eliminar_registro_visual).pack(side="left", padx=10, pady=15)

tk.Button(frameInferior, image=imgDel, text=" Eliminar Campo", font=("Garamond", 10, "bold"),
          compound="left", bg="#1a242f", fg="#ff6b6b", relief="ridge",
          command=eliminar_campo_visual).pack(side="left", padx=10, pady=15)

# --- BOTONES DERECHA RECONECTADOS ---
imgCheck = iconCheck()
tk.Button(frameInferior, image=imgCheck, text=" VALIDAR ", font=("Garamond", 11, "bold"),
          bg="blue", fg="white", command=validar_datos,  # <--- CONECTADO
          relief="raised", padx=15).pack(side="right", padx=20)

tk.Button(frameInferior, text=" GUARDAR CAMBIOS ", font=("Garamond", 11, "bold"),
          bg="#28a745", fg="white", command=guardar_datos_visual, relief="raised", padx=15).pack(side="right", padx=10)

root.mainloop()
