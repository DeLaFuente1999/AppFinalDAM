import PySimpleGUI as sg
import subprocess
import os
import tempfile

tempFolder = tempfile.gettempdir()
admin = False

sg.theme('DarkGrey6')

absolutepath = os.path.abspath(__file__)

try:
    if os.path.isfile(os.path.join(tempFolder, 'login.txt')):
        f = open(os.path.join(tempFolder, 'login.txt'), "r")
        salida = f.read(1)
        admin = True if salida == '1' else False
except Exception as ex:
    print(ex)

def launchMenuClientes():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuClientes.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

def launchMenuProveedores():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuProveedores.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

def launchMenuProductos():
    subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuProductos.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)


layout = [
    [sg.Text('MAIN MENU', font=('Any 17 underline'))],
    [sg.VPush()],
    [sg.Button('CLIENTS', key='menuClientes', size=(40,1))],
    [sg.Button('PRODUCTS', key='menuProductos', size=(40,1))],
    [sg.Button('PROVIDERS', key='menuProveedores', size=(40,1))],
    [sg.Button('INVOICES', key='menuFacturas', size=(40,1))],
    [sg.VPush()]
]

layoutAdmin = [
    [sg.Text('MAIN MENU', font=('Any 17 underline'))],
    [sg.VPush()],
    [sg.Button('CLIENTS', key='menuClientes', size=(40,1))],
    [sg.Button('PRODUCTS', key='menuProductos', size=(40,1))],
    [sg.Button('PROVIDERS', key='menuProveedores', size=(40,1))],
    [sg.Button('INVOICES', key='menuFacturas', size=(40,1))],
    [sg.Button('USERS', key='usuarios', size=(40,1))],
    [sg.VPush()]
]


if __name__ == '__main__':

    if admin == True:
        window = sg.Window('MAIN MENU', layoutAdmin, size=(600,280), element_justification='c',icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))
    else:
        window = sg.Window('MAIN MENU', layout, size=(600,250), element_justification='c',icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))



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
            window.close()
            subprocess.call(['python', os.path.join(absolutepath, '..\\..\\FACTURAS\\facturas.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        elif event == 'usuarios':
            window.close()
            subprocess.call(['python', os.path.join(absolutepath, '..\\..\\USERS\\users.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)