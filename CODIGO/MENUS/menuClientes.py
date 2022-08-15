import os
from pathlib import Path
import sys
import subprocess
import PySimpleGUI as sg


path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

absolutepath = os.path.abspath(__file__)

def launchClientesCrear():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\CLIENTS\\createClient.py')])

def launchClientesMostar():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\CLIENTS\\showClient.py')])

# def launchClientesEliminar():
#     subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuProductos.py')])


layout = [[
    [sg.Text('CLIENTS', font=('Any 17 underline'))],
    [sg.VPush()],
    [sg.Button('CREATE CLIENT', key='createClient', size=(40,1))],
    [sg.Button('SHOW CLIENT', key='showClient', size=(40,1))],
    [sg.Button('DELETE CLIENT', key='menuProveedores', size=(40,1))],
    [sg.VPush()]
],[
    [sg.Button('GO BACK', key='goBack', size=(20,1))],
]
]


window = sg.Window('CLIENTS', layout, size=(600,250), element_justification='c')


while True:             
    event, values = window.read()
    
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'createClient':
        launchClientesCrear()
    elif event == 'showClient':
        launchClientesMostar()
    # elif event == 'menuProveedores':
    #     launchClientesEliminar()
    # elif event == 'goBack':
    #     goBack()
