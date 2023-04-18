from tkinter.filedialog import askopenfilename
import cotizacion as ct
import global_var as gv
import os

os.system(gv.clear)

try:
    file1 = askopenfilename()
    file2 = askopenfilename()
    # file3 = askopenfilename()

    cot1 = ct.Cotizacion(file1)
    cot2 = ct.Cotizacion(file2)
    # cot3 = COT.Cotizacion(file3)

    cot1.Comparar(cot2)
    print(f'\n{cot1}')
    # cot1.Count()







except IndexError:
    print(f'\nNO SE PUDEN COMPARAR COTIZACIONES, NúMERO DE PRODUCTOS DIFERENTES\nIntente de nuevo')
    exit()
except KeyboardInterrupt:
    os.system(gv.clear)
    exit()