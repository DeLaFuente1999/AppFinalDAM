import os
import datetime as dt

import sys
sys.path.insert(1, '.')

absolutepath = os.path.abspath(__file__)

date = dt.datetime.today().strftime("%d/%m/%Y %H:%M:%S")

def resetLogFile():
    """
    Funcion que se usa para limpiar el archivo de logs. Al lanzarla, vacia el contenido de este. 
    """
    f = open(os.path.join(absolutepath, '..\\..\\..\\CODIGO\\LOGS\\logs.log'), "w")
    f.write("")
    f.close()
    print("LOGS FILE WIPED")


def newExecution():
    """
    Funcion encargada de escribir un mensaje de log en el archivo cada vez que se ejecute la aplicacion. 
    """
    f = open(os.path.join(absolutepath, '..\\..\\..\\CODIGO\\LOGS\\logs.log'), "a")
    f.write(f"{date} - APP LAUNCH - WELCOME TO E MANAGEMENT Z \r")
    f.close()
    print(f"{date} - APP LAUNCH - WELCOME TO E MANAGEMENT Z")


def info(valor):
    """
    Informacion en archivo de logs. 
    """
    f = open(os.path.join(absolutepath, '..\\..\\..\\CODIGO\\LOGS\\logs.log'), "a")
    f.write(f"{date} - (INFORMATION) - {valor} \r")
    f.close()
    print(f"{date} - (INFORMATION) - {valor}")


def warning(valor):
    """
    Warning en archivo de logs. 
    """
    f = open(os.path.join(absolutepath, '..\\..\\..\\CODIGO\\LOGS\\logs.log'), "a")
    f.write(f"{date} - (WARNING) - {valor} \r")
    f.close()
    print(f"{date} - (WARNING) - {valor}")


def error(valor):
    """
    Error en archivo de logs. 
    """
    f = open(os.path.join(absolutepath, '..\\..\\..\\CODIGO\\LOGS\\logs.log'), "a")
    f.write(f"{date} - (ERROR) - {valor} \r")
    f.close()
    print(f"{date} - (ERROR) - {valor}")


def critico(valor):
    """
    Critico en archivo de logs. 
    """
    f = open(os.path.join(absolutepath, '..\\..\\..\\CODIGO\\LOGS\\logs.log'), "a")
    f.write(f"{date} - (CRITICAL) - {valor} \r")
    f.close()
    print(f"{date} - (CRITICAL) - {valor}")

