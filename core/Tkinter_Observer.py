import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

from core.openYdelTablas import ControladorDeEX, iconExcel, iconBD

# IMPORTANTE: Aquí importamos tu clase externa
# from mi_archivo_de_logica import ControladorDeEX

# --- VARIABLES GLOBALES PARA LA GESTIÓN ---
controlador = None  # Aquí guardaremos la instancia de tu clase
lista_entrys = []  # Para mapear los widgets de la pantalla
ruta_selecionada=""
# --- FUNCIONES DE CONEXIÓN A TUS MÉTODOS ---

def accion_cargar():
    """Instancia la clase ControladorDeEX con el archivo seleccionado"""
    global controlador
    global ruta_selecionada
    ruta_selecionada = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if ruta_selecionada:
        try:
            # Llamamos al __init__ de tu clase
            controlador = ControladorDeEX(ruta_selecionada)
            renderizar_cuadricula()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo inicializar el controlador: {e}")


def renderizar_cuadricula():
    """Usa el método cabezeras() y getExcelName() para dibujar los Entrys"""
    global lista_entrys
    for widget in frame_interior_tabla.winfo_children():
        widget.destroy()

    lista_entrys = []
    # Usamos tus métodos
    df = controlador.getExcelName()
    columnas = controlador.cabezeras()

    # Dibujar encabezados
    for j, col in enumerate(columnas):
        tk.Label(frame_interior_tabla, text=col, font=("Garamond", 10, "bold"),
                 bg="#1a242f", fg="#00FF00", padx=10).grid(row=0, column=j)

    # Dibujar filas de Entrys
    for i, fila in df.iterrows():
        fila_widgets = []
        for j, valor in enumerate(fila):
            ent = tk.Entry(frame_interior_tabla, bg="#101922", fg="white", width=15)
            ent.insert(0, "" if pd.isna(valor) else str(valor))
            ent.grid(row=i + 1, column=j, padx=2, pady=2)
            fila_widgets.append(ent)
        lista_entrys.append(fila_widgets)

    # Actualizar scroll
    frame_interior_tabla.update_idletasks()
    canvas_tabla.config(scrollregion=canvas_tabla.bbox("all"))


def accion_eliminar():
    """Llama a tu método eliminarFila()"""
    if controlador and lista_entrys:
        # Ejemplo: eliminamos la última fila
        indice_ultimo = len(controlador.getExcelName()) - 1
        controlador.eliminarFila(indice_ultimo)
        renderizar_cuadricula()


def accion_agregar():
    """Llama a tu método addFila()"""
    if controlador:
        # Creamos una lista vacía con el tamaño de las cabeceras
        nueva_fila = [""] * len(controlador.cabezeras())
        controlador.addFila(nueva_fila)
        renderizar_cuadricula()


def accion_validar_y_guardar():
    """Actualiza el DF interno y llama a guardaCambios()"""
    if not controlador: return

    txt_errores.delete("1.0", tk.END)
    hay_errores = False

    # Sincronizamos los Entrys de la pantalla con el DataFrame de tu clase
    df = controlador.getExcelName()
    for i, fila_w in enumerate(lista_entrys):
        for j, entry in enumerate(fila_w):
            valor = entry.get()
            df.iat[i, j] = valor  # Actualización directa en la memoria del controlador
            if valor.strip() == "":
                hay_errores = True
                txt_errores.insert(tk.END, f"❌ Vacío: Fila {i + 1}, Col {controlador.cabezeras()[j]}\n", "error")

    if not hay_errores:
        controlador.guardaCambios(ruta_selecionada)  # Llamamos a tu método de guardado
        txt_errores.insert(tk.END, "✅ Cambios guardados en Excel correctamente.", "success")


def accion_backup():
    """Llama a tu método CopiaDeSeguridad()"""
    if controlador:
        controlador.CopiaDeSeguridad(ruta_selecionada)
        messagebox.showinfo("Backup", "Copia de seguridad generada.")


