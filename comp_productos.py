import os
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename
import id_program as id

def LowerOfTwoPrices(n1: int, n2: int):
    if n1 >= n2:
        return n2
    else:
        return n1

def BestPriceOfThree(n1: int, n2: int, n3: int):
    try:
        n = LowerOfTwoPrices(n1, n2)
        n_final = LowerOfTwoPrices(n, n3)
        return n_final
    except TypeError:
        return False

def PrintTable3(table: pd.DataFrame):
    table.to_csv(r'C:/Users/ameri/Documents/Inventario/test/compare_list.csv', index=None, header=True, encoding='utf-8-sig')
    print(f"\n{table[[f'{id.code}',f'{id.product}','Precio 1', 'Precio 2', 'Precio 3', f'{id.best_price}', f'{id.inv}']]}")

def PrintTable5(table: pd.DataFrame):
    table.to_csv(r'C:/Users/ameri/Documents/Inventario/compare_list.csv', index=None, header=True, encoding='utf-8-sig')
    print(f"\n{table[[f'{id.code}',f'{id.product}','Precio 1', 'Precio 2', 'Precio 3', 'Precio 4', 'Precio 5', f'{id.best_price}', f'{id.inv}']]}")

def NumTable3(n1: int, n2: int, n3: int, n: int):
    if n == n1:
        return '1'
    elif n == n2:
        return '2'
    elif n == n3:
        return '3'
    else:   return False

def NumTable5(n1: int, n2: int, n3: int, n4: int, n5: int, n: int):
    x = NumTable3(n1, n2, n3, n)
    if x in ['1','2','3']:
        return x
    elif n == n4:
        return '4'
    elif n == n5:
        return '5'

def BestInventory3(df: pd.DataFrame, opt: int):
    count = np.zeros(opt, int)

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
    elif count[1] > count[2]:
        print(f'\nEl mejor inventario es el 2.\nTiene {count[1]} productos a mejor precio\n')
    else:
        print(f'\nEl mejor inventario es el 3.\nTiene {count[2]} productos a mejor precio\n')

def CreateVector(size: int):
    vector = []
    for i in range(size):
        vector.append(i+1)
    return vector

def CompareTables3(table: pd.DataFrame, num: int):
    size = table[f'{id.product}'].__len__()
    best_price = []
    num_table = []

    j = iter(CreateVector(num))

    for i in range(0, size):
        n1 = table[f'{id.price} {next(j)}'][i]
        n2 = table[f'{id.price} {next(j)}'][i]
        n3 = table[f'{id.price} {next(j)}'][i]
        n_mejor = BestPriceOfThree(n1, n2, n3)
        if n_mejor:
            best_price.append(n_mejor)
            num_table.append(NumTable3(n1, n2, n3, n_mejor))
        j = iter(CreateVector(num))
    
    table[f'{id.best_price}'] = best_price
    table[f'{id.num}'] = num_table

    return table

def CompareTables5(table: pd.DataFrame, num: int):
    size = table[f'{id.product}'].__len__()
    vector_n = []
    best_price = []
    num_table = []

    j = iter(CreateVector(num))
    """ a > b > c > d > e
            alpha > d > e
                    beta => será el mejor
        """
    for i in range(0, size):
        n1 = table[f'{id.price} {next(j)}'][i]
        n2 = table[f'{id.price} {next(j)}'][i]
        n3 = table[f'{id.price} {next(j)}'][i]
        n4 = table[f'{id.price} {next(j)}'][i]
        n5 = table[f'{id.price} {next(j)}'][i]
        alpha = BestPriceOfThree(n1, n2, n3)
        beta = BestPriceOfThree(alpha, n4, n5)
        best_price.append(beta)
        num_table.append(NumTable5(n1, n2, n3, n4, n5, beta))
        j = iter(CreateVector(num))
    
    table[f'{id.best_price}'] = best_price
    table[f'{id.num}'] = num_table
    
    return table

def BestPriceByInventory3(inventory: pd.DataFrame):
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

def FilesList(opt):
    _table = pd.DataFrame()

    for i in range(0, opt):
        _file = askopenfilename()
        _inventory = pd.read_csv(f"{_file}", encoding='utf-8-sig', encoding_errors='replace', header=0)
        _table[f'{id.code}'] = _inventory[f'{id.code}']
        _table[f'{id.product}'] = _inventory[f'{id.product}']
        _table[f'{id.price} {i+1}'] = _inventory[f'{id.price_csv}']

    return _table

if __name__ == '__main__':
    """ Reto 1: Correr los 3 inventarios al mismo tiempo y 
    saber cuales son los mejores precios de cada inventario
    
    Comparar producto a producto cual es el mejor precio 
    y exportar cual es el mejor inventario """
    
    os.system('cls')
    while True:
        opt = input("\nElige una opción:\n1) Analizar 3 inventarios\n2) Analizar 5 inventarios\n3) Analizar 10 inventarios:\n")
        if opt == '1' or opt == '2' or opt == '3':
            if opt == '1':
                opt = int(3)
                df = FilesList(opt)
                df_compare = CompareTables3(df, opt)
                df_final = BestPriceByInventory3(df_compare)
                PrintTable3(df_final)
                BestInventory3(df_final, opt)
            elif opt == '2':
                opt = int(5)
                df = FilesList(opt)
                df_compare = CompareTables5(df, opt)
                
                print(df_compare)

                # df_final = BestPriceByInventory5(df_compare)
                # PrintTable5(df_final)
                # BestInventory5(df_final, opt)
            elif opt == '3':
                opt = int(10)
            break

    """" Reto 2: El inventario fisico el viernes
        las bases de datos de prueba el jueves
        checar para 5 inventarios y 10 """