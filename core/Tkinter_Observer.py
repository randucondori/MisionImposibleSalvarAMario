import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

# Variable global para guardar los datos cargados
df_actual = None


def seleccionar_y_cargar_archivo():
    global df_actual
    ruta_archivo = filedialog.askopenfilename(
        filetypes=(("Archivos de Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*"))
    )

    if ruta_archivo:
        try:
            df_actual = pd.read_excel(ruta_archivo)

            # Limpiar tabla y reporte de errores
            tabla.delete(*tabla.get_children())
            txt_errores.delete("1.0", tk.END)

            # Configurar columnas
            columnas = list(df_actual.columns)
            tabla["columns"] = columnas
            tabla["show"] = "headings"
            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=100)

            # Insertar datos
            for _, fila in df_actual.iterrows():
                # Reemplazar NaN por texto vacío para visualización
                valores = ["" if pd.isna(x) else x for x in fila]
                tabla.insert("", "end", values=valores)

            label_ruta.config(text=f"Archivo: {ruta_archivo.split('/')[-1]}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {e}")


def validar_datos():
    if df_actual is None:
        messagebox.showwarning("Atención", "Primero carga un archivo de Excel.")
        return

    txt_errores.delete("1.0", tk.END)
    hay_errores = False

    # 1. Buscar campos vacíos (NaN)
    # df.isna() devuelve una matriz de True/False
    posiciones_vacias = df_actual.isna()

    for columna in df_actual.columns:
        # Obtenemos los índices de las filas donde esa columna está vacía
        filas_vacias = df_actual[df_actual[columna].isna()].index

        if not filas_vacias.empty:
            hay_errores = True
            for fila in filas_vacias:
                # Sumamos 2 al índice: +1 porque Excel empieza en 1, y +1 por la cabecera
                mensaje = f"❌ Error: Campo vacío en Columna '{columna}', Fila Excel: {fila + 2}\n"
                txt_errores.insert(tk.END, mensaje, "error")

    if not hay_errores:
        txt_errores.insert(tk.END, "✅ ¡Validación completa! No se encontraron campos vacíos.", "success")

    # Hacer scroll automático al final
    txt_errores.see(tk.END)


# --- Interfaz ---
root = tk.Tk()
root.title("Validador de Excel con Python")
root.geometry("900x650")

# Panel Superior (Botones)
frame_controles = tk.Frame(root)
frame_controles.pack(pady=10)

btn_cargar = tk.Button(frame_controles, text="1. Cargar Excel", command=seleccionar_y_cargar_archivo, bg="#217346",
                       fg="white", padx=10)
btn_cargar.grid(row=0, column=0, padx=5)

btn_validar = tk.Button(frame_controles, text="2. Validar Datos", command=validar_datos, bg="#d9534f", fg="white",
                        padx=10)
btn_validar.grid(row=0, column=1, padx=5)

label_ruta = tk.Label(root, text="Sin archivo", fg="gray")
label_ruta.pack()

# Panel Medio (Visualización de Tabla)
frame_tabla = tk.Frame(root)
frame_tabla.pack(pady=10, fill="both", expand=True, padx=20)

tabla = ttk.Treeview(frame_tabla)
scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll_y.set)
scroll_y.pack(side="right", fill="y")
tabla.pack(side="left", fill="both", expand=True)

# Panel Inferior (Reporte de Errores)
tk.Label(root, text="Reporte de Errores:", font=("Arial", 10, "bold")).pack(anchor="w", padx=20)
txt_errores = tk.Text(root, height=8, padx=10, pady=10, font=("Consolas", 9))
txt_errores.pack(fill="x", padx=20, pady=(0, 20))

# Colores para el texto de errores
txt_errores.tag_config("error", foreground="red")
txt_errores.tag_config("success", foreground="green")

root.mainloop()