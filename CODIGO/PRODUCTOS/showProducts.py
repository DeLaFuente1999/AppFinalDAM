from email.policy import default
from genericpath import isfile
import subprocess
import pandas as pd
import io
import os
import shutil
import sqlite3
from turtle import color
import PySimpleGUI as sg
from PIL import Image
from pathlib import Path
import sys

from numpy import product
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

absolutepath = os.path.abspath(__file__)
folderpath = os.path.dirname(absolutepath)
folderpath2 = os.path.dirname(absolutepath)

from CODIGO.LOGS import logs
from CODIGO.BD import queryFunctions

sg.theme('Dark Amber')

try:
    productos = queryFunctions.selectBD('SELECT * FROM productos')
    if productos.empty:
        productos = {'nombre': ['NO DATA'], 'descripcion': ['NO DATA'], 'referencia': ['NO DATA'],'precio': ['NO DATA'], 'image': ['NO DATA'], 'proveedorCif': ['NO DATA']}
        productos= pd.DataFrame(productos)        

except Exception as ex:
    sg.Popup('Error al recuperar los productos de la base de datos')
    
    
maxItems = len(productos)
contador = 0
print(contador)

def setImagen(imagen):
    mywidth = 250
    if isfile(imagen):  
        img = Image.open(imagen)
        wpercent = (mywidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((mywidth,hsize))
        bio = io.BytesIO()
        img.save(bio, format="PNG") 
        del img
        
        return bio.getvalue()
    else:
        img = Image.open(os.path.join(folderpath, '..\\..\\RESOURCES\\BaseImages\\BaseImageProducts.jpg'))
        wpercent = (mywidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((mywidth,hsize))
        bio = io.BytesIO()
        img.save(bio, format="PNG") 
        del img
        
        return bio.getvalue()

def showNextProduct():
    global contador
    global productos
    if (contador + 1) == maxItems:
        print(maxItems)
    else:
        contador = contador + 1
        
    window['productName'].update(productos.iloc[contador]['nombre'])
    window['productDescription'].update(productos.iloc[contador]['descripcion'])
    window['productReference'].update(productos.iloc[contador]['referencia'])
    window['productPrize'].update(productos.iloc[contador]['precio'])
    window['productCif'].update(productos.iloc[contador]['proveedorCif'])
    window['imagen'].update(setImagen(os.path.join(folderpath, '..\\..\\DATA\\' + productos.iloc[contador]['image'])))

    print(contador)

def showLastProduct():
    global contador
    if (contador) == 0:
        print(0)
    else:
        contador = contador - 1

    window['productName'].update(productos.iloc[contador]['nombre'])
    window['productDescription'].update(productos.iloc[contador]['descripcion'])
    window['productReference'].update(productos.iloc[contador]['referencia'])
    window['productPrize'].update(productos.iloc[contador]['precio'])
    window['productCif'].update(productos.iloc[contador]['proveedorCif'])
    
    print(contador)

layout = [[
    [
        sg.Text('SHOW PRODUCT', font=('Any 17 underline'))
    ],[
        sg.Column(layout=[
            [sg.Text('PRODUCT NAME:')],
            [sg.InputText(key='productName', disabled_readonly_background_color='#705e52', readonly=True, use_readonly_for_disable=True, default_text=productos.iloc[contador]['nombre'])],
            [sg.Text('PRODUCT DESCRIPTION:')],
            [sg.InputText(key='productDescription', disabled_readonly_background_color='#705e52', readonly=True, default_text=productos.iloc[contador]['descripcion'])],
            [sg.Text('PRODUCT REFERENCE:')],
            [sg.InputText(key='productReference', disabled_readonly_background_color='#705e52', readonly=True, default_text=productos.iloc[contador]['referencia'])],
            [sg.Text('PRODUCT PRICE:')],
            [sg.InputText(key='productPrize', disabled_readonly_background_color='#705e52', readonly=True, default_text=productos.iloc[contador]['precio'])],
            [sg.Text('PRODUCT PROVIDER:')],
            [sg.InputText(key='productCif', disabled_readonly_background_color='#705e52', readonly=True, default_text=productos.iloc[contador]['proveedorCif'])],
            [sg.Column(layout=[[sg.Button('PREVIOUS', key='previousProduct', size=(10,1)), sg.Text(f'{contador + 1} of {maxItems}',key='productCount'),sg.Button('NEXT', key='nextProduct', size=(10,1))]])],
        ], element_justification='c')
        ,sg.Column(layout=[
            [sg.Image(source=setImagen(os.path.join(folderpath, '..\\..\\DATA\\' + productos.iloc[contador]['image'])), key='imagen',size=(250,250), )]
            ], element_justification='c')
        ],
        [sg.Button('BACK TO MENU', key='backMenu', size=(20,1), pad=(10,10,10,1))]
        ],
        
    ]

window = sg.Window('SHOW PRODUCT', layout, size=(700,400), element_justification='c')


while True:             
    

    
    event, values = window.read()
    
    if event in (None, 'Exit'):
        break
    if callable(event):
        event()
    elif event == 'nextProduct':
        showNextProduct()
        window['productCount'].update(f'{contador + 1} of {maxItems}')
    elif event == 'previousProduct':
        showLastProduct()
        window['productCount'].update(f'{contador + 1} of {maxItems}')
    elif event == 'backMenu':
        window.close()
        subprocess.call(['python', os.path.join(absolutepath, '..\\..\\MENUS\\menuProductos.py')])