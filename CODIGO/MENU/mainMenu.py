import PySimpleGUI as sg
import subprocess
import os



absolutepath = os.path.abspath(__file__)

def launchMenuClientes():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuClientes.py')])

def launchMenuProveedores():
    subprocess.call(['python', os.path.join(absolutepath, '..\\MENUS\\menuProveedores.py')])

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
        launchMenuProductos()
    elif event == 'menuProveedores':
        launchMenuProveedores()
    elif event == 'menuFacturas':
        print(1)