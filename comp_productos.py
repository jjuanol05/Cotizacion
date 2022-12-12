""" 
>>> Para MacOS en terminal ejecutar la siguiente linea:
    brew install python-tk@3.10

>>> Para Ubuntu con Python 3.10, en terminal ejecutar la siguiente linea:
    sudo apt-get install python3.10-tk
"""

from tkinter.filedialog import askopenfilename
from pandas import DataFrame
from pathlib import Path
import pandas as pd
import id_program as id
import numpy as np
import time, os

def LowerOfTwoPrices(n1: float, n2: float):
    """Esta función retorna el precio más bajo y diferente de 0

    Args:
        n1 (float): Primer precio para a comparar
        n2 (float): Segundo precio para a comparar

    Returns:
        float | False: Precio más bajo o False si ambos son 0
    """
    if n1 == 0 and n2 == 0:
        return False 
    elif n1 >= n2 and n2 > 0:
        return n2
    elif n1 > 0:
        return n1
    else:
        return n2

def BestPriceOfThree(n1: float, n2: float, n3: float):
    """Esta función retorna el precio más bajo entre tres valores

    Args:
        n1 (float): Precio 1 para comparar
        n2 (float): Precio 2 para comparar
        n3 (float): Precio 3 para comparar

    Returns:
        float | False: Precio más bajo o False si son igual a 0
    """
    try:
        n = LowerOfTwoPrices(n1, n2)
        n_final = LowerOfTwoPrices(n, n3)
        return n_final
    except TypeError:
        return False

