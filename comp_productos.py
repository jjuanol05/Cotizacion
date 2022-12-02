import pandas as pd

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
    print(f"\n{table[['Codigo','Producto', 'Precio 1', 'Precio 2', 'Precio 3', 'Mejor precio']]}")
    print("\nCSV exportado correctamente")

def NumTable(n1: int, n2: int, n3: int, n: int):
    if n == n1:
        return '1'
    elif n == n2:
        return '2'
    elif n == n3:
        return '3'

def BestInventory(df: pd.DataFrame):
    count1 = 0
    count2 = 0
    count3 = 0

    for p in df['Inventario']:
        if p == '1':
            count1+= 1
        elif p == '2':
            count2+= 1
        elif p == '3':
            count3+= 1
    
    if count1 > count2:
        if count1 > count3:
            print(f'\nEl mejor inventario es el 1.\nTiene {count1} productos más baratos\n')
        else:
            print(f'\nEl mejor inventario es el 3.\nTiene {count3} productos más baratos\n')
    elif count2 > count3:
        print(f'\nEl mejor inventario es el 2.\nTiene {count2} productos más baratos\n')
    else:
        print(f'\nEl mejor inventario es el 3.\nTiene {count3} productos más baratos\n')
    
def CompareTables(table: pd.DataFrame):
    size = table['Producto'].__len__()
    best_price = []
    comp_list = []
    num_table = []

    for i in range(0,size):
        n1 = table['Precio 1'][i]
        n2 = table['Precio 2'][i]
        n3 = table['Precio 3'][i]
        n_mejor, opt = BestPrice(n1, n2, n3)
        best_price.append(n_mejor)
        comp_list.append(opt)
        num_table.append(NumTable(n1, n2, n3, n_mejor))
    
    table['Comparar'] = comp_list
    table['Mejor precio'] = best_price
    table['Inventario'] = num_table

    return table

def CreateTable(list1: pd.DataFrame, list2: pd.DataFrame, list3: pd.DataFrame):
    _table = pd.DataFrame()
    _table['Codigo'] = list1['Código']
    _table['Producto'] = list1['Producto']
    _table['Precio 1'] = list1['Precio mensual']
    _table['Precio 2'] = list2['Precio mensual']
    _table['Precio 3'] = list3['Precio mensual']
    _table['Comparar'] = pd.Series([bool])
    return _table

if __name__ == '__main__':
    """ Reto: Correr los 3 inventarios al mismo tiempo y 
    saber cuales son los mejores precios de cada inventario
    
    Comparar producto a producto cual es el mejor precio 
    y exportar cual es el mejor inventario """

    inventory1 = pd.read_csv('lista_productos_1.csv', encoding='utf-8-sig', header=0)
    inventory2 = pd.read_csv('lista_productos_2.csv', encoding='utf-8-sig', header=0)
    inventory3 = pd.read_csv('lista_productos_3.csv', encoding='utf-8-sig', header=0)

    nueva_tabla = CreateTable(inventory1, inventory2, inventory3)
    mejor_tabla = CompareTables(nueva_tabla)

    PrintTable(mejor_tabla)
    BestInventory(mejor_tabla)