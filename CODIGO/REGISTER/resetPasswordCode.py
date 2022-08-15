from ctypes.wintypes import SIZE
import sqlite3
import subprocess
from sys import argv
import PySimpleGUI as sg
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


absolutepath = os.path.abspath(__file__)

print(*argv)


sg.theme('DarkAmber')  

layout = [  
            [sg.Text('RESET PASSWORD', font=('Any 17 underline'))],
            [sg.Text('CODE:')],[sg.InputText(key='code', justification='center')],
            [sg.Text('NEW PASSWORD:')],[sg.InputText(key='newpass', justification='center', password_char='*')],
            [sg.Text('CONFIRM NEW PASSWORD:')],[sg.InputText(key='renewpass', justification='center', password_char='*')],
            [sg.Button('RESET PASSWORD', key='SEND REQUEST', size=(20,1))]
        ]


def resetPassword():

    code = argv[1]
    user = argv[2]

    if code == values['code']:
        if not values['newpass'] == '' and not values['renewpass'] == '':
            if values['newpass'] == values['renewpass']:
                try:
                    sqliteConnection = sqlite3.connect(os.path.join(absolutepath, '..\\..\\..\\CODIGO\\BD\\emz.db'))
                    print(sqliteConnection)
                    cursor = sqliteConnection.cursor()
                    print("Connected to SQLite")

                    sqlite_updateUser_query = """UPDATE usuarios set password = '%s' where username = '%s';"""

                    sqlite_updateUser_query = sqlite_updateUser_query % ( values['newpass'], user)
                    print(sqlite_updateUser_query)

                    cursor.execute(sqlite_updateUser_query)
                    sqliteConnection.commit()

                    sg.popup("Contraseña cambiada correctamente", icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))

                    cursor.close()

                    return True

                except Exception as ex:
                    sg.popup("ERROR", icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))
                    return False
        else:
            sg.popup("FALTAN CAMPOS", icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))
    else:
        sg.popup("EL CODIGO NO COINCIDE CON EL RECIBIDO", icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))


def launchLogin():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\LOGIN\\login.py')])

def launchresetPassword():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\REGISTER\\resetPassword.py')])


# Create the Window
window = sg.Window('Reset Password', layout, element_justification='c', icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))

# Event Loop to process "events" and get the "values" of the inputs
while True:             # Event Loop
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'BACK TO LOGIN':
        window.close()
        launchLogin()
    elif event == 'SEND REQUEST':
        salida = resetPassword()
        if salida:
            window.close()
            launchLogin()
        else:
            window.close()
            resetPassword()

window.close()