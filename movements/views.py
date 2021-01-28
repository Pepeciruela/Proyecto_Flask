from flask import render_template, request, url_for, redirect
from movements import app
from movements.validacion import Validacion
from datetime import datetime, date, time
import requests
import json
from movements.api import consulta_api
from movements.funciones import *

API_KEY = app.config["API_KEY"]

@app.route('/')
def index():
    operaciones = consulta("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, p_u, id FROM criptomonedas;") #De la función consulta, llamamos a los parámteros que precisamos
    
    return render_template ("index.html", datos = operaciones, title = "Movimientos de compra y venta de Criptomonedas") #Devolver en pantalla la información solicitada

@app.route("/purchase", methods=["GET", "POST"])
def compra_venta():
    if request.method == 'GET': # 1º Validamos las monedas disponibles para comprar
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
                    
        validacion = Validacion()
        validacion.from_currency.choices = lista_monedas

        return render_template('compra_criptos.html', validacion = validacion)
    #2º validar que para la casilla from_quantity, solo se pueda coger el valor existente de to_cuantity en las diferentes monedas y poner a EURO infinito
        
    else: # Si el metodo es POST
        validacion = Validacion()
        if request.form.get("submit") == "Aceptar" and validacion.validate(): # Si le damos a Aceptar guardamos los datos en la BBDD
            try:
                consulta("INSERT INTO criptomonedas(date, time, from_currency, from_quantity, to_currency, to_quantity, p_u) VALUES(?, ?, ?, ?, ?, ?, ?);", 
                        (datetime.now().strftime("%d/%m/%Y"), 
                        datetime.now().strftime("%H:%M:%S"), 
                        request.form.get("from_currency"), 
                        request.form.get("from_quantity"),
                        request.form.get("to_currency"), 
                        request.form.get("to_quantity"),
                        request.form.get("p_u"),
                        ))
                return redirect(url_for("index")) #Si todos los datos están validados y son correctos, muestramelos en la función de inicio
            except:
                return render_template ('compra_criptos.html', validacion=validacion)       
        else: # Si le damos a la calculadora, llamamos a la API
            amount = request.form.get('from_quantity')
            symbol = request.form.get('from_currency')  
            convert = request.form.get('to_currency')
            
            if symbol != convert: 
                try:
                    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(amount,symbol,convert,API_KEY)
                    respuesta = consulta_api(url) #Llamamos a la función de consuta de la API
                    
                    to_quantity = respuesta['data']['quote'][convert]['price'] # Sacamos el precio de conversión de la moneda a cambiar
                    
                    p_u = float(amount)/to_quantity # Sacamos el precio unitario dividiendo entre la cantidad
                    
                    return render_template ("compra_criptos.html", validacion = validacion, to_quantity = to_quantity, p_u = p_u) 
                except:
                    return render_template ('compra_criptos.html', validacion=validacion)
            else:
                return render_template ('compra_criptos.html', validacion=validacion)
                
    
    