import sqlite3
import subprocess
import PySimpleGUI as sg
import os
import tempfile


absolutepath = os.path.abspath(__file__)
bd = os.path.join(absolutepath, '..\\..\\..\\CODIGO\\BD\\emz.db')
tempFolder = tempfile.gettempdir()

sg.theme('DarkAmber')

def loginApp():
    try:
        sqliteConnection = sqlite3.connect(bd)
        print(sqliteConnection)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")


        sqlite_select_query = """SELECT username, password, tipouser FROM USUARIOS where username = "%s" AND password = "%s" """
        sqlite_select_query = sqlite_select_query % (values['usernameText'], values['passwordText'])
        print(sqlite_select_query)


        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()


        if len(records) > 0:
            sg.popup("Bienvenido, %s" % values['usernameText'])
                        
            if os.path.isfile(os.path.join(tempFolder, 'login.txt')):            
                f = open(os.path.join(tempFolder, 'login.txt'), "w")
                f.write(str(records[0][2]))
                f.close()
            else:
                f = open(os.path.join(tempFolder, 'login.txt'), "x")
                f.write(str(records[0][2]))
                f.close()
            
            
            window.close()
            subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENU\\mainMenu.py')])

        else:
            sg.popup("Error, usuario o contraseña incorrectos")
 
        cursor.close()

    except Exception as ex:
        print(str(ex))


def launchRegister():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\REGISTER\\register.py')])

def launchResetPassword():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\REGISTER\\resetPassword.py')])

layout = [  
            [sg.Text('E MANAGEMENT Z', font=('Any 17 underline'))],
            [sg.Text('USERNAME:')],[sg.InputText(key='usernameText', justification='center')],
            [sg.Text('PASSWORD:')], [sg.InputText(password_char='*', key='passwordText', justification='center')],
            [sg.Button('LOGIN', key=loginApp, size=(20,1),pad=((0,0),(10,20)))],
            [sg.Button("REGISTER", size=(20,1))],
            [sg.Button('RESET PASSWORD', size=(20,1))]
        ]

# Create the Window
window = sg.Window('Login', layout, element_justification='c')

# Event Loop to process "events" and get the "values" of the inputs

while True:             
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == "REGISTER":
        window.close()
        launchRegister()
    elif event == "RESET PASSWORD":
        window.close()
        launchResetPassword()

window.close()
