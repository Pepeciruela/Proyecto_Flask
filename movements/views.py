from flask import render_template, request, url_for, redirect
from movements import app
from movements.validacion import Validacion
import sqlite3
from datetime import date

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

@app.route('/')
def index():
    
    operaciones = consulta("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, id FROM criptomonedas;") #De la función consulta, llamamos a los parámteros que precisamos
    
    return render_template ("index.html", datos = operaciones, title = "Movimientos de compra y venta de Criptomonedas") #Devolver en pantalla la información solicitada

@app.route("/purchase", methods=["GET", "POST"])
def compra_venta():
    
    validacion = Validacion()
    
    if request.method == "POST": #Si envio información sin ser visible para el usuario
        if validacion.validate:
            consulta("INSERT INTO criptomonedas(date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?, ?, ?);", 
                    (validacion.date, 
                    validacion.time, 
                    validacion.from_currency.data, 
                    validacion.from_quantity.data,
                    validacion.to_currency.data, 
                    validacion.to_quantity.data
                    ))
            return redirect(url_for("index")) #Si todos los datos están validados y son correctos, muestramelos en la función de inicio
        else:
            return render_template ("compra_criptos.html", validacion = validacion) #Sino vuelve a la página de creación de altas
            
    return render_template ("compra_criptos.html", validacion = validacion) #Sino es un POST se sale y vuelve a la pagina de creación de altas"""
            
        

"""@app.route("/status")
def estado_inversion():
    return "estado de las inversiones
    """