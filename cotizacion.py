from pathlib import Path
import global_var as gv
import pandas as pd
import numpy as np
import time

def Min(n1: float, n2: float) -> float|bool:
    if n1 == 0 and n2 > 0:
        return n2
    elif n2 == 0 and n1 > 0:
        return n1
    elif n1 >= n2 and n2 > 0:
        return n2
    elif n1 <= n2 and n1 > 0:
        return n1
    elif n1 == 0 and n2 == 0:
        return False

def CountWords(words_list: list[str]) -> dict:
    word_dict = {}
    for word in words_list:
        if word in word_dict:
            word_dict[word] +=1
        else:
            word_dict[word] = 1
    return word_dict 

class Cotizacion():
    def __init__(self, _file: str) -> None:
        self.best = ''
        self.compare = ''
        
        self.path = _file
        self.name = _file.replace(gv.path_replace, '')

        self._dataframe = pd.read_csv(_file, encoding='utf-8-sig', encoding_errors='replace', header=0)

        self._table = pd.DataFrame()
        self._table[f'{gv.code}'] = self._dataframe[f'{gv.code}'].fillna(0)
        self._table[f'{gv.product}'] = self._dataframe[f'{gv.product}']
        self._table[f'{gv.price}'] = self._dataframe[f'{gv.price_csv}'].fillna(0)

        self.size = self._table[f'{gv.product}'].__len__()

    def NameCotiz(self, other, n1: float, n2: float, n: float) -> str|bool:
        if n == n1:
            return f'{self.name}'
        elif n == n2:
            return f'{other.name}'
        else:
            return False
    
    def Comparar(self, other_cot) -> str:
        self.comparacion = pd.DataFrame()
        self.comparacion[f'{gv.product}'] = self._dataframe[f'{gv.product}']
        
        self.compare = other_cot.name
        self.compare_table = other_cot._table
        count = np.zeros(2, int)

        self.best_price = []
        self.name_table = []
        self.none = 0

        if self.size == other_cot.size:
            for i in range(0, self.size):
                n1 = self._table[f'{gv.price}'][i]
                n2 = other_cot._table[f'{gv.price}'][i]
                
                best_n = Min(n1, n2)
                
                if best_n:
                    self.best_price.append(best_n)
                    self.name_table.append(self.NameCotiz(other_cot, n1, n2, best_n))
                else:
                    self.best_price.append(None)
                    self.name_table.append(None)
                    
            self.comparacion[f'{self.name}'] = self._table[f'{gv.price}']
            self.comparacion[f'{other_cot.name}'] = other_cot._table[f'{gv.price}']
            self.comparacion[f'{gv.best_price}'] = pd.Series(self.best_price).fillna(0)
            self.comparacion[f'{gv.name}'] = self.name_table
            
            self.count_other = self.CountOther(other_cot)

            for p in self.comparacion[f'{gv.name}']:
                if p == self.name:
                    count[0] += 1
                elif p == other_cot.name:
                    count[1] += 1
                else:
                    self.none += 1
            
            if count[0] >= count[1]:
                self.best = self.name
                self.count = count[0]
                return self.path
            else:
                self.best = other_cot.name
                self.count = other_cot.size - count[1] - self.none
                return other_cot.path
        else:
            raise IndexError()

    def CountOther(self, other) -> int:
        count_words = CountWords(self.comparacion[f'{gv.name}'])
        return count_words[other.name]


    def __str__(self) -> str:
        info = f"\nARCHIVO:\t{self.name}\n\n{self._table}\n\nCOMPARACIÓN CON:\t{self.compare}\n\n{self.compare_table}"
        info = f"{info}\n\nRESULTADO:\n\n{self.comparacion}"
        info = f"{info}\n\nCOTIZACIÓN:\t{self.name}\tPRODUCTOS A MEJOR PRECIO:\t{self.count}"
        if self.name != self.compare:
            info = f"{info}\nCOTIZACIÓN:\t{self.compare}\tPRODUCTOS A MEJOR PRECIO:\t{self.count_other}"
        if self.none != 0:
            info = f"{info}\nPRODUCTOS SIN REGISTRO DE PRECIO:\t{self.none}"
        info = f"{info}\n\nLA MEJOR COTIZACIÓN ES:\t{self.best}\n"
        
        self.Export()

        return info
    
    def Export(self):
        filepath = Path(gv.path_export)
        filepath.parent.mkdir(parents=False, exist_ok=True)
        while True:
            try:
                self.comparacion.to_csv(filepath, index=None, header=True, encoding='utf-8-sig')
                break
            except PermissionError: 
                print(f"\n\t\tCIERRA EL ARCHIVO: compare_list.csv PARA EXPORTARLO Y ESPERA LA CONFIRMACIÓN")
                time.sleep(3)
        