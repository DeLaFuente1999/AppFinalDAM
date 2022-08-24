import subprocess
import PySimpleGUI as sg
import io
import os
from pathlib import Path
import sys

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
absolutepath = os.path.abspath(__file__)


from CODIGO.BD import queryFunctions

def eliminarProveedor(proveedor, nombreProveedor):
    salidaComprobacionProductos = queryFunctions.selectBD('SELECT * FROM PRODUCTOS WHERE proveedorCif = (SELECT cif FROM proveedores where nombre = "%s")' % nombreProveedor)
    
    if len(salidaComprobacionProductos) > 0:
        sg.Popup('Provider can not be delete while has referenced products')
    else:
        queryFunctions.updateBD('DELETE FROM proveedores WHERE idproovedor = %s' % proveedor)

def getValores():
    return queryFunctions.selectBD('SELECT idproovedor as ID, nombre as NAME, cif as CIF, telefono as PHONE, email as EMAIL, direccion as ADDRESS, cuentabanco as ACCOUNT FROM proveedores')


valores = queryFunctions.selectBD('SELECT idproovedor as ID, nombre as NAME, cif as CIF, telefono as PHONE, email as EMAIL, direccion as ADDRESS, cuentabanco as ACCOUNT FROM proveedores')

sg.theme('DarkGrey6')

layout = [
    [sg.Table(key='table', headings=list(valores), auto_size_columns=True, expand_x=True,justification='c', values=valores.values.tolist())],
    [sg.Column(layout=[[sg.Button('DELETE', key='deleteOne', size=(20,1)),sg.Button('DELETE ALL', key='deleteAll', button_color=('black', 'red'),size=(20,1))]])],
    [sg.Button('BACK TO MENU', key='backToMenu', size=(20,1))]
]

window = sg.Window('DELETE PROVIDER', layout, size=(800,280), element_justification='c',icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))

while True:             
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'deleteOne':
        try:
            if len(values['table']) != 0:
                eliminarProveedor(getValores().values.tolist()[values['table'][0]][0], getValores().values.tolist()[values['table'][0]][1])
                window['table'].update(getValores().values.tolist())
            else:
                sg.Popup('You must select one provider on the table')
        except Exception as ex:
            print(ex)
    elif event == 'deleteAll':
        salida = sg.popup_yes_no('Do you want to delete all? This action can not be undone', title='Delete All')
        if salida == 'Yes':
            queryFunctions.updateBD('DELETE FROM PROVEEDORES')
            window['table'].update(getValores().values.tolist())

    elif event == 'backToMenu':
        window.close()
        subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuProveedores.py')])