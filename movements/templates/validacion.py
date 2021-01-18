from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date

"""Validar fecha con el sistema """

class Validacion(FlaskForm):
    date = DateField ("Fecha", validators = [DataRequired]) 
    """time
    from_currency
    form_quantity
    to_currency
    to_quantity"""
    
    submit = SubmitField("Aceptar")