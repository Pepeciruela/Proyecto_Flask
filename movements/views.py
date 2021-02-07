from flask import render_template, request, url_for, redirect, flash
from movements import app
from movements.validacion import Validacion
from datetime import datetime, date, time
import requests
import json
from movements.api import consulta_api
from movements.funciones import * 
import re

API_KEY = app.config["API_KEY"]

@app.route('/')
def index():
    mensajes =[]
    try: 
        operaciones = consulta("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, p_u, id FROM criptomonedas;") #De la función consulta, llamamos a los parámteros que precisamos
    except Exception as e:
        print("**ERROR**: Acceso a base de datos - consulta registro operaciones: {} - {}". format(type(e).__name__, e))
        mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")  
        return render_template ("index.html", datos = [], title = "Movimientos de compra y venta de Criptomonedas", mensajes=mensajes) #Devolver en pantalla la información solicitada
    return render_template ("index.html", datos = operaciones, title = "Movimientos de compra y venta de Criptomonedas", mensajes=mensajes) #Devolver en pantalla la información solicitada

@app.route("/purchase", methods=["GET", "POST"])
def compra_venta():
    mensajes =[]
    validacion = Validacion()
    if request.method == 'GET': 
        try: 
            validar_monedas = monedas_inicio()
        except Exception as e:
            print("**ERROR**: Acceso a base de datos - consulta monedas disponibles al inicio: {} - {}". format(type(e).__name__, e))
            mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")           
            return render_template('compra_criptos.html', validacion = validacion, validar_monedas=[], mensajes=mensajes)
        
        validacion.from_currency.choices = validar_monedas
        
        return render_template('compra_criptos.html', validacion = validacion, validar_monedas=validar_monedas, mensajes=mensajes)
    
    else:
        try: 
            validar_monedas = monedas_inicio()
        except Exception as e:
            print("**ERROR**: Acceso a base de datos - consulta monedas disponibles al inicio: {} - {}". format(type(e).__name__, e))
            mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")
            return render_template('compra_criptos.html', validacion = validacion, validar_monedas=[], mensajes=mensajes)  
        validacion.from_currency.choices = validar_monedas
       
        if request.form.get('calculadora') == 'Calculadora' and validacion.validate:
            amount = request.form.get('from_quantity')
            validadores=('0','1','2','3','4','5','6','7','8','9','.')
            contador = 0
            for i in amount:
                if i == ',':
                    flash ("Utiliza '.' para separar los números decimales")
                    return render_template('compra_criptos.html', validacion = validacion, validar_monedas=[], mensajes=mensajes)
                elif i in validadores:
                    if i == '.':
                        contador = contador +1
                        if contador > 1:
                            flash ("Ese no es un numero valido. Por favor repita la operacion")
                            return render_template('compra_criptos.html', validacion = validacion, validar_monedas=[], mensajes=mensajes)
                        else:
                            pass                      
                else:
                    flash ("Ese no es un numero valido. Por favor repita la operacion")
                    return render_template('compra_criptos.html', validacion = validacion, validar_monedas=[], mensajes=mensajes) 

            symbol = request.form.get('from_currency')
            convert = request.form.get('to_currency')
                
            valor1 = [symbol]
            valor2 = [amount]
            
                
            comprobacion = dict(zip(valor1, valor2))
                
            try: 
                hucha = monedas_disponibles()
            except Exception as e:
                print("**ERROR**: Acceso a base de datos - validacion valor monedas: {} - {}". format(type(e).__name__, e))
                mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")
                return render_template('compra_criptos.html', validacion = validacion, validar_monedas=[], mensajes=mensajes) 
            
            monedas_saldo = {}
            for moneda in hucha:
                if hucha[moneda] > 0:
                    monedas_saldo[moneda] = hucha[moneda]
                            
            if symbol != convert:
                lista_comprobacion = list(comprobacion.items())
                lista_hucha = list(monedas_saldo.items())
                for clave in lista_comprobacion:
                    for otra_clave in lista_hucha:
                        if clave[0] == otra_clave[0]:
                            if float(clave[1]) <= float(otra_clave[1]):
                                print ("Hay dinero de sobra")
                                try: 
                                    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(amount,symbol,convert,API_KEY)
                                    try: 
                                        respuesta = consulta_api(url)
                                    except Exception as e:
                                        print("**ERROR**: Acceso a la API - intercambio de precio de las monedas: {} - {}". format(type(e).__name__, e))
                                        mensajes.append("Error en acceso a la API. Consulte con el administrador.")
                                        return render_template('compra_criptos.html', validacion = validacion, validar_monedas=[], mensajes=mensajes) 
                                               
                                    to_quantity = respuesta['data']['quote'][convert]['price']
                                    if convert == "EUR":
                                        to_quantity = round(to_quantity, 2)
                                    else:
                                        to_quantity = round(to_quantity, 8)
                                
                                                   
                                    p_u = float(amount)/to_quantity
                                    if convert == "EUR":
                                        p_u = round(p_u, 2)
                                    else:
                                        p_u = round(p_u, 8) 
                                                    
                                    return render_template ("compra_criptos.html", validacion = validacion, to_quantity = to_quantity, p_u = p_u) 
                                except:
                                    return render_template ('compra_criptos.html', validacion=validacion, validar_monedas = validar_monedas)
                            else:
                                flash("No tienes suficientes monedas para realizar esta compra")
                        
                                return render_template ('compra_criptos.html', validacion=validacion, validar_monedas = validar_monedas)
            else:
                flash("Las monedas deben ser diferentes")
                return render_template ('compra_criptos.html', validacion=validacion, validar_monedas = validar_monedas)
                    
        elif request.form.get('submit') == 'Aceptar' and validacion.validate:
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
                return redirect(url_for("index"))
            except Exception as e:
                print("**ERROR**: Acceso a la base de datos - introduccion de valores en tabla: {} - {}". format(type(e).__name__, e))
                mensajes.append("Error en acceso a la base de datos. Consulte con el administrador.")
                return render_template ('index', mensajes=mensajes)           
        else:
            try: 
                validar_monedas = monedas_inicio()
            except Exception as e:
                print("**ERROR**: Acceso a la base de datos - monedas disponibles: {} - {}". format(type(e).__name__, e))
                mensajes.append("Error en acceso a la base de datos. Consulte con el administrador.")
                return render_template ('compra_criptos.html', validacion=validacion, validar_monedas = [], mensajes=mensajes )
            validacion.from_currency.choices = validar_monedas
            vacio=True
            return render_template ('compra_criptos.html', validacion=validacion, validar_monedas = validar_monedas, vacio=vacio)
                              
