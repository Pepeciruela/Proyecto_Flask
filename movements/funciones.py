from movements import app
import sqlite3




def consulta(query, params=()):
    DB_FILE = app.config["DB_FILE"]
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

def monedas_inicio():
    criptomonedas = ('EUR','BTC','ETH','XRP','LTC','BCH','BNB','USTD','EOS','BSV','XLM','ADA','TRX')
    monedas = consulta("SELECT DISTINCT to_currency FROM criptomonedas;")
    lista_monedas = []
    if not monedas:
        lista_monedas.append('EUR')
    else:
        for moneda in monedas:
            for k,v in moneda.items():
                lista_monedas.append(v)
        if not "EUR" in lista_monedas:
            lista_monedas.append('EUR')
    return lista_monedas
    
def monedas_invertidas():
    monedas_disponibles = {'EUR': 300000 ,'BTC': 0,'ETH': 0,'XRP': 0,'LTC': 0,'BCH': 0,'BNB': 0,'USTD': 0,'EOS': 0,'BSV': 0,'XLM': 0,'ADA': 0,'TRX': 0}
    lista_movimientos = consulta('SELECT * FROM criptomonedas')
    
    for movimiento in lista_movimientos:
        monedas_disponibles[movimiento['from_currency']] = monedas_disponibles[movimiento['from_currency']] - movimiento['from_quantity']
        monedas_disponibles[movimiento['to_currency']] = monedas_disponibles[movimiento['to_currency']] + movimiento['to_quantity']
    
    return monedas_disponibles 

def euros_invertidos():
    monedas_disponibles = {'EUR': 0 ,'BTC': 0,'ETH': 0,'XRP': 0,'LTC': 0,'BCH': 0,'BNB': 0,'USTD': 0,'EOS': 0,'BSV': 0,'XLM': 0,'ADA': 0,'TRX': 0}
    lista_movimientos = consulta('SELECT * FROM criptomonedas')
    
    for movimiento in lista_movimientos:
        monedas_disponibles[movimiento['from_currency']] = monedas_disponibles[movimiento['from_currency']] + movimiento['from_quantity']
    
    return monedas_disponibles     