from pathlib import Path
import subprocess
import PySimpleGUI as sg
import os
import sys

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
absolutepath = os.path.abspath(__file__)
from CODIGO.BD import queryFunctions


clientes = list(queryFunctions.selectBD('SELECT NOMBRE FROM CLIENTES')['nombre'])
providers = queryFunctions.selectBD('SELECT nombre, cif FROM PROVEEDORES')
providersCombo = list(providers['nombre']) 
item = []
productos = []

def getItems(nombre):
    nombre = list(providers.loc[providers['nombre']==nombre]['cif'])[0]

    valor = queryFunctions.selectBD('SELECT nombre, precio FROM productos where proveedorCif = "%s"' % nombre)
    return valor.values.tolist()    



listaDatos = []

layout = [
    [sg.Text('INVOICES', font=('Any 17 underline'))],
    [sg.Column(layout=[     
        [sg.Text('CLIENT')],
        [sg.Combo(values=clientes, size=(37,1), key='clientesCombo')],
        [sg.Text('PROVIDER')],
        [sg.Combo(values=providersCombo,size=(37,1), enable_events=True, key='providersCombo')],
        [sg.Column(layout=[
            [sg.Text('ITEM')],
            [sg.Table(headings=['NAME', 'PRICE'],key='items', values=item , justification='c',auto_size_columns=False, col_widths=(20,9))]
        ])],
        [sg.Column(layout=[
            [sg.Button('ADD ITEM TO LIST', key='addItemToList', size=(20,1))]
            ], element_justification='c')]

    ]),
    sg.Column(layout=[[sg.Text('LIST OF ITEMS')],
        [sg.Table(headings=['NAME', 'PRICE','QUANTITY'],key='items2', values=item, justification='c' , auto_size_columns=False,col_widths=(20,9,9))],
        [sg.Button('DELETE ONE',key='deleteOne', size=(20,1)), sg.Button('DELETE', key='delete', size=(20,1))]
    ], element_justification='c')
    ],
    [sg.Button('CREATE INVOICE', key='createInvoice', size=(20,1))],
    [sg.Button('BACK TO MENU',key='backToMenu', size=(20,1), pad=(10,10,10,1))]
]



# Create the Window
window = sg.Window('Invoices', layout, size=(700,500),element_justification='c', icon=os.path.join(absolutepath, '..\\..\\..\\RESOURCES\\AppIcon\\icon.ico'))


# Event Loop to process "events" and get the "values" of the inputs
while True:             # Event Loop
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'providersCombo':
        print(values['providersCombo'])
        items1 = getItems(values['providersCombo'])
        window['items'].update(items1)
        productos = []
        window['items2'].update(productos)
    elif event == 'addItemToList':
        if len(values['items']) == 0:
            sg.Popup('You must select one item to delete')
        else:
            if len(productos) == 0:
                productos.append([items1[values['items'][0]][0],items1[values['items'][0]][1],1])
            else:
                for i in productos:
                    if i[0] == items1[values['items'][0]][0]:
                        i[2] = i[2] + 1
                        i[1] = items1[values['items'][0]][1] * i[2]
                        break
                else:
                    productos.append([items1[values['items'][0]][0],items1[values['items'][0]][1],1])
            window['items2'].update(productos)
        
    elif event == 'deleteOne':
        if len(values['items2']) == 0:
            sg.Popup('You must select one item to delete')
        else:
            productos[values['items2'][0]][1] = productos[values['items2'][0]][1] - items1[values['items2'][0]][1]
            productos[values['items2'][0]][2] = productos[values['items2'][0]][2] - 1
            window['items2'].update(productos)
        
    elif event == 'delete':
            if len(values['items2']) == 0:
                sg.Popup('You must select one item to delete')
            else:
                productos.remove(productos[values['items2'][0]])
                window['items2'].update(productos)

    elif event == 'backToMenu':
        window.close()
        subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENU\\mainMenu.py')])
        
    elif event == 'createInvoice':
        if values['providersCombo'] != None and values['clientesCombo'] != None and len(values['items2']) != 0:
            print(1)
        else:
            sg.Popup('Client, Provider and at least 1 product are required!')