# --- INTERFAZ GRÁFICA (TU DISEÑO) ---
root = tk.Tk()
root.state('zoomed')
root.configure(bg="#101922")
# --- FRAME SUPERIOR (Layout de tu diseño original) ---
frameSuperior = tk.Frame(root, bg="#1a242f")
frameSuperior.pack(side="top", fill="x")

# (Aquí iría el Label de BASE DE DATOS e iconos...)
imgBD = iconBD()
textoBBDD = tk.Label(
    frameSuperior,
    image=imgBD,
    compound="left",
    text="BASE DE DATOS",
    font=("Garamond", 22, "bold"),
    bg="#1a242f",
    fg="cyan",
    padx=20,
    pady=10
)
textoBBDD.pack(side="left")

separador = tk.Frame(frameSuperior, bg="#E6F1FF", width=2, height=50)
separador.pack(side="left",padx=15,pady=15)

imgExcel = iconExcel()
btnCargaExcel = tk.Button(
    frameSuperior,
    cursor="hand2",
    image=imgExcel,
    text="Cargar Excel",
    font=("Garamond", 11, "bold"),
    compound="left",
    activebackground="Green4",
    activeforeground="azure",
    bg="#1a242f",
    fg="cyan",
    borderwidth=2,
    relief="solid",
    highlightthickness=2,
    highlightbackground="blue",
    command=accion_cargar
)
btnCargaExcel.pack(padx=20,pady=20,side="left")


btnCopiaSeguridad = tk.Button(frameSuperior, text="Generar Backup", bg="#1a242f", fg="white",
                              command=accion_backup, font=("Garamond", 11, "bold"))
btnCopiaSeguridad.pack(padx=20, pady=20, side="left")

# --- FRAME CENTRAL ---
frameInfo = tk.Frame(root, bg="#101922")
frameInfo.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# Tabla (Izquierda)
frameColumnas = tk.Frame(frameInfo, bg="#1a242f")
frameColumnas.pack(side="left", fill="both", expand=True, padx=10)
tk.Label(frameColumnas, text="Información Excel", font=("Garamond", 18, "bold"), bg="#1a242f", fg="#E6F1FF").pack(
    pady=10)

canvas_tabla = tk.Canvas(frameColumnas, bg="#1a242f", highlightthickness=0)
scroll_y = ttk.Scrollbar(frameColumnas, orient="vertical", command=canvas_tabla.yview)
frame_interior_tabla = tk.Frame(canvas_tabla, bg="#1a242f")
canvas_tabla.create_window((0, 0), window=frame_interior_tabla, anchor="nw")
canvas_tabla.configure(yscrollcommand=scroll_y.set)
scroll_y.pack(side="right", fill="y")
canvas_tabla.pack(fill="both", expand=True)

# Validación (Derecha)
frameValidacion = tk.Frame(frameInfo, bg="#1a242f", width=350)
frameValidacion.pack(side="right", fill="y")
tk.Label(frameValidacion, text="Reporte de Errores", font=("Garamond", 18, "bold"), bg="#1a242f", fg="#E6F1FF").pack(
    pady=10)
txt_errores = tk.Text(frameValidacion, bg="#101922", fg="#FF7F7F", width=40)
txt_errores.pack(fill="both", expand=True, padx=10, pady=10)
txt_errores.tag_config("error", foreground="red")
txt_errores.tag_config("success", foreground="#00FF00")

# --- FRAME INFERIOR ---
frameInferior = tk.Frame(root, bg="#1a242f")
frameInferior.pack(side="bottom", fill="x")

tk.Button(frameInferior, text="Añadir registro", bg="#1a242f", fg="white", command=accion_agregar).pack(side="left",
                                                                                                        padx=20,
                                                                                                        pady=20)
tk.Button(frameInferior, text="Eliminar", bg="#1a242f", fg="white", command=accion_eliminar).pack(side="left", padx=20,
                                                                                                  pady=20)
tk.Button(frameInferior, text="Validar y Guardar", bg="blue", fg="white", command=accion_validar_y_guardar).pack(
    side="right", padx=20, pady=20)

root.mainloop()