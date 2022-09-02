import os
from pathlib import Path
import sys
import subprocess
import PySimpleGUI as sg

sg.theme('DarkGrey6')

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

absolutepath = os.path.abspath(__file__)

def launchCrear():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\PRODUCTOS\\createProduct.py')])

def launchMostar():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\PRODUCTOS\\showProducts.py')])

def launchEliminar():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\PRODUCTOS\\deleteProducts.py')])

def goBack():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENU\\mainMenu.py')])


layout = [[
    [sg.Text('PRODUCTS', font=('Any 17 underline'))],
    [sg.VPush()],
    [sg.Button('CREATE PRODUCT', key='createProduct', size=(40,1))],
    [sg.Button('SHOW PRODUCT', key='showProduct', size=(40,1))],
    [sg.Button('DELETE PRODUCT', key='deleteProduct', size=(40,1))],
    [sg.VPush()]
],[
    [sg.Button('GO BACK', key='goBack', size=(20,1))],
]
]


window = sg.Window('PRODUCTS', layout, size=(600,250), element_justification='c',icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))


while True:             
    event, values = window.read()
    
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'createProduct':
        window.close()
        launchCrear()
    elif event == 'showProduct':
        window.close()
        launchMostar()
    elif event == 'deleteProduct':
        window.close()
        launchEliminar()
    elif event == 'goBack':
        window.close()
        goBack()
