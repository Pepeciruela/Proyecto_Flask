from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date
from datetime import datetime

def today(form, field):
    today = date.today()
    

class Validacion(FlaskForm):
    date = StringField ("Fecha", validators = [DataRequired()])
    time = StringField ("Hora", validators = [DataRequired()])
    from_currency = StringField ("from_currency", validators = [DataRequired()])
    from_quantity = StringField('from_quantity', validators=[DataRequired()])
    to_currency = StringField ("to_currency", validators = [DataRequired()])
    to_quantity = StringField("to_quantity", validators=[DataRequired()])
    submit = SubmitField("Aceptar")
   