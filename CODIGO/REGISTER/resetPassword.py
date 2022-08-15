import sqlite3
import subprocess
import PySimpleGUI as sg
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime as dt
import random
import string

from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
from CODIGO.BD import queryFunctions


absolutepath = os.path.abspath(__file__)
bd = os.path.join(absolutepath, '..\\..\\..\\CODIGO\\BD\\emz.db')


sg.theme('DarkGrey6')  


def randomCodeGenerate():

    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for i in range(7))
    return code


def changePassword(email, pwd, pwdNew1, pwdNew2):
    
    if not email == '' or pwd == '' or pwdNew1 == '' or pwdNew2 == '':
        if pwdNew1 == pwdNew2:
            sqlite_updatePassword_query = 'UPDATE usuarios SET password = "' + pwdNew1 + '" WHERE correo = "' + email + '" AND password = "' + pwd + '"'
            print( sqlite_updatePassword_query)

            queryFunctions.updateBD(sqlite_updatePassword_query)
            
            sg.popup("Password changed for user")
        else:
            sg.popup("New passwords don't match")
    else:
        sg.popup("All fields must be filled")



def sendPassResetRequest(username, code, mail):

    if not username == '' or code == '' or mail == '':

        try:
            sqliteConnection = sqlite3.connect(bd)
            print(sqliteConnection)
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")


            sqlite_select_query = """select * from usuarios where username = "%s" and correo = "%s" """
            sqlite_select_query = sqlite_select_query % (username, mail)
            print(sqlite_select_query)

            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()

            if len(records) > 0:
                try:
                    mail_content = """
                    <!DOCTYPE html>
                        <html>
                            <head>
                                <meta charset="utf-8">
                                <title>E MANAGEMENT Z</title> 
                            </head>
                            <body>
                                <header>
                                    <h1>E MANAGEMENT Z</h1>
                                    <h3>PASSWORD REPLACEMENT:</h3>
                                </header>
                            
                                <main>
                                    <p>Hi!</p>
                                    <p>This is a mail automatically sended from E Management Z, do not reply.</p>
                                    <p>The user %s has requested a new password.</p>
                                    <p>The code to recover the password is:</p>
                                    <p>%s</p>
                                    <p>The date of this request is %s</p>
                                    <p>If you did not requested the new password, call an administrator inmediatly</p>
                                    <p>Thanks</p>
                                </main>
                            </body>
                        </html>
                    """ % (username, code ,dt.datetime.today().strftime("%d/%m/%Y %H:%M"))

                    #The mail addresses and password
                    sender_address = 'managemententerprisez@gmail.com'
                    sender_pass = 'osdvqguqnkzpdnov'
                    receiver_address = str(mail)

                    #Setup the MIME
                    message = MIMEMultipart()
                    message['From'] = sender_address
                    message['To'] = receiver_address
                    message['Subject'] = 'PASSWORD CHANGE REQUEST.'   #The subject line

                    #The body and the attachments for the mail
                    message.attach(MIMEText(mail_content, 'html'))

                    #Create SMTP session for sending the mail
                    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
                    session.starttls() #enable security
                    session.login(sender_address, sender_pass) #login with mail_id and password
                    text = message.as_string()
                    session.sendmail(sender_address, receiver_address, text)
                    session.quit()


                    launchResetPassCode(code=code, username=username)

                except Exception as ex:
                    print(ex)

            else:
                sg.popup("User %s does not exists or does not match with the email" % username)
                launchResetPassword()
                
            cursor.close()

        except Exception as ex:
            print(ex)


layout = [  
            [sg.Text('CHANGE PASSWORD', font=('Any 17 underline'))],
            [sg.Text('EMAIL:')],[sg.InputText(key='emailChange', justification='center')],
            [sg.Text('OLD PASSWORD:')],[sg.InputText(key='oldpass', justification='center', password_char='*')],
            [sg.Text('NEW PASSWORD:')],[sg.InputText(key='newpass', justification='center', password_char='*')],
            [sg.Text('CONFIRM NEW PASSWORD:')],[sg.InputText(key='renewpass', justification='center', password_char='*')],
            [sg.Button('RESET PASSWORD' ,key='resetPwd', size=(20,1))],
            [sg.Text('RESET PASSWORD', font=('Any 17 underline'), pad=((0,0),(40,0)))],
            [sg.Text('USERNAME:')],[sg.InputText(key='username', justification='center')],
            [sg.Text('EMAIL:')],[sg.InputText(key='email', justification='center')],
            [sg.Button('SEND EMAIL', size=(20,1))],
            [sg.Button('BACK TO LOGIN', size=(20,1), pad=((0,0),(30,10)))]        
        ]


def launchLogin():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\LOGIN\\login.py')])

def launchResetPassword():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\REGISTER\\resetPassword.py')])

def launchResetPassCode(code, username):
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\REGISTER\\resetPasswordCode.py'), code, username])



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
    elif event == 'resetPwd':
        changePassword(values['emailChange'], values['oldpass'], values['newpass'], values['renewpass'])
        window.close()
        launchLogin()
    elif event == 'SEND EMAIL':
        code = randomCodeGenerate()
        window.close()
        sendPassResetRequest(values['username'], code, mail=values['email'])


window.close()