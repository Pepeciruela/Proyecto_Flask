from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Length
from datetime import datetime, date, time
import requests

class Validacion(FlaskForm):
    criptomonedas = ['EUR','BTC','ETH','XRP','LTC','BCH','BNB','USTD','EOS','BSV','XLM','ADA','TRX']
    
    
    
    from_currency = SelectField ('From:', choices= criptomonedas, validators = [DataRequired()])
    to_currency = SelectField ('To:', choices= criptomonedas, validators=[DataRequired()])
    from_quantity = FloatField ('Q', validators = [DataRequired()])
    to_quantity = FloatField('Q')
    p_u = FloatField('P.U.')
    
    calculadora = SubmitField('Calculadora')
    
    submit = SubmitField('Aceptar')