def PrintTable3(table: DataFrame):
    """Esta función imprime en consola el resultado de la comparación entre los 3 inventarios
    y exporta la tabla ordenada a un archivo .csv

    Args:
        table (DataFrame): DataFrame que contiene todos los datos analizados
    """
    export = DataFrame()
    for i in range(3):
        export[f"{id.code} {i+1}"] = table[f"{id.code} {i+1}"]
    export[f"{id.product}"] = table[f"{id.product}"]    
    for i in range(3):
        export[f"{id.price} {i+1}"] = table[f"{id.price} {i+1}"]
    export[f"{id.best_price}"] = table[f"{id.best_price}"]
    export[f"{id.num}"] = table[f"{id.num}"]
    export[f"{id.inv}"] = table[f"{id.inv}"]
    
    filepath = Path('Resultado/out.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    while True:
        try:
            export.to_csv(filepath, index=None, header=True, encoding='utf-8-sig')
            print(f"\n{export[[f'{id.product}','Precio 1', 'Precio 2', 'Precio 3', f'{id.best_price}', f'{id.inv}']]}")
            print('\nArchivo compare_list.csv exportado correctamente')
            break
        except PermissionError: 
            print(f"\n\t\tCIERRA EL ARCHIVO: compare_list.csv PARA EXPORTARLO Y ESPERA LA CONFIRMACIÓN")
            time.sleep(3)
        except OSError:     # Para Ubuntu
            export.to_csv(filepath, index=None, header=True, encoding='utf-8-sig')
            print(f"\n{export[[f'{id.product}','Precio 1', 'Precio 2', 'Precio 3', f'{id.best_price}', f'{id.inv}']]}")
            print('\nArchivo compare_list.csv exportado correctamente')
            break

def NumTable3(n1: int, n2: int, n3: int, n: int):
    """Esta función devuelve el número del inventario que contiene el mejor precio

    Args:
        n1 (int): Precio de inventario 1
        n2 (int): Precio de inventario 2
        n3 (int): Precio de inventario 3
        n (int): Mejor precio

    Returns:
        int | False: 1, 2, o 3 | False si ocurre algun error
    """
    if n == n1:
        return '1'
    elif n == n2:
        return '2'
    elif n == n3:
        return '3'
    else:   return False

def BestInventory3(df: DataFrame):
    """Esta función imprime en consola el resultado de analizar los 3 inventarios.
    Muestra el mejor inventario con el número de productos que contiene a mejor precio,
    y el número de productos con mejor precio de los otros dos inventarios.

    Args:
        df (DataFrame): DataFrame con los datos obtenidos del análisis 
    """
    count = np.zeros(3, int)

    for p in df[f'{id.num}']:
        if p == '1':
            count[0]+= 1
        elif p == '2':
            count[1]+= 1
        elif p == '3':
            count[2]+= 1
    
    if count[0] > count[1]:
        if count[0] > count[2]:
            print(f'\nEl mejor inventario es el 1.\tTiene {count[0]} productos a mejor precio')
            print(f'\nInventario 2 tiene {count[1]} productos a mejor precio\nInventario 3 tiene {count[2]} productos a mejor precio\n')
        else:
            print(f'\nEl mejor inventario es el 3.\nTiene {count[2]} productos a mejor precio\n')
            print(f'\nInventario 1 tiene {count[0]} productos a mejor precio\nInventario 2 tiene {count[1]} productos a mejor precio\n')
    elif count[1] > count[2]:
        print(f'\nEl mejor inventario es el 2.\nTiene {count[1]} productos a mejor precio\n')
        print(f'\nInventario 1 tiene {count[0]} productos a mejor precio\nInventario 3 tiene {count[2]} productos a mejor precio\n')
    else:
        print(f'\nEl mejor inventario es el 3.\nTiene {count[2]} productos a mejor precio\n')
        print(f'\nInventario 1 tiene {count[0]} productos a mejor precio\nInventario 2 tiene {count[1]} productos a mejor precio\n')

def CreateVector(size: int):
    """Esta función crea un vector con rango(size) para auxiliar en un proceso a la función CompareTables3

    Args:
        size (int): Tamaño del vector

    Returns:
        list: Vector con los indices de 0 a size -1 
    """
    vector = []
    for i in range(size):
        vector.append(i+1)
    return vector

def CompareTables3(table: DataFrame):
    """Esta función compara los precios de los 3 inventarios para encontrar el mejor precio

    Args:
        table (DataFrame): DataFrame con los datos de los 3 inventarios a analizar

    Returns:
        DataFrame: DataFrame que contiene los datos de los 3 inventarios y el de mejor precio
    """
    size = table[f'{id.product}'].__len__()
    best_price = []
    num_table = []

    j = iter(CreateVector(3))

    for i in range(0, size):
        n1 = table[f'{id.price} {next(j)}'][i]
        n2 = table[f'{id.price} {next(j)}'][i]
        n3 = table[f'{id.price} {next(j)}'][i]
        n_mejor = BestPriceOfThree(n1, n2, n3)
        if n_mejor:
            best_price.append(n_mejor)
            num_table.append(NumTable3(n1, n2, n3, n_mejor))
        j = iter(CreateVector(3))
    
    table[f'{id.best_price}'] = best_price
    table[f'{id.num}'] = num_table

    return table

def BestPriceByInventory3(inventory: DataFrame):
    """Esta función convierte la columna num del DataFrame que recibe a cadena de texto
    más descriptiva sobre cada inventario

    Args:
        inventory (DataFrame): DataFrame con los datos de analizar el precio de los 3 inventarios

    Returns:
        DataFrame: DataFrame con nueva columna 'Inventario x' 
    """
    inventarios = []
    for i in inventory[f'{id.num}']:
        if i == '1':
            inventarios.append(f'{id.inv} 1')
        elif i == '2':
            inventarios.append(f'{id.inv} 2')
        elif i == '3':
            inventarios.append(f'{id.inv} 3')
        else:   print(f'\n{id.Error1}: {i}')

    inventory[f'{id.inv}'] = inventarios

    return inventory

def FilesList(opt: int):
    """Esta función crea un DataFrame con el numero de inventarios que deseas analizar

    Args:
        opt (int): Número de inventarios para crear el DataFrame

    Returns:
        DataFrame: DataFrame nuevo con los datos de los (opt) inventarios para analizar
    """
    _table = DataFrame()
    while True:
        try:
            for i in range(opt):
                _file = askopenfilename()
                print(f"\nInventario {i+1}: {_file.replace('C:/Users/ameri/Documents/Inventario/Cotizaciones SIMA/', '')}")
                _inventory = pd.read_csv(f"{_file}", encoding='utf-8-sig', encoding_errors='replace', header=0)
                _table[f'{id.code} {i+1}'] = _inventory[f'{id.code}']
                _table[f'{id.product}'] = _inventory[f'{id.product}']
                _table[f'{id.price} {i+1}'] = _inventory[f'{id.price_csv}']
            break
        except FileNotFoundError:
            print('\nSeleccione un archivo .csv')
    return _table.fillna(0)

if __name__ == '__main__':
    """ Reto 1: Correr los 3 inventarios al mismo tiempo y 
    saber cuales son los mejores precios de cada inventario
    
    Comparar producto a producto cual es el mejor precio 
    y exportar cual es el mejor inventario """
    
    os.system(f'{id.clear}')
    while True:
        opt = input("\nElige una opción:\n1) Analizar 3 inventarios\n2) Analizar 5 inventarios\n3) Analizar 10 inventarios:\n")
        if opt == '1' or opt == '2' or opt == '3':
            if opt == '1':
                new_df = FilesList(3)
                compare_df = CompareTables3(new_df)
                final_df = BestPriceByInventory3(compare_df)
                PrintTable3(final_df)
                BestInventory3(final_df)
            # elif opt == '2':
            #     from _funciones_para_5 import CompareTables5, PrintTable5
            #     new_df = FilesList(5)
            #     compare_df = CompareTables5(new_df, opt)
                
            #     print(compare_df)
            #     PrintTable5(compare_df)

            #     # df_final = BestPriceByInventory5(df_compare)
            #     # BestInventory5(df_final, opt)
            # elif opt == '3':
            #     opt = int(10)
            break

    """" Reto 2: El inventario fisico el viernes
        las bases de datos de prueba el jueves
        checar para 5 inventarios y 10 """