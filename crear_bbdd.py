import sqlite3
from sqlite3 import Error

DB_FILE = 'database.db'

tabla = 'CREATE TABLE IF NOT EXISTS criptomonedas(\
                id INTEGER PRIMARY KEY NOT NULL,\
                date TEXT NOT NULL,\
                time TEXT NOT NULL,\
                from_currency INTEGER NOT NULL,\
                from_quantity REAL NOT NULL,\
                to_currency INTEGER NOT NULL,\
                to_quantity REAL NOT NULL,\
                p_u REAL NOT NULL);'


def crear_tabla():
    conexion = sqlite3.connect(DB_FILE)
    cursor = conexion.cursor()
    
    try:
        cursor.execute(tabla)                      
    except sqlite3.OperationalError:
        print("La tabla de criptomonedas ya existe.")
    else:
        print("La tabla de Criptomonedas se ha creado correctamente.")
        
    conexion.commit()
    conexion.close()

    print("Has creado tu tabla")
    
crear_tabla()