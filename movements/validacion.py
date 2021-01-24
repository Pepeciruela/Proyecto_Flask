from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Length
from datetime import datetime, date, time
import requests

class Validacion(FlaskForm):
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    from_currency = SelectField ('from_currency', choices= [('BTC','BTC'),('ETH','ETH'),('XRP','XRP'),('LTC','LTC'),('BCH','BCH'),('BNB','BNB'),('USTD','USTD'),('EOS','EOS'),('BSV','BSV'),('XLM','XLM'),('ADA','ADA'),('TRX','TRX')], validators = [DataRequired()])
    from_quantity = SelectField ('from_quantity', choices= [('BTC','BTC'),('ETH','ETH'),('XRP','XRP'),('LTC','LTC'),('BCH','BCH'),('BNB','BNB'),('USTD','USTD'),('EOS','EOS'),('BSV','BSV'),('XLM','XLM'),('ADA','ADA'),('TRX','TRX')], validators=[DataRequired()])
    to_currency = FloatField ("to_currency", validators = [DataRequired()])
    to_quantity = StringField('to_quantity')
    submit = SubmitField("Aceptar")