@app.route("/status")
def estado_inversiones():
    mensajes = []
    if request.method == "GET":
        try:
            hucha = monedas_invertidas()
        except Exception as e:
            print("**ERROR**: Acceso a la base de datos - monedas inicio disponibles: {} - {}". format(type(e).__name__, e))
            mensajes.append("Error en acceso a la base de datos. Consulte con el administrador.")
            return render_template('estado_inversion.html', suma_saldo=[], suma_cotizacion=[], suma_invertidos=[], valor_actual=[], rentabilidad=[], mensajes=mensajes)
        monedas_saldo = {}
        for moneda in hucha:
            if hucha[moneda] > 0:
                monedas_saldo[moneda] = hucha[moneda]
                
        saldo= list(monedas_saldo.items())
        euros_saldo =[]
        for clave in saldo:
            if clave[0]== "EUR":
                euros_saldo.append(clave[1])
        
        suma_saldo = -300000
        for numero in euros_saldo:
            suma_saldo += numero
        
        monedas_consulta = list(monedas_saldo.items())
        monedas_cotizacion = []
        for clave in monedas_consulta:
            symbol = clave[0]
            amount = clave[1]
            convert = "EUR"
            
            if symbol != "EUR":
                url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(amount,symbol,convert,API_KEY)
                try: 
                    respuesta = consulta_api(url)
                except Exception as e:
                    print("**ERROR**: Acceso a la API - intercambio de precio de las monedas: {} - {}". format(type(e).__name__, e))
                    mensajes.append("Error en acceso a la API. Consulte con el administrador.")
                    return render_template('estado_inversion.html', suma_saldo=[], suma_cotizacion=[], suma_invertidos=[], valor_actual=[], rentabilidad=[], mensajes=mensajes)
                                                
                to_quantity = respuesta['data']['quote'][convert]['price']
                monedas_cotizacion.append(to_quantity)
        
        suma_cotizacion = 0
        for numero in monedas_cotizacion:
            suma_cotizacion += numero
            
        try: 
            hucha_euro = euros_invertidos()
        except Exception as e:
            print("**ERROR**: Acceso a la base de datos - monedas inicio disponibles: {} - {}". format(type(e).__name__, e))
            mensajes.append("Error en acceso a la base de datos. Consulte con el administrador.")
            return render_template('estado_inversion.html', suma_saldo=[], suma_cotizacion=[], suma_invertidos=[], valor_actual=[], rentabilidad=[], mensajes=mensajes)
        euros_saldo = {}
        euros_inversion = []
        for moneda in hucha_euro:
            if hucha_euro[moneda] > 0:
                euros_saldo[moneda] = hucha_euro[moneda]
                
        lista_euros = list(euros_saldo.items())
        for clave in lista_euros:
            if clave[0]== "EUR":
                euros_inversion.append(clave[1])
                
        suma_invertidos = 0
        for numero in euros_inversion:
            suma_invertidos += numero    
                
        valor_actual = suma_saldo + suma_cotizacion +  suma_invertidos
        
        if suma_saldo != 0:
            rentabilidad = 1-(suma_invertidos/valor_actual)        
        else:
            rentabilidad = 0       
    return render_template('estado_inversion.html', suma_saldo=suma_saldo, suma_cotizacion=suma_cotizacion, suma_invertidos=suma_invertidos, valor_actual=valor_actual, rentabilidad=rentabilidad)
    