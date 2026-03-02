from PIL import Image, ImageTk


def iconAgregar():
    iconAgregar = Image.open("../assets/images/iconAgregar.png").convert("RGBA")
    iconAgregar = iconAgregar.resize((30, 30), Image.Resampling.LANCZOS)
    r, g, b, a = iconAgregar.split()
    new_color = Image.new("RGBA", iconAgregar.size,(255, 255, 255, 255))
    img_coloreada = Image.composite(new_color, iconAgregar, a)
    icono = ImageTk.PhotoImage(img_coloreada)
    return icono

def iconEditar():
    iconEditar = Image.open("../assets/images/iconEditar.png").convert("RGBA")
    iconEditar = iconEditar.resize((30, 30), Image.Resampling.LANCZOS)
    r, g, b, a = iconEditar.split()
    new_color = Image.new("RGBA", iconEditar.size,(255, 255, 255, 255))
    img_coloreada = Image.composite(new_color, iconEditar, a)
    icono = ImageTk.PhotoImage(img_coloreada)
    return icono

def iconEliminar():
    iconEliminar = Image.open("../assets/images/iconEliminar.png").convert("RGBA")
    iconEliminar = iconEliminar.resize((30, 30), Image.Resampling.LANCZOS)
    r, g, b, a = iconEliminar.split()
    new_color = Image.new("RGBA", iconEliminar.size,(255, 0, 0, 255))
    img_coloreada = Image.composite(new_color, iconEliminar, a)
    icono = ImageTk.PhotoImage(img_coloreada)
    return icono

def iconCheck():
    iconCheck = Image.open("../assets/images/iconCheck.png").convert("RGBA")
    iconCheck = iconCheck.resize((30, 30), Image.Resampling.LANCZOS)
    r, g, b, a = iconCheck.split()
    new_color = Image.new("RGBA", iconCheck.size,(255, 255, 255, 255))
    img_coloreada = Image.composite(new_color, iconCheck, a)
    icono = ImageTk.PhotoImage(img_coloreada)
    return icono

def iconExcel():
    iconExcel = Image.open("../assets/images/iconExcel.png").convert("RGBA")
    iconExcel = iconExcel.resize((30, 30), Image.Resampling.LANCZOS)
    r, g, b, a = iconExcel.split()
    new_color = Image.new("RGBA", iconExcel.size,(0, 0, 255, 255))
    img_coloreada = Image.composite(new_color, iconExcel, a)
    icono = ImageTk.PhotoImage(img_coloreada)
    return icono

def iconBD():
    iconBD = Image.open("../assets/images/iconBD.png").convert("RGBA")
    iconBD = iconBD.resize((30, 30), Image.Resampling.LANCZOS)
    r, g, b, a = iconBD.split()
    new_color = Image.new("RGBA", iconBD.size,(0, 0, 255, 255))
    img_coloreada = Image.composite(new_color, iconBD, a)
    icono = ImageTk.PhotoImage(img_coloreada)
    return icono

def iconNube():
    iconNube = Image.open("../assets/images/iconNube.png").convert("RGBA")
    iconNube = iconNube.resize((30, 30), Image.Resampling.LANCZOS)
    r, g, b, a = iconNube.split()
    new_color = Image.new("RGBA", iconNube.size,(230, 235, 240, 255))
    img_coloreada = Image.composite(new_color, iconNube, a)
    icono = ImageTk.PhotoImage(img_coloreada)
    return icono