from barcode import Code39
from barcode.writer import ImageWriter
import os
import pandas as pd
from tkinter.filedialog import askopenfilename

def create_barcode(code,product):
    path = "C:/Users/ameri/Documents/Inventario/Codigos de barra"
    os.chdir(path)
    with open(f'{product}.jpg', 'wb') as f:
        Code39(code, writer=ImageWriter()).write(f)

def OpenCSV(file: str):
    codelist = []
    productlist = []

    df = pd.read_csv(file, encoding='utf-8-sig', header=0)
    
    for i in range(0,df.__len__()):
        codelist.append(df['Código'][i])
        productlist.append(df['Producto'][i])

    return pd.DataFrame({'Código':codelist, 'Producto':productlist})

if __name__ == '__main__':
    
    """ Automatizar codigos de barra directamente de una base de datos 
    o cargar lista de productos y ejecutar codigos de barras por producto """
    
    _file = askopenfilename()
    lista = OpenCSV(_file)

    for i in range(0, lista['Código'].__len__()):
        code = lista['Código'][i]
        product = lista['Producto'][i]
        create_barcode(code, product)

        print(f'\nCódigo de barras: {code}\nProducto: {product}, creado.')