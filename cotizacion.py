from pathlib import Path
import global_var as gv
import pandas as pd
import time


def Min(n1: float, n2: float) -> float | bool:
    if n1 == 0 and n2 == 0:
        return False
    elif n1 >= n2 and n2 > 0:
        return n2
    elif n1 > 0:
        return n1
    else:
        return n2


class Cotizacion():
    def __init__(self, _file: str) -> None:

        self.FILE_PATH = _file
        self.FILE_NAME = _file.replace(gv.PATH_REPLACE, '')

        self._DATAFRAME = pd.read_csv(
            _file, encoding='utf-8-sig', encoding_errors='replace', header=0)

        self._TABLE = pd.DataFrame()
        self._TABLE[f'{gv.CODE}'] = self._DATAFRAME[f'{gv.CODE}'].fillna(0)
        self._TABLE[f'{gv.PRODUCT}'] = self._DATAFRAME[f'{gv.PRODUCT}']
        self._TABLE[f'{gv.PRICE}'] = self._DATAFRAME[f'{gv.PRICE_CSV}'].fillna(
            0)

        self.SIZE = self._TABLE[f'{gv.PRODUCT}'].__len__()

    def NameQuote(self, other, n1: float, n2: float, n: float) -> str | bool:
        if n == n1:
            return f'{self.FILE_NAME}'
        elif n == n2:
            return f'{other.FILE_NAME}'
        else:
            return False

    def Compare(self, other) -> str:

        self.FILE_TO_COMPARE = other.FILE_NAME
        self.TABLE_TO_COMPARE = other._TABLE

        self.table_with_best_prices = []
        self.table_with_names = []

        if self.SIZE == other.SIZE:
            for i in range(self.SIZE):
                n1 = self._TABLE[f'{gv.PRICE}'][i]
                n2 = other._TABLE[f'{gv.PRICE}'][i]

                best_n = Min(n1, n2)

                if best_n:
                    self.table_with_best_prices.append(best_n)
                    self.table_with_names.append(
                        self.NameQuote(other, n1, n2, best_n))
                else:
                    self.table_with_best_prices.append(None)
                    self.table_with_names.append(None)

            self.count = self.table_with_names.count(self.FILE_NAME)
            self.count_other = self.table_with_names.count(other.FILE_NAME)
            self.NONE = self.table_with_names.count(None)

            self.Export_to_CSV(other)

            if self.count >= self.count_other:
                self.name_best_quote = self.FILE_NAME
                return self.FILE_PATH
            else:
                self.name_best_quote = other.FILE_NAME
                return other.FILE_PATH

        else:
            raise IndexError()

    def __str__(self) -> str:
        info = f"\nARCHIVO:\t{self.FILE_NAME}\n\n{self._TABLE}"
        info = f"{info}\n\nCOMPARACIÓN CON:\t{self.FILE_TO_COMPARE}\n\n{self.TABLE_TO_COMPARE}"
        info = f"{info}\n\nRESULTADO:\n\n{self.comparative_table}"
        info = f"{info}\n\nCOTIZACIÓN:\t{self.FILE_NAME}\tPRODUCTOS A MEJOR PRECIO:\t{self.count}"
        if self.FILE_NAME != self.FILE_TO_COMPARE:
            info = f"{info}\nCOTIZACIÓN:\t{self.FILE_TO_COMPARE}\tPRODUCTOS A MEJOR PRECIO:\t{self.count_other}"
        if self.NONE != 0:
            info = f"{info}\nPRODUCTOS SIN REGISTRO DE PRECIO:\t{self.NONE}"
        info = f"{info}\n\nLA MEJOR COTIZACIÓN ES:\t{self.name_best_quote}\n"

        return info

    def Export_to_CSV(self, other):

        self.comparative_table = pd.DataFrame()
        self.comparative_table[f'{gv.PRODUCT}'] = self._DATAFRAME[f'{gv.PRODUCT}']
        self.comparative_table[f'{self.FILE_NAME}'] = self._TABLE[f'{gv.PRICE}']
        self.comparative_table[f'{other.FILE_NAME}'] = other._TABLE[f'{gv.PRICE}']
        self.comparative_table[f'{gv.TABLE_WITH_BEST_PRICES}'] = pd.Series(
            self.table_with_best_prices).fillna(0)
        self.comparative_table[f'{gv.NAME}'] = self.table_with_names

        filepath = Path(gv.PATH_EXPORT)
        filepath.parent.mkdir(parents=False, exist_ok=True)
        while True:
            try:
                self.comparative_table.to_csv(
                    filepath, index=None, header=True, encoding='utf-8-sig')
                break
            except PermissionError:
                print(
                    f"\n\t\tCIERRA EL ARCHIVO: compare_list.csv PARA EXPORTARLO Y ESPERA LA CONFIRMACIÓN")
                time.sleep(3)
