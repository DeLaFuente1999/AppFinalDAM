import pathlib
import sqlite3
import subprocess
import sys
import PySimpleGUI as sg
import os
import tempfile
from pathlib import Path

absolutepath = os.path.abspath(__file__)
absolutepath1 = str(pathlib.Path().resolve())

bd = os.path.join(absolutepath, '..\\CODIGO\\BD\\emz.db')

tempFolder = tempfile.gettempdir()

sg.theme('DarkGrey6')

def loginApp():
    try:

        sqliteConnection = sqlite3.connect(bd)
        cursor = sqliteConnection.cursor()

        sqlite_select_query = """SELECT username, password, tipouser FROM USUARIOS where username = "%s" AND password = "%s" """
        sqlite_select_query = sqlite_select_query % (values['usernameText'], values['passwordText'])

        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        if len(records) > 0:
            sg.popup("Welcome, %s" % values['usernameText'])
                        
            if os.path.isfile(os.path.join(tempFolder, 'login.txt')):            
                f = open(os.path.join(tempFolder, 'login.txt'), "w")
                f.write(str(records[0][2]))
                f.close()
            else:
                f = open(os.path.join(tempFolder, 'login.txt'), "x")
                f.write(str(records[0][2]))
                f.close()
            
            
            window.close()
            subprocess.run(['python', os.path.join(absolutepath1, 'CODIGO\\MENU\\mainMenu.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

        else:
            sg.popup("Error, incorrect user or password")
 
        cursor.close()

    except Exception as ex:
        print(str(ex))


def launchRegister():
    window.close()
    subprocess.run([ 'python', os.path.join(absolutepath1, 'CODIGO\\REGISTER\\register.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    
def launchResetPassword():
    subprocess.call(['python', os.path.join(absolutepath1, 'CODIGO\\REGISTER\\resetPassword.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

layout = [  
            [sg.Text('E MANAGEMENT Z', font=('Any 17 underline'))],
            [sg.Text('USERNAME:')],[sg.InputText(key='usernameText', justification='center')],
            [sg.Text('PASSWORD:')], [sg.InputText(password_char='*', key='passwordText', justification='center')],
            [sg.Button('LOGIN', size=(20,1),pad=((0,0),(10,20)))],
            [sg.Button("REGISTER", size=(20,1))],
            [sg.Button('RESET PASSWORD', size=(20,1))]
        ]

if __name__ == '__main__':

    # Create the Window
    window = sg.Window('Login', layout, element_justification='c',icon=os.path.join(absolutepath1, 'RESOURCES\\AppIcon\\icon.ico'))

    # Event Loop to process "events" and get the "values" of the inputs

    while True:             
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if callable(event):
            event()
        elif event == "LOGIN":
            loginApp()
        elif event == "REGISTER":
            launchRegister()
        elif event == "RESET PASSWORD":
            window.close()
            launchResetPassword()

    window.close()
