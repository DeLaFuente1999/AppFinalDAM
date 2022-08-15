#!Archivo que sera el encargado de lanzar la aplicacion
import subprocess
import os
absolutepath = os.path.abspath(__file__)

if __name__ == '__main__':
    subprocess.call(['python', os.path.join(absolutepath, '\\TrabajoFinalDAM\\CODIGO\\LOGIN\\login.py')])
