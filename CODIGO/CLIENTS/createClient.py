import io
import os
import shutil
import sqlite3
import PySimpleGUI as sg
from PIL import Image
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from CODIGO.LOGS import logs
from CODIGO.BD import queryFunctions

sg.theme('DarkAmber')

absolutepath = os.path.abspath(__file__)
folderpath = os.path.dirname(absolutepath)

bd = os.path.join(absolutepath, '..\\..\\..\\CODIGO\\BD\\emz.db')

def limpiarCampos():
            
    window['clientName'].update("")
    window['clientPhone'].update("")
    window['clientAddress'].update("")
    window['clientEmail'].update("")


def insertDBValues(datos):
    try:
        sqliteConnection = sqlite3.connect(bd)
        print(sqliteConnection)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        

        sqlite_select_query = "INSERT INTO clientes (nombre, telefono, direccion, correoelectronico) values ( '%s','%s','%s','%s')" % (datos[0],datos[1],datos[2],datos[3])
        print(sqlite_select_query)

        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        cursor.close()
        
        print('INSERTADO CON EXITO')

    except Exception as ex:
        print(str(ex))


layout = [[
    [
        sg.Text('CREATE CLIENT', font=('Any 17 underline'))
    ],[
        sg.Column(layout=[
            [sg.Text('CLIENT NAME:')],
            [sg.InputText(key='clientName')],
            [sg.Text('PHONE NUMBER:')],
            [sg.InputText(key='clientPhone')],
            [sg.Text('CLIENT ADDRESS:')],
            [sg.InputText(key='clientAddress')],
            [sg.Text('CLIENT EMAIL:')],
            [sg.InputText(key='clientEmail')],
            [sg.Button("ADD CLIENT", key='addClient', size=(20,1))]
        ], element_justification='c')]
    ]
]

window = sg.Window('CREATE CLIENT', layout, size=(700,300), element_justification='c')

while True:             
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
         
    elif event == "addClient":
        
        datos = [values['clientName'], values['clientPhone'], values['clientAddress'], values['clientEmail']]
        
        if (
            values['clientName'] == '' or
            values['clientPhone'] == '' or
            values['clientAddress'] == '' or
            values['clientEmail'] == ''           
        ):
            sg.Popup('Error!', 'All text fields must be filled')
        
        else:
            try:

                insertDBValues(datos)
                
                sg.Popup('Done!', 'Client correctly added')
                
                limpiarCampos()
                
            except Exception as ex:
                logs.error(ex.args)
        
