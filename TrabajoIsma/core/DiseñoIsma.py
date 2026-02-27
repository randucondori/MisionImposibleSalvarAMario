import tkinter as tk
from core.openYdelTablas import iconAgregar,iconEliminar,iconCheck,iconBD,iconEditar,iconNube,iconExcel


root = tk.Tk()
root.geometry("1500x1500")
root.configure(bg="#101922")


## FRAME INFERIOR--------------------------------
frameInferior = tk.Frame(root, bg="#1a242f")
frameInferior.pack(side="bottom", fill="x")

imgAgregar = iconAgregar()
botonAgregar = tk.Button(
    frameInferior,
    image=imgAgregar,
    text="Añadir registro",
    font=("Garamond",11,"bold"),
    compound="left",
    bg="#1a242f",
    activebackground="#00FF00",
    fg="white",
    cursor="hand2",
)
botonAgregar.pack(padx=20, pady=20, side="left")

botonAgregarFila = tk.Button(
    frameInferior,
    image=imgAgregar,
    text="Añadir fila",
    font=("Garamond",11,"bold"),
    compound="left",
    bg="#1a242f",
    activebackground="#00FF90",
    fg="white",
    cursor="hand2",
)
botonAgregarFila.pack(padx=20, pady=20, side="left")

imgEditar = iconEditar()
botonEditar = tk.Button(
    frameInferior,
    image=imgEditar,
    text="Editar registro",
    font=("Garamond",11,"bold"),
    borderwidth=2,
    compound="left",
    activebackground="#FFFF00",  # color cuando se presiona
    activeforeground="#000000",  # color del texto cuando se presiona
    bg="#1a242f",
    fg="white",
    cursor="hand2",
)
botonEditar.image = imgEditar  # <-- referencia de la imagen
botonEditar.pack(padx=20, pady=20, side="left")

imgEliminar = iconEliminar()
botonEliminar = tk.Button(
    frameInferior,
    image=imgEliminar,
    text="Eliminar",
    font=("Garamond",11,"bold"),
    compound="left",
    bg="#1a242f",
    activebackground="#FF7F7F",
    fg="white",
    cursor="hand2",
)
botonEliminar.pack(padx=20, pady=20, side="left")

imgCheck = iconCheck()
botonCheck = tk.Button(
    frameInferior,
    image=imgCheck,
    text="Validar datos",
    compound="left",
    font=("Garamond",11,"bold"),
    activebackground="dodger blue",
    bg="blue",
    fg="white",
    cursor="hand2",
)

def on_enter(e):
    botonEliminar['height'] = 34   # simula scaleY (agranda vertical)

def on_leave(e):
    botonEliminar['height'] = 30     # vuelve al tamaño original

botonEliminar.bind("<Enter>", on_enter)
botonEliminar.bind("<Leave>", on_leave)

botonCheck.pack(padx=20, pady=20, side="right")


## FRAME SUPERIOR--------------------------------
frameSuperior = tk.Frame(root, bg="#1a242f")
frameSuperior.pack(side="top", fill="x")

imgBD = iconBD()
textoBBDD = tk.Label(
    frameSuperior,
    image=imgBD,
    compound="left",
    text="BASE DE DATOS",
    font=("Garamond", 22, "bold"),
    bg="#1a242f",
    fg="#E6F1FF",
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
    fg="blue",
    borderwidth=2,
    relief="solid",
    highlightthickness=2,
    highlightbackground="blue"
)
btnCargaExcel.pack(padx=20,pady=20,side="left")


imgNube = iconNube()
btnCopiaSeguridad = tk.Button(
    frameSuperior,
    cursor="hand2",
    image=imgNube,
    text="Generar Backup",
    font=("Garamond", 11, "bold"),
    fg="#FFFFFF",
    compound="left",
    activebackground="#243447",
    activeforeground="azure",
    bg="#1a242f",
    highlightcolor="white",
    highlightthickness=0,
    borderwidth=0,
    relief="flat",
)
btnCopiaSeguridad.pack(padx=20,pady=20,side="left")

frameInfo = tk.Frame(root, bg="#101922")
frameInfo.pack(side="top", fill="both", expand=True, pady=10, padx=10)

frameColumnas = tk.Frame(frameInfo, bg="#1a242f")
frameColumnas.pack(side="left", fill="both", expand=True, padx=10)

line_top = tk.Frame(frameColumnas, bg="#E6F1FF", height=1)
line_top.pack(fill="x", side="top")

labelName = tk.Label(
    frameColumnas,
    text="Información Excel",
    font=("Garamond", 18, "bold"),
    bg="#1a242f",
    fg="#E6F1FF",
    padx=20,
    pady=10,
)
labelName.pack(fill="x")

line_bottom = tk.Frame(frameColumnas, bg="#E6F1FF", height=1)
line_bottom.pack(fill="x", side="top")

frameValidacion = tk.Frame(frameInfo, bg="#1a242f")
frameValidacion.pack(side="right", fill="y")

line_top = tk.Frame(frameValidacion, bg="#E6F1FF", height=1)
line_top.pack(fill="x", side="top")

labelValidacion = tk.Label(
    frameValidacion,
    text="Validación de Datos",
    font=("Garamond", 18, "bold"),
    bg="#1a242f",
    fg="#E6F1FF",
    padx=20,
    pady=10,
)
labelValidacion.pack(fill="x")

line_bottom = tk.Frame(frameValidacion, bg="#E6F1FF", height=1)
line_bottom.pack(fill="x", side="top")

root.mainloop()
