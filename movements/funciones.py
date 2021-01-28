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
        criptomonedas_disponibles = ('EUR','BTC','ETH','XRP','LTC','BCH','BNB','USTD','EOS','BSV','XLM','ADA','TRX')
        operaciones = consulta("SELECT to_currency, to_quantity FROM criptomonedas;")
        lista_monedas = []
        lista_valores = []
        for operacion in operaciones:
            for k, v in operacion.items():
                if v in criptomonedas_disponibles:
                    lista_monedas.append(v)
                else:
                    lista_valores.append(v)
        
        diccionario_monedas = dict()
        for i in range (len(lista_monedas)):
            diccionario_monedas[lista_monedas[i]] = lista_valores[i]
            
        reserva_monedas = Counter(criptos_disponibles) + Counter(diccionario_monedas)    

    
    
    