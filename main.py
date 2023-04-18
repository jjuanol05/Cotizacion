# Install tkinter   with sudo apt-get install python3.10-tk (for linux)
# Install tkinter   with brew install python-tk@3.10 (for MAC)
# Install pandas    with pip install pandas
# Install numpy     with pip install numpy
# Install pathlib   with pip install pathlib

from tkinter.filedialog import askopenfilename
import cotizacion as ct
import global_var as gv
import os

""" El mejor de 3 cotizaciones a, b, c:
    a > b
        resul > c
                resul: el mejor
"""

os.system(gv.clear)

try:
    # file1 = askopenfilename()
    # file2 = askopenfilename()
    # file3 = askopenfilename()

    file1 = '/home/jjuanol05/Documentos/SIMA/Codigo/Cotizaciones SIMA/Cotizacion Tamex 2087708.csv'
    file2 = '/home/jjuanol05/Documentos/SIMA/Codigo/Cotizaciones SIMA/Ventas.csv'
    file3 = '/home/jjuanol05/Documentos/SIMA/Codigo/Cotizaciones SIMA/641122.csv'

    cot1 = ct.Cotizacion(file1)
    cot2 = ct.Cotizacion(file2)
    cot3 = ct.Cotizacion(file3)

    file = cot1.Comparar(cot2)
    
    if  file == file1:
        print(f'\nCOMPARACIÓN 1:\n{cot1}')
        cot1.Comparar(cot3)
        print(f'\nCOMPARACIÓN 2:\n{cot1}')

    elif file == file2:
        cot2.Comparar(cot1)
        print(f'\nCOMPARACIÓN 1:\n{cot2}')
        cot2.Comparar(cot3)
        print(f'\nCOMPARACIÓN 2:\n{cot2}')

except IndexError:
    print(f'\nNO SE PUDEN COMPARAR COTIZACIONES, NúMERO DE PRODUCTOS DIFERENTES\nIntente de nuevo')
    exit()
except KeyboardInterrupt:
    os.system(gv.clear)
    exit()