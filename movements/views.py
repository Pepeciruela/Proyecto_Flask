from flask import render_template, request, url_for, redirect
from movements import app
import sqlite3

DB_FILE = app.config["DB_FILE"]

def consulta(query, params =()):
    
    #CONECTAMOS CON LA BASE DE DATOS
    conn = sqlite3.connect(DB_FILE)
    #CREAR EL CURSOS
    c = conn.cursor() 
    #INSERTAR LOS DATOS ESTABLECIDOS EN EL DATA BASE
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
    operaciones = consulta("SELECT date, time, from_currency, form_quantity, to_currency, to_quantity, id FROM criptomonedas;")
    
    return render_template ("index.html", title = "Movimientos de compra y venta de Criptomonedas")

"""
@app.route("/purchase", methods=["GET", "POST"])
def compra_venta():
    if request.method == "POST":
        request.form[]
        
        return redirect(url_for("index"))

@app.route("/status")
def estado_inversion():
    return "estado de las inversiones
    """