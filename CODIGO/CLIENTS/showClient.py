from email.policy import default
import io
import os
import shutil
import sqlite3
from turtle import color
import PySimpleGUI as sg
from PIL import Image
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))


from CODIGO.LOGS import logs
from CODIGO.BD import queryFunctions

sg.theme('Dark Amber')

try:
    clientes = queryFunctions.selectBD('SELECT * FROM clientes')

except Exception as ex:
    sg.Popup('Error al recuperar los clientes de la base de datos')
    
    
maxItems = len(clientes)
contador = 0
print(contador)


def showNextClient():
    global contador
    global clientes
    if (contador + 1) == maxItems:
        print(maxItems)
    else:
        contador = contador + 1
        
    window['clientName'].update(clientes.iloc[contador]['nombre'])
    window['clientPhone'].update(clientes.iloc[contador]['telefono'])
    window['clientAddress'].update(clientes.iloc[contador]['direccion'])
    window['clientEmail'].update(clientes.iloc[contador]['correoelectronico'])
    
    print(contador)

def showLastClient():
    global contador
    if (contador) == 0:
        print(0)
    else:
        contador = contador - 1

    window['clientName'].update(clientes.iloc[contador]['nombre'])
    window['clientPhone'].update(clientes.iloc[contador]['telefono'])
    window['clientAddress'].update(clientes.iloc[contador]['direccion'])
    window['clientEmail'].update(clientes.iloc[contador]['correoelectronico'])
    
    print(contador)

layout = [[
    [
        sg.Text('SHOW CLIENT', font=('Any 17 underline'))
    ],[
        sg.Column(layout=[
            [sg.Text('CLIENT NAME:')],
            [sg.InputText(key='clientName', readonly=True, use_readonly_for_disable=True, default_text=clientes.iloc[contador]['nombre'])],
            [sg.Text('PHONE NUMBER:')],
            [sg.InputText(key='clientPhone', readonly=True, default_text=clientes.iloc[contador]['telefono'])],
            [sg.Text('CLIENT ADDRESS:')],
            [sg.InputText(key='clientAddress', readonly=True, default_text=clientes.iloc[contador]['direccion'])],
            [sg.Text('CLIENT EMAIL:')],
            [sg.InputText(key='clientEmail', readonly=True, default_text=clientes.iloc[contador]['correoelectronico'])],
            [sg.Column(layout=[[sg.Button('PREVIOUS', key='previousClient', size=(10,1)), sg.Text(f'{contador + 1} of {maxItems}',key='clientCount'),sg.Button('NEXT', key='nextClient', size=(10,1))]])],
            [sg.Button('DELETE',size=(10,1), button_color=('white','red'))]
        ], element_justification='c')
        ]
    ]
]

window = sg.Window('SHOW CLIENT', layout, size=(700,330), element_justification='c')


while True:             
    

    
    event, values = window.read()
    
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'nextClient':
        showNextClient()
        window['clientCount'].update(f'{contador + 1} of {maxItems}')
    elif event == 'previousClient':
        showLastClient()
        window['clientCount'].update(f'{contador + 1} of {maxItems}')
        