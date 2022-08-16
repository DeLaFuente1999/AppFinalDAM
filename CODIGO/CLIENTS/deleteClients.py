import PySimpleGUI as sg
import io
import os
from pathlib import Path
import sys

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))


from CODIGO.BD import queryFunctions


valores = queryFunctions.selectBD('SELECT nombre as NOMBRE, cif AS CIF, telefono AS TELEFONO, email AS EMAIL, direccion AS DIRECCION, cuentabanco AS "CUENTA BANCARIA" FROM proveedores')
print(valores.to_dict())

sg.theme('DarkGrey6')

layout = [
    [sg.Table(key='table', headings=list(valores), auto_size_columns=True, expand_x=True,justification='c', values=valores.values.tolist())],
    [sg.Column(layout=[[sg.Button('DELETE', key='deleteOne', size=(20,1)),sg.Button('DELETE ALL', key='deleteAll', button_color=('black', 'red'),size=(20,1))]])],
    [sg.Button('BACK TO MENU', key='backToMenu', size=(20,1))]
]

window = sg.Window('DELETE PROVIDER', layout, size=(800,280), element_justification='c')

while True:             
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'deleteOne':
        print('Eliminar uno')
        print(valores.values.tolist()[values['table']])
    elif event == 'deleteAll':
        print('Eliminar todos')
    elif event == 'backToMenu':
        print('Volver al menú')