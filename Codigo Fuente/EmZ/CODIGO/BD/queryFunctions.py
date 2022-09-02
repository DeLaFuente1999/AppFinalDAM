import os
import sqlite3
import pandas as pd

absolutepath = os.path.abspath(__file__)
folderpath = os.path.dirname(absolutepath)

bd = os.path.join(folderpath, 'emz.db')

def selectBD(query):
    con = sqlite3.connect(bd)
    
    salida=pd.read_sql(query, con)

    con.close()
    
    return salida

def updateBD(query):
    con = sqlite3.connect(bd)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()
    






    
