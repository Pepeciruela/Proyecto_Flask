from flask import render_template, request, url_for, redirect
from movements import app
import sqlite3

DB_FILE = app.config["DB_FILE"]

@app.route('/')
def index():
    return "Inicio"

@app.route("/purchase")
def compra_venta():
    return "compra y venta de criptomonedas"

@app.route("/status")
def estado_inversion():
    return "estado de las inversiones"