from datetime import date

import pandas as pd


class ControladorDeEX:
    def __init__(self, exel):
        # Cargamos todo como string para evitar problemas de formato en el Entry
        self.__excel = pd.read_excel(exel, dtype=str)
        self.ruta_archivo = exel

    def getExcel(self):
        return self.__excel

    def setExcel(self, nuevo_df):
        self.__excel = nuevo_df

    def cabezeras(self):
        return list(self.__excel.columns)

    def addFila(self, obValue):
        self.__excel.loc[len(self.__excel)] = obValue

    def addColumna(self, name: str):
        self.__excel[name] = ""

    def eliminarFilaPorIndice(self, index: int):
        # Validamos que el índice exista en el DataFrame
        if index in self.__excel.index:
            self.__excel.drop(index, axis=0, inplace=True)
            self.__excel.reset_index(drop=True, inplace=True)  # Reordenar índices
            return True
        return False

    def eliminarColumnaPorNombre(self, name: str):
        if name in self.__excel.columns:
            self.__excel.drop(name, axis=1, inplace=True)
            return True
        return False

    def guardaCambios(self, archivo):
        self.__excel.to_excel(archivo, index=False)

    def CopiaDeSeguridad(self, archivo):
        fecha = date.today().strftime("%d-%m-%Y")
        archivo_name = str(archivo).split(".")[0]
        ruta_final = f'{archivo_name}-{fecha}.xlsx'
        self.__excel.to_excel(ruta_final, index=False)
        return ruta_final

