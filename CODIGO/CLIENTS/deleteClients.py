import subprocess
import PySimpleGUI as sg
import io
import os
from pathlib import Path
import sys

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

absolutepath = os.path.abspath(__file__)

from CODIGO.BD import queryFunctions

def eliminarCliente(cliente):
    queryFunctions.updateBD('DELETE FROM clientes WHERE idcliente = %s' % cliente)

def getValores():
    return queryFunctions.selectBD('SELECT idcliente as ID, nombre as NOMBRE, telefono AS TELEFONO, correoelectronico AS EMAIL, direccion AS DIRECCION FROM clientes')

sg.theme('DarkGrey6')

layout = [
    [sg.Table(key='table' , headings=list(getValores()), select_mode=sg.TABLE_SELECT_MODE_BROWSE ,auto_size_columns=True, expand_x=True,justification='c', values=getValores().values.tolist())],
    [sg.Column(layout=[[sg.Button('DELETE', key='deleteOne', size=(20,1)),sg.Button('DELETE ALL', key='deleteAll', button_color=('black', 'red'),size=(20,1))]])],
    [sg.Button('BACK TO MENU', key='backToMenu', size=(20,1))]
]

window = sg.Window('DELETE PROVIDER', layout, size=(800,280), element_justification='c')

while True:   
    window.refresh()          
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'deleteOne':
        try:
            eliminarCliente(getValores().values.tolist()[values['table'][0]][0])
            window['table'].update(getValores().values.tolist())
        except Exception as ex:
            print(ex)
    elif event == 'deleteAll':
        print('Eliminar todos')
        salida = sg.popup_yes_no('Do you want to delete all? This action can not be undone', title='Delete All')
        print(salida)
        if salida == 'Yes':
            queryFunctions.updateBD('DELETE FROM CLIENTES')
            window['table'].update(getValores().values.tolist())

    elif event == 'backToMenu':
        print('Back to menu')
        window.close()
        subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuClientes.py')])

        