from email.policy import default
import io
import os
import shutil
import sqlite3
import subprocess
from turtle import color
import PySimpleGUI as sg
from PIL import Image
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
import pandas as pd
absolutepath = os.path.abspath(__file__)

from CODIGO.LOGS import logs
from CODIGO.BD import queryFunctions

sg.theme('DarkGrey6')

try:
    proveedores = queryFunctions.selectBD('SELECT * FROM proveedores')
    
    if proveedores.empty:
        proveedores = {'nombre': ['NO DATA'], 'cif': ['NO DATA'], 'telefono': ['NO DATA'],'email': ['NO DATA'], 'direccion': ['NO DATA'], 'cuentabanco': ['NO DATA']}
        proveedores = pd.DataFrame(proveedores)        


except Exception as ex:
    sg.Popup('Error retrieving providers from database')
    
    
maxItems = len(proveedores)
contador = 0


def showNextProvider():
    global contador
    global proveedores
    if (contador + 1) != maxItems:
        contador = contador + 1
        
    window['providerName'].update(proveedores.iloc[contador]['nombre'])
    window['providerCif'].update(proveedores.iloc[contador]['cif'])
    window['providerPhone'].update(proveedores.iloc[contador]['telefono'])
    window['providerMail'].update(proveedores.iloc[contador]['email'])
    window['providerAddress'].update(proveedores.iloc[contador]['direccion'])
    window['providerAccount'].update(proveedores.iloc[contador]['cuentabanco'])
    
def showLastProvider():
    global contador
    if (contador) != 0:
        contador = contador - 1
        
    window['providerName'].update(proveedores.iloc[contador]['nombre'])
    window['providerCif'].update(proveedores.iloc[contador]['cif'])
    window['providerPhone'].update(proveedores.iloc[contador]['telefono'])
    window['providerMail'].update(proveedores.iloc[contador]['email'])
    window['providerAddress'].update(proveedores.iloc[contador]['direccion'])
    window['providerAccount'].update(proveedores.iloc[contador]['cuentabanco'])
    
layout = [[
    [
        sg.Text('SHOW PROVIDER', font=('Any 17 underline'))
    ],[
        sg.Column(layout=[
            [sg.Text('PROVIDER NAME:')],
            [sg.InputText(key='providerName', readonly=True, disabled_readonly_background_color='#68868c', use_readonly_for_disable=True, default_text=proveedores.iloc[contador]['nombre'])],
            [sg.Text('PHONE NUMBER:')],
            [sg.InputText(key='providerCif' , disabled_readonly_background_color='#68868c', readonly=True, default_text=proveedores.iloc[contador]['cif'])],
            [sg.Text('CLIENT ADDRESS:')],
            [sg.InputText(key='providerPhone', disabled_readonly_background_color='#68868c', readonly=True, default_text=proveedores.iloc[contador]['telefono'])],
            [sg.Text('CLIENT EMAIL:')],
            [sg.InputText(key='providerMail', disabled_readonly_background_color='#68868c', readonly=True, default_text=proveedores.iloc[contador]['email'])],
            [sg.Text('CLIENT EMAIL:')],
            [sg.InputText(key='providerAddress', disabled_readonly_background_color='#68868c', readonly=True, default_text=proveedores.iloc[contador]['direccion'])],
            [sg.Text('CLIENT EMAIL:')],
            [sg.InputText(key='providerAccount', disabled_readonly_background_color='#68868c', readonly=True, default_text=proveedores.iloc[contador]['cuentabanco'])],
            [sg.Column(layout=[[sg.Button('PREVIOUS', key='previousProvider', size=(10,1)), sg.Text(f'{contador + 1} of {maxItems}',key='providerCount'),sg.Button('NEXT', key='nextProvider', size=(10,1))]])],
        ], element_justification='c')
        ],
        [
            sg.Button('BACK TO MENU', key='backMenu', size=(20,1), pad=(10,10,10,1))
        ]
    ]
]

window = sg.Window('SHOW PROVIDERS', layout, size=(700,450), element_justification='c',icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))


while True:             
    

    
    event, values = window.read()
    
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'nextProvider':
        showNextProvider()
        window['providerCount'].update(f'{contador + 1} of {maxItems}')
    elif event == 'previousProvider':
        showLastProvider()
        window['providerCount'].update(f'{contador + 1} of {maxItems}')
    elif event == 'backMenu':
        window.close()
        subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuProveedores.py')])