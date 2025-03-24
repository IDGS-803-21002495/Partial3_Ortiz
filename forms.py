from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, DateField, validators, PasswordField

class DeliveryForm(Form):
    nombre = StringField('nombre',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=70, message='Ingrese un nombre válido')
    ])
    direccion = StringField('direccion',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=120, message='Ingrese una dirección válido')
    ])
    telefono = StringField('telefono',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=10, message='Ingrese un número telefonico válido')
    ])
    numero_pizzas = IntegerField('numero_pizzas',[
        validators.number_range(min=1,message='Campo no válido')
    ])

class UserForm(Form):
    Usuario = StringField('Usuario',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=3, max=20, message='Ingrese un nombre de usuario válido')
    ])
    Contraseña = PasswordField('Contraseña',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=30, message='Ingrese una contraseña válida')
    ])