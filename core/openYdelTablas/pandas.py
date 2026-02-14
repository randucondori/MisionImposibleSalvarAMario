import pandas as pd
from sqlite3 import connect

bd = pd.DataFrame(
    {
        "Name": [
            "Braund, Mr. Owen Harris",
            "Allen, Mr. William Henry",
            "Bonnell, Miss Elizabeth",
        ],
        "Age": [22, 35, 58],
        "Sex": ["male", "male", "female"],
    }
)


#Crear una tabla a base de un diccionario
# bd.to_sql(
#     name="prueba",
#     index=True,
#     if_exists="fail",
#     dtype={},
#     method="multi",
#     con=conn, )

    #Leer una tabla a base de un diccionario
# datos=pd.read_sql("select * from prueba",conn)
# print(datos)


class ControladorDeBD:
    def __init__(self, bases):
        self.__bases = []
        self.__bases.append(bases)

    def getBases(self):
        return self.__bases

    def addBase(self, base):
        self.__bases.append(base)

    def modificarBase(self, base, contenido):
        base = self.__bases.index(base)

    def __str__(self):
        data = ""
        i = 1
        for base in self.__bases:
            data += f"{i}- {base}"
            i += 1
        return data
conn = connect("memory.sqlite")


base = {
    "Name": [
        "Braund, Mr. Owen Harris",
        "Allen, Mr. William Henry",
        "Bonnell, Miss Elizabeth",
    ],
    "Age": [22, 35, 58],
    "Sex": ["male", "male", "female"],
}

controlador = ControladorDeBD(base)
print(controlador)
