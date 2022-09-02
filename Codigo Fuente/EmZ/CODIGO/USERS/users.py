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

def eliminarCliente(usuario):
    queryFunctions.updateBD('DELETE FROM usuarios WHERE id = %s' % usuario)

def getValores():
    
    
    valoresSalida = queryFunctions.selectBD('SELECT id as ID, nombre as NAME, apellidos as SURNAME, correo as MAIL, username as USERNAME, password as PASSWORD, tipouser as ADMIN FROM usuarios')
    valoresSalida['ADMIN'] = valoresSalida['ADMIN'].replace(1, 'True')
    valoresSalida['ADMIN'] = valoresSalida['ADMIN'].replace(2, 'False')
   
    return valoresSalida


def processAction(nombre, id):
    if nombre == 'MODIFY USER':
        if id == -1:
            sg.popup('You must select a user on the table!')
        else:    
            queryupdate = 'UPDATE USUARIOS SET %s WHERE ID = %s'
            
            camposQuery = 'tipouser = %s' % 1 if values['tipouser'] == 'TRUE' else 'tipouser = 2'
            
            if values['nombre'] != '':
                camposQuery += ', nombre = "%s"' % values['nombre']
            
            if values['apellidos'] != '':
                camposQuery += ', apellidos = "%s"' % values['apellidos']
            
            if values['username'] != '':
                camposQuery += ', username = "%s"' % values['username']
            
            if values['correo'] != '':
                camposQuery += ', correo = "%s"' % values['correo']
            
            if values['password'] != '':
                camposQuery += ', password = "%s"' % values['password']

            queryupdate = queryupdate % (camposQuery, id)
            
            queryFunctions.updateBD(queryupdate)
                    
    elif nombre == 'ADD USER':
        if values['nombre'] != None and values['apellidos'] != None and  values['username'] != None and  values['password'] != None and  values['tipouser'] != None and  values['correo']  != None:
            try:
                queryInsert = 'INSERT INTO USUARIOS (NOMBRE, APELLIDOS, CORREO, USERNAME, PASSWORD, TIPOUSER) VALUES ("%s","%s","%s","%s","%s",%s)' % (values['nombre'], values['apellidos'], values['correo'] ,values['username'] ,values['password'] , 1 if values['tipouser'] == 'TRUE' else 2)
                queryFunctions.updateBD(queryInsert)
                sg.Popup('User added')
            except Exception as ex:
                sg.Popup('Error adding the user')
        else:
            sg.Popup('All fields must be filled')

sg.theme('DarkGrey6')

layout = [
    [sg.Table(key='table' , headings=list(getValores()), select_mode=sg.TABLE_SELECT_MODE_BROWSE ,auto_size_columns=True, expand_x=True,justification='c', values=getValores().values.tolist())],
    [sg.Button('DELETE', key='deleteOne', size=(20,1))],
    [
        sg.Column(key='valores', layout=[
            [sg.Text('NAME', justification='center', size=(40,1)), sg.Text('SURNAME', justification='center', size=(40,1))],
            [sg.InputText(key='nombre'), sg.InputText(key='apellidos')],
            [sg.Text('MAIL', justification='center', size=(40,1)), sg.Text('USERNAME', justification='center', size=(40,1))],
            [sg.InputText(key='correo'), sg.InputText(key='username')],
            [sg.Text('PASSWORD', justification='center', size=(40,1)), sg.Text('', justification='center', size=(40,1))],
            [sg.InputText(key='password'), sg.Combo(values=['TRUE', 'FALSE'], default_value='FALSE', size=(43,1), key='tipouser')],
        ])
    ],
    [
        sg.Column(key='valores2', layout=[
          [sg.Checkbox('MODIFY USER', key='modify',enable_events=True, default=True), sg.Checkbox('ADD USER',enable_events=True, key='add')],
        ])
                                           
    ],
    [sg.Button('MODIFY USER', key='processAction')],
    [sg.Button('BACK TO MENU', key='backToMenu', size=(20,1), pad=(10,10,10,1))]
]

window = sg.Window('USERS MANAGEMENT', layout, size=(800,510), element_justification='c',icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))

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

    elif event == 'backToMenu':
        window.close()
        subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENU\\mainMenu.py')])

    elif event == 'add':
        window['modify'].update(False)
        window['add'].update(True)
        window['processAction'].update('ADD USER')
    elif event == 'modify':
        window['modify'].update(True)
        window['add'].update(False)
        window['processAction'].update('MODIFY USER')
    elif event == 'processAction':        
        processAction(window['processAction'].get_text(), getValores().values.tolist()[values['table'][0]][0] if values['table'] else -1)
        window['table'].update(getValores().values.tolist())
