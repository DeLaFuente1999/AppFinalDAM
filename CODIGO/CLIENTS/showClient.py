from email.policy import default
import subprocess
import pandas as pd
import io

import os
absolutepath = os.path.abspath(__file__)
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

sg.theme('DarkGrey6')

try:
    clientes = queryFunctions.selectBD('SELECT * FROM clientes')
    if clientes.empty:
        clientes = {'nombre': ['NO DATA'], 'telefono': ['NO DATA'], 'direccion': ['NO DATA'],'correoelectronico': ['NO DATA']}
        clientes= pd.DataFrame(clientes)
except Exception as ex:
    sg.Popup('Error retrieving clients from database')
    
    
maxItems = len(clientes)
contador = 0

def showNextClient():
    global contador
    global clientes
    
    if (contador + 1) != maxItems:
        contador = contador + 1
        
    window['clientName'].update(clientes.iloc[contador]['nombre'])
    window['clientPhone'].update(clientes.iloc[contador]['telefono'])
    window['clientAddress'].update(clientes.iloc[contador]['direccion'])
    window['clientEmail'].update(clientes.iloc[contador]['correoelectronico'])
    

def showLastClient():
    global contador
    if (contador) != 0:
        contador = contador - 1
        
    window['clientName'].update(clientes.iloc[contador]['nombre'])
    window['clientPhone'].update(clientes.iloc[contador]['telefono'])
    window['clientAddress'].update(clientes.iloc[contador]['direccion'])
    window['clientEmail'].update(clientes.iloc[contador]['correoelectronico'])
    
layout = [[
    [
        sg.Text('SHOW CLIENT', font=('Any 17 underline'))
    ],[
        sg.Column(layout=[
            [sg.Text('CLIENT NAME:')],
            [sg.InputText(key='clientName', readonly=True, disabled_readonly_background_color='#68868c', use_readonly_for_disable=True, default_text=clientes.iloc[contador]['nombre'])],
            [sg.Text('PHONE NUMBER:')],
            [sg.InputText(key='clientPhone', readonly=True, disabled_readonly_background_color='#68868c', default_text=clientes.iloc[contador]['telefono'])],
            [sg.Text('CLIENT ADDRESS:')],
            [sg.InputText(key='clientAddress', readonly=True, disabled_readonly_background_color='#68868c', default_text=clientes.iloc[contador]['direccion'])],
            [sg.Text('CLIENT EMAIL:')],
            [sg.InputText(key='clientEmail', readonly=True, disabled_readonly_background_color='#68868c', default_text=clientes.iloc[contador]['correoelectronico'])],
            [sg.Column(layout=[[sg.Button('PREVIOUS', key='previousClient', size=(10,1)), sg.Text(f'{contador + 1} of {maxItems}',key='clientCount'),sg.Button('NEXT', key='nextClient', size=(10,1))]])],
            [sg.Button('BACK TO MENU', key='backMenu', size=(20,1))]

        ], element_justification='c')
        ]
    ]
]

window = sg.Window('SHOW CLIENT', layout, size=(700,330), element_justification='c',icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))


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
    elif event == 'backMenu':
        window.close()  
        subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuClientes.py')])