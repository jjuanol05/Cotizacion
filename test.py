from tkinter.filedialog import askopenfilename
from QuoteObject import QuoteObject
from global_var import CLEAR
import os

os.system(CLEAR)

try:
    file1 = askopenfilename()
    file2 = askopenfilename()
    # file3 = askopenfilename()

    cot1 = QuoteObject(file1)
    cot2 = QuoteObject(file2)
    # cot3 = COT.Cotizacion(file3)

    cot1.compare(cot2)
    print(f'\n{cot1}')
    # cot1.Count()

except IndexError:
    print(f'\nNO SE PUDEN COMPARAR COTIZACIONES, NúMERO DE PRODUCTOS DIFERENTES\nIntente de nuevo')
    exit()
except KeyboardInterrupt:
    os.system(CLEAR)
    exit()