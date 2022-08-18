import PySimpleGUI as sg
import subprocess
import os
import tempfile

tempFolder = tempfile.gettempdir()
admin = False


absolutepath = os.path.abspath(__file__)

try:
    if os.path.isfile(os.path.join(tempFolder, 'login.txt')):
        f = open(os.path.join(tempFolder, 'login.txt'), "r")
        salida = f.read(1)
        admin = True if salida == '1' else False
except Exception as ex:
    print(ex)

def launchMenuClientes():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuClientes.py')])

def launchMenuProveedores():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuProveedores.py')])

def launchMenuProductos():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuProductos.py')])


layout = [
    [sg.Text('MAIN MENU', font=('Any 17 underline'))],
    [sg.VPush()],
    [sg.Button('CLIENTES', key='menuClientes', size=(40,1))],
    [sg.Button('PRODUCTOS', key='menuProductos', size=(40,1))],
    [sg.Button('PROVEEDORES', key='menuProveedores', size=(40,1))],
    [sg.Button('FACTURAS', key='menuFacturas', size=(40,1))],
    [sg.VPush()]
]

layoutAdmin = [
    [sg.Text('MAIN MENU', font=('Any 17 underline'))],
    [sg.VPush()],
    [sg.Button('CLIENTES', key='menuClientes', size=(40,1))],
    [sg.Button('PRODUCTOS', key='menuProductos', size=(40,1))],
    [sg.Button('PROVEEDORES', key='menuProveedores', size=(40,1))],
    [sg.Button('FACTURAS', key='menuFacturas', size=(40,1))],
    [sg.Button('USUARIOS', key='usuarios', size=(40,1))],
    [sg.VPush()]
]

if admin == True:
    window = sg.Window('MAIN MENU', layoutAdmin, size=(600,280), element_justification='c')
else:
    window = sg.Window('MAIN MENU', layout, size=(600,250), element_justification='c')



while True:             
    event, values = window.read()
    
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'menuClientes':
        window.close()
        launchMenuClientes()
    elif event == 'menuProductos':
        window.close()
        launchMenuProductos()
    elif event == 'menuProveedores':
        window.close()
        launchMenuProveedores()
    elif event == 'menuFacturas':
        print(1)