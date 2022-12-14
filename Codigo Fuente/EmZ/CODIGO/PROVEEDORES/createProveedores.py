import io
import os
import shutil
import sqlite3
import subprocess
import PySimpleGUI as sg
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))





from CODIGO.LOGS import logs
from CODIGO.BD import queryFunctions


sg.theme('DarkGrey6')

absolutepath = os.path.abspath(__file__)
folderpath = os.path.dirname(absolutepath)

bd = os.path.join(absolutepath, '..\\..\\..\\CODIGO\\BD\\emz.db')


        
def limpiarCampos():
            
    window['providerName'].update("")
    window['providerCif'].update("")
    window['providerNumber'].update("")
    window['providerMail'].update("")
    window['providerAddress'].update("")
    window['providerBank'].update("")


def insertDBValues(datos):
    try:
        sqliteConnection = sqlite3.connect(bd)
        cursor = sqliteConnection.cursor()
        
        sqlite_select_query = "INSERT INTO proveedores (nombre, cif, telefono, email, direccion, cuentabanco) values ( '%s','%s','%s','%s','%s','%s' )" % (datos[0],datos[1],datos[2],datos[3],datos[4],datos[5])

        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        cursor.close()
        
    except Exception as ex:
        print(str(ex))


layout = [[
    [
        sg.Text('CREATE PROVIDER', font=('Any 17 underline'))
    ],[
        sg.Column(layout=[
            [sg.Text('NAME:')],
            [sg.InputText(key='providerName')],
            [sg.Text('CIF:')],
            [sg.InputText(key='providerCif')],
            [sg.Text('PHONE NUMBER:')],
            [sg.InputText(key='providerNumber')],
            [sg.Text('EMAIL:')],
            [sg.InputText(key='providerMail', enable_events=True)],
            [sg.Text('ADDRESS:')],
            [sg.InputText(key='providerAddress')],
            [sg.Text('BANK ACCOUNT:')],
            [sg.InputText(key='providerBank')],
            [sg.Button("ADD PROVIDER", key='addProvider', size=(20,1))]
        ], element_justification='c')
    ],
    [
        sg.Button("BACK TO MENU", key='backMenu', size=(20,1), pad=(10,10,10,1))
    ]
]]

window = sg.Window('CREATE PROVIDER', layout, size=(700,440), element_justification='c',icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))

while True:             
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()

        
        
    elif event == "addProvider":
        
        datos = [values['providerName'], values['providerCif'], values['providerNumber'], values['providerMail'], values['providerAddress'] , values['providerBank']]
        
        if (
            values['providerName'] == '' or
            values['providerCif'] == '' or
            values['providerNumber'] == '' or
            values['providerMail'] == '' or
            values['providerAddress'] == '' or
            values['providerBank'] == ''    
        ):
            sg.Popup('Error!', 'All text fields must be filled')
        
        else:
            try:             
                insertDBValues(datos)
                
                sg.Popup('Done!', 'Provider correctly added')
                
                limpiarCampos()
                
            except Exception as ex:
                logs.error(ex.args)
        
    elif event == 'backMenu':
        window.close()
        subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuProveedores.py')])