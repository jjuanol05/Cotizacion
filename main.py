# Install tkinter   with sudo apt-get install python3.10-tk (for linux)
# Install tkinter   with brew install python-tk@3.10 (for MAC)
# Install pandas    with pip install pandas
# Install pathlib   with pip install pathlib

from tkinter.filedialog import askopenfilename
from QuoteObject import QuoteObject
import global_var as gv
import os

""" El mejor de 3 cotizaciones a, b, c:
    a > b
        resul > c
                resul: el mejor
"""

os.system(gv.CLEAR)

def compare_three_quotes(filepath1: str, filepath2: str, filepath3: str):
    
    quote_a = QuoteObject(filepath1)
    quote_b = QuoteObject(filepath2)
    quote_c = QuoteObject(filepath3)

    filepath = quote_a.compare(quote_b)
    
    if  filepath == filepath1:
        print(f'\nCOMPARACIÓN 1:\n{quote_a}')
        filepath = quote_a.compare(quote_c)
        print(f'\nCOMPARACIÓN 2:\n{quote_a}')

    elif filepath == filepath2:
        quote_b.compare(quote_a)
        print(f'\nCOMPARACIÓN 1:\n{quote_b}')
        filepath = quote_b.compare(quote_c)
        print(f'\nCOMPARACIÓN 2:\n{quote_b}')
    
    return filepath

try:
    # file1 = askopenfilename()
    # file2 = askopenfilename()
    # file3 = askopenfilename()

    file1 = '/home/jjuanol05/Documentos/SIMA/Codigo/Cotizaciones SIMA/Cotizacion Tamex 2087708.csv'
    file2 = '/home/jjuanol05/Documentos/SIMA/Codigo/Cotizaciones SIMA/Ventas.csv'
    file3 = '/home/jjuanol05/Documentos/SIMA/Codigo/Cotizaciones SIMA/641122.csv'
    file4 = '/home/jjuanol05/Documentos/SIMA/Codigo/Cotizaciones SIMA/Cotizacion Tamex 2087708.csv'
    file5 = '/home/jjuanol05/Documentos/SIMA/Codigo/Cotizaciones SIMA/641122.csv'

    file = compare_three_quotes(file1, file2, file3)

    file_final = compare_three_quotes(file, file4, file5)

except IndexError:
    print(f'\nNO SE PUDEN COMPARAR COTIZACIONES, NúMERO DE PRODUCTOS DIFERENTES\nIntente de nuevo')
    exit()
except KeyboardInterrupt:
    os.system(gv.CLEAR)
    exit()