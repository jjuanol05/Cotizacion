import os
import pandas as pd
from tkinter.filedialog import askopenfilename

def HigherPrice(n1: int, n2: int):
    if n1 >= n2:
        return n2, True
    else:
        return n1, False

def BestPrice(n1: int, n2: int, n3: int):
    n, opt = HigherPrice(n1, n2)
    n_final, opt = HigherPrice(n, n3)
    return n_final, opt 

def PrintTable(table: pd.DataFrame):
    table.to_csv(r'C:/Users/ameri/Documents/Inventario/compare_list.csv', index=None, header=True, encoding='utf-8-sig')
    print(f"\n{table[['Código','Producto', 'Precio 1', 'Precio 2', 'Precio 3', 'Mejor precio', 'Inventario']]}")
    print("\nCSV exportado correctamente")

def NumTable(n1: int, n2: int, n3: int, n: int):
    if n == n1:
        return '1'
    elif n == n2:
        return '2'
    elif n == n3:
        return '3'

def BestInventory(df: pd.DataFrame):
    count = [0,0,0]

    for p in df['Num']:
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

def CrearVector(size: int):
    vector = []
    for i in range(size):
        vector.append(i+1)
    return vector

def CompareTables(table: pd.DataFrame, num: int):
    size = table['Producto'].__len__()
    best_price = []
    comp_list = []
    num_table = []

    j = iter(CrearVector(num))

    for i in range(0, size):
        n1 = table[f'Precio {next(j)}'][i]
        n2 = table[f'Precio {next(j)}'][i]
        n3 = table[f'Precio {next(j)}'][i]
        n_mejor, opt = BestPrice(n1, n2, n3)
        best_price.append(n_mejor)
        comp_list.append(opt)
        num_table.append(NumTable(n1, n2, n3, n_mejor))
        j = iter(CrearVector(num))
    
    table['Comparar'] = comp_list
    table['Mejor precio'] = best_price
    table['Num'] = num_table

    return table

def BestPriceByInventory(inventory: pd.DataFrame):
    inventarios = []
    for i in inventory['Num']:
        if i == '1':
            inventarios.append('Inventario 1')
        elif i == '2':
            inventarios.append('Inventario 2')
        elif i == '3':
            inventarios.append('Inventario 3')
        else:   print(f'\nOcurrio un error: {i}')

    inventory['Inventario'] = inventarios

    return inventory

def FilesList(opt):
    _table = pd.DataFrame()

    for i in range(0, opt):
        _file = askopenfilename()
        _inventory = pd.read_csv(f"{_file}", encoding='utf-8-sig', header=0)
        _table['Código'] = _inventory['Código']
        _table['Producto'] = _inventory['Producto']
        _table[f'Precio {i+1}'] = _inventory['Precio mensual']

    return _table

if __name__ == '__main__':
    """ Reto: Correr los 3 inventarios al mismo tiempo y 
    saber cuales son los mejores precios de cada inventario
    
    Comparar producto a producto cual es el mejor precio 
    y exportar cual es el mejor inventario """
    
    os.system('cls')
    opt = input('\n¿Cuántos inventarios desea analizar? ')
    while not opt.isdigit():
        opt = input('\t\t\nError.\nIngrese un número entero\n¿Cuántos inventarios desea analizar? ')
    
    opt = int(opt)
    df = FilesList(opt)
    df_compare = CompareTables(df, opt)
    df_final = BestPriceByInventory(df_compare)
    PrintTable(df_final)
    BestInventory(df_final)