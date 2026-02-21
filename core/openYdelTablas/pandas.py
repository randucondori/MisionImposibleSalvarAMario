from datetime import date

import pandas as pd


# conn = connect("memory.sqlite")

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


class ControladorDeEX:
    def __init__(self,exel):
        self.__excel =pd.read_excel(exel)

    def getExcelName(self):
        return self.__excel

    def cabezeras(self):
        return list(self.__excel.keys())

    def modificarFila(self,col:int,fil:str,value):
        self.__excel.insert(col,fil,value)

    def addFila(self,obValue):
        self.__excel.loc[len(self.__excel)]=obValue

    def addColumna(self,name:str):
        self.__excel[name]=[]

    def eliminarFila(self,index:int):
        self.__excel.drop([index],axis=0,inplace=True)

    def eliminarUltimaFila(self):
        self.__excel.drop([len(self.__excel)-1],axis=0,inplace=True)

    def eliminarColumna(self,col:str):
        self.__excel.drop(col,axis=1,inplace=True)

    def filasSin(self,col:str):
        filas=self.__excel.loc[self.__excel[col]=="nsd"]
        return  f"no hay filas con la columna '{col}' vacia" if filas.empty else filas

    def guardaCambios(self):
        self.__excel.to_excel('prueba.xlsx',index=False)

    def CopiaDeSeguridad(self):
        fecha=date.today().strftime("%d-%m-%Y")
        self.__excel.to_excel(f'prueba-{fecha}.xlsx',index=False)


    def __str__(self):
        return f"{self.__excel}"

# nuevo=pd.DataFrame({
#     "nombre":["daniel","ricardo"],
#     "apellidos":["moreno","angel"]
# })

# nuevo.to_excel("prueba.xlsx",index=False)

controlador=ControladorDeEX("prueba.xlsx")
controlador.addFila({"nombre":"randu","apellido":"wolbert"})
controlador.guardaCambios()


# print(list(datos.keys())) #obtener la cabezera
# print(list(datos.index)) #obtener las posiciones de los elemntos
# datos.at[6,"Nombre"]="martias"
#
# with pd.ExcelWriter('prueba.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
#     datos.to_excel(writer,sheet_name='sheet1',index=False)
#     datos.loc[1,"Nombre"]="mario"



