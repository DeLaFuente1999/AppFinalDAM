import os
from pathlib import Path
import sys
import subprocess
import PySimpleGUI as sg

sg.theme('DarkGrey6')

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

absolutepath = os.path.abspath(__file__)

def launchClientesCrear():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\CLIENTS\\createClient.py')])

def launchClientesMostar():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\CLIENTS\\showClient.py')])

def launchClientesEliminar():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\CLIENTS\\deleteClients.py')])

def goBack():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENU\\mainMenu.py')])


layout = [[
    [sg.Text('CLIENTS', font=('Any 17 underline'))],
    [sg.VPush()],
    [sg.Button('CREATE CLIENT', key='createClient', size=(40,1))],
    [sg.Button('SHOW CLIENT', key='showClient', size=(40,1))],
    [sg.Button('DELETE CLIENT', key='deleteClient', size=(40,1))],
    [sg.VPush()]
],[
    [sg.Button('GO BACK', key='goBack', size=(20,1))],
]
]


window = sg.Window('CLIENTS', layout, size=(600,250), element_justification='c',icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))


while True:             
    event, values = window.read()
    
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'createClient':
        window.close()
        launchClientesCrear()
    elif event == 'showClient':
        window.close()
        launchClientesMostar()
    elif event == 'deleteClient':
        window.close()
        launchClientesEliminar()
    elif event == 'goBack':
        window.close()
        goBack()
