import sqlite3
from movements import app

def crear_bd():
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    try:
        cursor.execute(CREATE TABLE IF NOT EXISTS criptomonedas(
                id INTEGER PRIMARY KEY NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                from_currency INTEGER NOT NULL,
                from_quantity REAL NOT NULL,
                to_currency INTEGER NOT NULL,
                to_quantity REAL NOT NULL,
                p_u REAL NOT NULL,);
                       
    except sqlite3.OperationalError:
        print("La tabla de criptomonedas ya existe.")
    else:
        print("La tabla de Criptomonedas se ha creado correctamente.")
    
    conexion.close()