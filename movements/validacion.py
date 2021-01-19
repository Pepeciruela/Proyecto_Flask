from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date
from datetime import datetime

def today(form, field):
    today = date.today()
    

class Validacion(FlaskForm):
    date = DateField ("Fecha", validators = [DataRequired(), today])
    """time =
    from_currency
    from_quantity
    to_currency"""
    from_quantity = FloatField('Cantidad', validators=[DataRequired()])
    submit = SubmitField("Aceptar")