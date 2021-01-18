from flask import render_template, request, url_for, redirect
from movements import app
import sqlite3

DB_FILE = app.config["DB_FILE"]

def consulta(query, params =()):
    
    #CONECTAMOS CON LA BASE DE DATOS
    conn = sqlite3.connect(DB_FILE)
    #CREAR EL CURSOS
    c = conn.cursor() 
    #EJECUTAR LOS DATOS ESTABLECIDOS EN EL DATA BASE
    c.execute(query, params)
    #SALVAR LOS CAMBIOS
    conn.commit()
    #RECUPERAMOS LAS FILAS
    filas = c.fetchall()
    #CERRAMOS LA CONEXION
    conn.close()
    
    if len(filas) == 0:
        return filas
    
    nombreColumnas = []
    for nombreColumna in c.description: #c.description proporciona los nombres de columna de la última consulta
        nombreColumnas.append(nombreColumna[0]) #añadimos la posición 0 de las columnas que hemos consultado
        
    diccionarios_consulta = []
    
    for fila in filas:
        d = {}
        for ix, nombreColumna in enumerate(nombreColumnas):
            d[nombreColumna] = fila[ix]
        diccionarios_consulta.append(d)
        
    return diccionarios_consulta

@app.route('/')
def index():
    
    #Seleccionamos los datos a extraer de la función consulta
    operaciones = consulta("SELECT date, time, from_currency, form_quantity, to_currency, to_quantity, id FROM criptomonedas;") #De la función consulta, llamamos a los parámteros que precisamos
    
    return render_template ("index.html", datos = operaciones, title = "Movimientos de compra y venta de Criptomonedas") #Devolver en pantalla la información solicitada

@app.route("/purchase", methods=["GET", "POST"])
def compra_venta():
    
    """validacion = validacionMovimientos()"""
    
    """if request.method == "POST": #Si envio información sin ser visible para el usuario
        if validacion.validate(): #Validamos los parámetros que se le van a pasar
            consulta ("INSERT INTO movimientos(date, time, from_currency, form_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?, ?, ?);",(
                validacion.date.data,
                validacion.time.data,
                validacion.from_currency.data,
                validacion.form_quality.data,
                validacion.to_currency.data,
                validacion.to_quantity.data,
            ))
            return redirect(url_for("index")) #Si todos los datos están validados y son correctos, muestramelos en la función de inicio
        else:
            return render_template ("compra_criptos.html", validacion = validacion) #Sino vuelve a la página de creación de altas"""
        
    return render_template ("compra_criptos.html") #Sino es un POST se sale y vuelve a la pagina de creación de altas
        
        

"""@app.route("/status")
def estado_inversion():
    return "estado de las inversiones
    """