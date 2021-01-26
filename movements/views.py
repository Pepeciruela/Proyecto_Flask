from flask import render_template, request, url_for, redirect
from movements import app
from movements.validacion import Validacion
import sqlite3
from datetime import date
from requests import Request, Session
import json

DB_FILE = app.config["DB_FILE"]
API_KEY = '8c547a52-a34e-4549-9dd2-90fe0266d0af'

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

@app.route('/')
def index():
    
    operaciones = consulta("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, id FROM criptomonedas;") #De la función consulta, llamamos a los parámteros que precisamos
    
    return render_template ("index.html", datos = operaciones, title = "Movimientos de compra y venta de Criptomonedas") #Devolver en pantalla la información solicitada

@app.route("/purchase", methods=["GET", "POST"])
def compra_venta():
    if request.method == 'GET':
        criptomonedas = ('EUR','BTC','ETH','XRP','LTC','BCH','BNB','USTD','EOS','BSV','XLM','ADA','TRX')
        monedas = consulta("SELECT DISTINCT to_currency FROM criptomonedas;")
        print (monedas[0])
        lista_monedas = []
        for moneda in monedas:
            for k,v in moneda:
                print (v)
            
                
            
            
        
        validacion = Validacion()
        validacion.to_currency.choices = monedas
        
        
        return render_template('compra_criptos.html', validacion = validacion)
        
        
        
    """if request.method == "POST":
        validacion = Validacion()
        
        validacion.from_currency.choices = [request.validacion.get('from_currency')]
        validacion.to_currency.choices = [request.validacion.get('to_currency')]
        #monedero --> hacer una funcion para calcular las moneadas disponibes con un select
        
        if request.validacion.get('submit') == 'Aceptar' and validacion.validate():
            try:
                consulta("INSERT INTO criptomonedas(date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?, ?, ?);", 
                        (request.validacion.get('date'), 
                        request.validacion.get('time'), 
                        request.validacion.get('from_currency'), 
                        request.validacion.get('from_quantity'),
                        request.validacion.get('to_currency'), 
                        request.validacion.get('to_quantity')
                        ))
                return redirect(url_for("index")) #Si todos los datos están validados y son correctos, muestramelos en la función de inicio
            except:
                return redirect(url_for("index")) #Si todos los datos están validados y son correctos, muestramelos en la función de inicio
        else:
            
            amount = request.validacion.get('from_quantity')
            symbol = request.validacion.get('from_currency')  
            convert = request.validacion.get('to_currency')
            API_KEY = '8c547a52-a34e-4549-9dd2-90fe0266d0af'
            
            
            try:
                url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(amount,symbol,convert,API_KEY)
                respuesta = requests.get(url)
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                else: 
                    print ('Error', respuesta.status)
                    
                to_quantity = datos['data']['quote'][convert]['price']
                precio_unidad = float(amount)/to_quantity
                
                return render_template ("compra_criptos.html", validacion = validacion, to_quantity = to_quantity, precio_unidad = precio_unidad) #Sino es un POST se sale y vuelve a la pagina de creación de altas
            except:
                return render_template ('compra_criptos.html', validacion=validacion)"""
    
    