import io
import os
import shutil
import sqlite3
import PySimpleGUI as sg
from PIL import Image
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))





from CODIGO.LOGS import logs
from CODIGO.BD import queryFunctions


sg.theme('DarkGrey6')

absolutepath = os.path.abspath(__file__)
folderpath = os.path.dirname(absolutepath)

bd = os.path.join(absolutepath, '..\\..\\..\\CODIGO\\BD\\emz.db')


def getProviderValues():
    valoresProveedores = queryFunctions.selectBD('SELECT * FROM PROVEEDORES')
    
    datos = []
    
    for i in valoresProveedores.itertuples(index=False):
        datos.append(f"Nombre:{i[1]}, CIF:{i[2]}")

    return datos

def setImagen(imagen):
    mywidth = 250
    
    img = Image.open(imagen)
    wpercent = (mywidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((mywidth,hsize))
    bio = io.BytesIO()
    img.save(bio, format="PNG") 
    del img
    
    return bio.getvalue()
        
        
def limpiarCampos():
            
    window['productName'].update("")
    window['productReference'].update("")
    window['productPrice'].update("")
    window['productDescription'].update("")
    window['providerName'].update("")
    
    imagenBase = setImagen(os.path.join(folderpath, '..\\..\\RESOURCES\\BaseImages\\BaseImageProducts.jpg'))
    window['imagen'].update(data=imagenBase)

def insertDBValues(datos):
    try:
        sqliteConnection = sqlite3.connect(bd)
        print(sqliteConnection)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        

        sqlite_select_query = "INSERT INTO productos (nombre, descripcion, proveedorCif, referencia, precio, image) values ( '%s','%s','%s','%s',%s,'%s' )" % (datos[0],datos[1],datos[2],datos[3],datos[4],datos[5])
        print(sqlite_select_query)

        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        cursor.close()
        
        print('INSERTADO CON EXITO')

    except Exception as ex:
        print(str(ex))


layout = [[
    [
        sg.Text('CREATE PRODUCT', font=('Any 17 underline'))
    ],[
        sg.Column(layout=[
            [sg.Text('PRODUCT NAME:')],
            [sg.InputText(key='productName')],
            [sg.Text('PRODUCT REFERENCE:')],
            [sg.InputText(key='productReference')],
            [sg.Text('PROVIDER NAME:')],
            [sg.Combo(key='providerName', values=getProviderValues(), size=(43,1), readonly=True)],
            [sg.Text('UNIT PRICE:')],
            [sg.InputText(key='productPrice', enable_events=True)],
            [sg.Text('DESCRIPTION:')],
            [sg.InputText(key='productDescription')],
            [sg.Button("ADD PRODUCT", key='addProduct', size=(20,1))]
        ], element_justification='c')
        ,sg.Column(layout=[
            [sg.Image(source=setImagen(os.path.join(folderpath, '..\\..\\RESOURCES\\BaseImages\\BaseImageProducts.jpg')), key='imagen',size=(250,250), )],
            [sg.FileBrowse(button_text='SELECT IMAGE', key='test', enable_events=True)]
            ], element_justification='c')
        ]
    ]
]

window = sg.Window('CREAR PRODUCTO', layout, size=(700,400), element_justification='c')

while True:             
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
        
    elif event == 'productPrice' and values['productPrice'] and values['productPrice'][-1] not in ('0123456789.'):
        window['productPrice'].update(values['productPrice'][:-1])
        
    elif event == "test":
                
        imagen = setImagen(values['test'])
        
        window['imagen'].update(data=imagen)
        
        
    elif event == "addProduct":
        
        datos = [values['productName'], values['productDescription'], values['providerName'].split(',')[1].strip().split(':')[1], values['productReference'], int(values['productPrice']) ,str(values['test'].split('/')[-1:])[2:-2]]
        
        if (
            values['productName'] == '' or
            values['productReference'] == '' or
            values['productPrice'] == '' or
            values['productDescription'] == '' or
            values['providerName'] == ''
           
        ):
            sg.Popup('Error!', 'All text fields must be filled')
        
        else:
            try:
                if str(values['test'].split('/')[-1:])[2:-2] != '':
                    shutil.copyfile(values['test'], os.path.join(folderpath, '..\\..\\DATA\\') + str(values['test'].split('/')[-1:])[2:-2])
                
                insertDBValues(datos)
                
                sg.Popup('Done!', 'Product correctly added')
                
                limpiarCampos()
                
            except Exception as ex:
                logs.error(ex.args)
        
