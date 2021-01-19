from flask import render_template, request, url_for, redirect
from movements import app
from movements.validacion import Validacion
from datetime import date
from datetime import datetime
import sqlite3

DB_FILE = app.config["DB_FILE"]

@app.route('/')
def index():
    #CONECTAMOS CON LA BASE DE DATOS
    conn = sqlite3.connect(DB_FILE)
    #CREAR EL CURSOS
    c = conn.cursor() 
    #EJECUTAR LOS DATOS ESTABLECIDOS EN EL DATA BASE
    c.execute("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, id FROM criptomonedas;")
    #SALVAR LOS CAMBIOS
    conn.commit()
    #RECUPERAMOS LAS FILAS
    data = c.fetchall()
    #CERRAMOS LA CONEXION
    conn.close()
    
    #Seleccionamos los datos a extraer de la función consulta
    """operaciones = consulta("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, id FROM criptomonedas;")""" #De la función consulta, llamamos a los parámteros que precisamos
    
    return render_template ("index.html", datos = data, title = "Movimientos de compra y venta de Criptomonedas") #Devolver en pantalla la información solicitada

@app.route("/purchase", methods=["GET", "POST"])
def compra_venta():
    
    if request.method == "POST": #Si envio información sin ser visible para el usuario
        date = request.form['date']
        time = request.form['time']
        from_currency = request.form['from_currency']
        from_quantity = request.form['from_quantity']
        to_currency = request.form['to_currency']
        to_quantity = request.form['to_quantity']
        #CONECTAMOS CON LA BASE DE DATOS
        conn = sqlite3.connect(DB_FILE)
        #CREAR EL CURSOS
        c = conn.cursor() 
        #EJECUTAR LOS DATOS ESTABLECIDOS EN EL DATA BASE
        c.execute("INSERT INTO criptomonedas(date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?, ?, ?)", (date, time, from_currency, from_quantity, to_currency, to_quantity))
        #SALVAR LOS CAMBIOS
        conn.commit()
        #RECUPERAMOS LAS FILAS
        data = c.fetchall()
        print (data)
        #CERRAMOS LA CONEXION
        conn.close()
        return redirect(url_for("index")) #Si todos los datos están validados y son correctos, muestramelos en la función de inicio
    else:
        return render_template ("compra_criptos.html") #Sino vuelve a la página de creación de altas
        
    return render_template ("compra_criptos.html") #Sino es un POST se sale y vuelve a la pagina de creación de altas"""
        
        

"""@app.route("/status")
def estado_inversion():
    return "estado de las inversiones
    """