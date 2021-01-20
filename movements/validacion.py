from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import datetime, date, time


class Validacion(FlaskForm):
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    from_currency = StringField ("from_currency", validators = [DataRequired()])
    from_quantity = StringField('from_quantity', validators=[DataRequired()])
    to_currency = StringField ("to_currency", validators = [DataRequired()])
    to_quantity = StringField("to_quantity", validators=[DataRequired()])
    submit = SubmitField("Aceptar")