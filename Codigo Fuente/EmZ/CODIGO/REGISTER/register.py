import sqlite3
# import CODIGO.LOGS.logs as lg
import subprocess
import PySimpleGUI as sg
import os

from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
from CODIGO.BD import queryFunctions


absolutepath = os.path.abspath(__file__)

listaAdminKeys = ["superduperadmin", "adminincreible", "megasuperadmin"]

# userQuestion.index(values['questionSecurityText']) -> Nos da el index de la pregunta para insertar en la base de datos

sg.theme('DarkGrey6')

def createUser():
    if values['nameText'] == '' or values['surnameText'] == '' or values['usernameText'] == '' or values['passwordText'] == '' or values['emailText'] == '':
        sg.popup("All fields must be filled except Admin Key field", title="Blank fields detected!", icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))
    else:
        try:
            sqliteConnection = sqlite3.connect(os.path.join(absolutepath, '..\\..\\..\\CODIGO\\BD\\emz.db'))
            cursor = sqliteConnection.cursor()

            sqlite_getUser_query = """SELECT * FROM USUARIOS WHERE username = '%s' or correo = '%s'"""
            
            salidagetuser = queryFunctions.selectBD(sqlite_getUser_query % (values['usernameText'], values['emailText']))
                        
            if len(salidagetuser) > 0:
                sg.Popup('This username or mail aready exists')
            else:
                try:
                    cursor.execute(sqlite_getUser_query % (values['usernameText'], values['emailText']))
                    records = cursor.fetchall()

                    if len(records) == 0:
                        sqlite_createUser_query = """INSERT INTO USUARIOS (nombre, apellidos, username, password, correo, 
                        tipouser) VALUES ('%s', '%s', '%s', '%s', '%s', %s) """
                        
                        if values['adminKey'] in listaAdminKeys:
                            valorAdmin = 1
                        else:
                            valorAdmin = 2

                        sqlite_createUser_query = sqlite_createUser_query % (values['nameText'],values['surnameText'],values['usernameText'], values['passwordText'], values['emailText'], valorAdmin)

                        cursor.execute(sqlite_createUser_query)

                        sqliteConnection.commit()
                        cursor.close() 

                        sg.popup("User created, %s" % (values['nameText'] + ' ' + values['surnameText'] + ' (' + values['usernameText'] + ')'), icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))
                        
                except Exception as ex:
                    # lg.error(ex)
                    print(ex)

        except Exception as ex:
            print(str(ex))


def launchLogin():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\LOGIN\\login.py')])

    
layout = [  [sg.Text('REGISTER', font=('Any 17 underline'))],
            [sg.Text('NAME:')],[sg.InputText(key='nameText', justification='center')],
            [sg.Text('SURNAME:')],[sg.InputText(key='surnameText', justification='center')],
            [sg.Text('USERNAME:')],[sg.InputText(key='usernameText', justification='center')],
            [sg.Text('PASSWORD:')], [sg.InputText(password_char='*', key='passwordText', justification='center')],
            [sg.Text('CORREO:')], [sg.InputText(key='emailText', justification='center')],
            [sg.Text('ADMIN KEY:')],[sg.InputText(key='adminKey', justification='center')],
            [sg.Button('CREATE USER', key=createUser, size=(20,1))],
            [sg.Button('BACK TO LOGIN', size=(20,1))]]




if __name__ == '__main__':
    # Create the Window
    window = sg.Window('Register', layout, element_justification='c', icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))


    # Event Loop to process "events" and get the "values" of the inputs
    while True:             # Event Loop
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if callable(event):
            event()
        elif event == 'CREATE USER':
            createUser()
        elif event == 'BACK TO LOGIN':
            window.close()
            launchLogin()


    window.close()   