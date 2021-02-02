from movements import app
import sqlite3
from collections import Counter


DB_FILE = app.config["DB_FILE"]

def consulta(query, params=()):
    #CONECTAMOS CON LA BASE DE DATOS
    conn = sqlite3.connect(DB_FILE)
    #CREAR EL CURSOS
    c = conn.cursor() 
    #EJECUTAR LOS DATOS ESTABLECIDOS EN EL DATA BASE
    c.execute(query, params)
    #SALVAR LOS CAMBIOS
    conn.commit()
    #RECUPERAMOS LAS FILAS
    data = c.fetchall()
    #CERRAMOS LA CONEXION
    conn.close()

    if len(data) == 0: #Si la longitud de los datos es igual a 0, los retornamos vacio
        return data

    columnNames = [] 
    for columnName in c.description: # Devuelve una lista de tuplas que describen las columnas en un conjunto de resultados
        columnNames.append(columnName[0]) #Se las añadimos a columName

    listaDeDiccionarios = []

    for dato in data: #Para cada dato dentro de data
        d = {}
        for ix, columnName in enumerate(columnNames): #Enumerate agrega contador a un iterable y lo devuelve. El objeto devuelto es un objeto enumerado.
            d[columnName] = dato[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

def monedas_disponibles():
    criptos_disponibles = {'EUR': 100000 ,'BTC': 0,'ETH': 0,'XRP': 0,'LTC': 0,'BCH': 0,'BNB': 0,'USTD': 0,'EOS': 0,'BSV': 0,'XLM': 0,'ADA': 0,'TRX': 0}
    lista_movimientos = consulta('SELECT * FROM criptomonedas')
    
    for movimiento in lista_movimientos:
        criptos_disponibles[movimiento['from_currency']] = criptos_disponibles[movimiento['from_currency']] - movimiento['from_quantity']
        criptos_disponibles[movimiento['to_currency']] = criptos_disponibles[movimiento['to_currency']] + movimiento['to_quantity']
    
    return criptos_disponibles    

    
    