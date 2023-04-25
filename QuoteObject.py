from pathlib import Path
from global_var import CODE, NAME, PRODUCT, PRICE, PRICE_CSV, PATH_REPLACE, PATH_EXPORT, BEST_PRICE
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


class QuoteObject():
    def __init__(self, path_file: str) -> None:
        self.QUOTE_PATH = path_file
        self.QUOTE_NAME = path_file.replace(PATH_REPLACE, "")

        self.QUOTE_DATAFRAME = pd.read_csv(
            path_file, encoding="utf-8-sig", encoding_errors="replace", header=0
        )

        self.QUOTE_TABLE = pd.DataFrame()
        self.QUOTE_TABLE[CODE] = self.QUOTE_DATAFRAME[CODE].fillna(0)
        self.QUOTE_TABLE[PRODUCT] = self.QUOTE_DATAFRAME[PRODUCT]
        self.QUOTE_TABLE[PRICE] = self.QUOTE_DATAFRAME[PRICE_CSV].fillna(0)

        self.QUOTE_SIZE = self.QUOTE_TABLE[PRODUCT].__len__()

    def name_of_quote(self, other_quote_object, n1: float, n2: float, n: float) -> str | bool:
        if n == n1:
            return self.QUOTE_NAME
        elif n == n2:
            return other_quote_object.QUOTE_NAME
        else:
            return False

    def compare(self, other_quote_object) -> str:

        self.name_the_quote_to_compare = other_quote_object.QUOTE_NAME
        self.quote_table_to_compare = other_quote_object.QUOTE_TABLE

        self.table_with_best_prices = []
        self.table_with_quote_names = []

        if self.QUOTE_SIZE == other_quote_object.QUOTE_SIZE:
            for i in range(self.QUOTE_SIZE):
                n1 = self.QUOTE_TABLE[PRICE][i]
                n2 = other_quote_object.QUOTE_TABLE[PRICE][i]

                best_n = Min(n1, n2)

                if best_n:
                    self.table_with_best_prices.append(best_n)
                    self.table_with_quote_names.append(
                        self.name_of_quote(other_quote_object, n1, n2, best_n)
                    )
                else:
                    self.table_with_best_prices.append(None)
                    self.table_with_quote_names.append(None)

            self.number_of_matches = self.table_with_quote_names.count(self.QUOTE_NAME)
            self.number_of_differences = self.table_with_quote_names.count(other_quote_object.QUOTE_NAME)
            self.number_of_none = self.table_with_quote_names.count(None)

            self.export_to_csv(other_quote_object)

            if self.number_of_matches >= self.number_of_differences:
                self.name_of_the_best_quote = self.QUOTE_NAME
                return self.QUOTE_PATH
            else:
                self.name_of_the_best_quote = other_quote_object.QUOTE_NAME
                return other_quote_object.QUOTE_PATH

        else:
            raise IndexError()

    def __str__(self) -> str:
        info = f"\nARCHIVO:\t{self.QUOTE_NAME}\n\n{self.QUOTE_TABLE}\n\nCOMPARACIÓN CON:\t{self.name_the_quote_to_compare}\n\n{self.quote_table_to_compare}\n\nRESULTADO:\n\n{self.comparative_table_of_quotations}\n\nCOTIZACIÓN:\t{self.QUOTE_NAME}\tPRODUCTOS A MEJOR PRECIO:\t{self.number_of_matches}"
        if self.QUOTE_NAME != self.name_the_quote_to_compare:
            info = f"{info}\nCOTIZACIÓN:\t{self.name_the_quote_to_compare}\tPRODUCTOS A MEJOR PRECIO:\t{self.number_of_differences}"
        if self.number_of_none != 0:
            info = f"{info}\nPRODUCTOS SIN REGISTRO DE PRECIO:\t{self.number_of_none}"
        info = f"{info}\n\nLA MEJOR COTIZACIÓN ES:\t{self.name_of_the_best_quote}\n"

        return info

    def export_to_csv(self, other_quote_object):
        self.comparative_table_of_quotations = pd.DataFrame()
        self.comparative_table_of_quotations[PRODUCT] = self.QUOTE_DATAFRAME[PRODUCT]
        self.comparative_table_of_quotations[self.QUOTE_NAME] = self.QUOTE_TABLE[PRICE]
        self.comparative_table_of_quotations[other_quote_object.QUOTE_NAME] = other_quote_object.QUOTE_TABLE[PRICE]
        self.comparative_table_of_quotations[BEST_PRICE] = pd.Series(
            self.table_with_best_prices
        ).fillna(0)
        self.comparative_table_of_quotations[NAME] = self.table_with_quote_names

        filepath = Path(PATH_EXPORT)
        filepath.parent.mkdir(parents=False, exist_ok=True)
        while True:
            try:
                self.comparative_table_of_quotations.to_csv(
                    filepath, index=None, header=True, encoding="utf-8-sig"
                )
                break
            except PermissionError:
                print(
                    f"\n\t\tCIERRA EL ARCHIVO: compare_list.csv PARA EXPORTARLO Y ESPERA LA CONFIRMACIÓN"
                )
                time.sleep(3)
