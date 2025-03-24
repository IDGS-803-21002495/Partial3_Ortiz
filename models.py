from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import datetime
db = SQLAlchemy()

# tabla de pedidos
class Pedido(db.Model):
    __tablename__='pedidos'
    id=db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(70))
    direccion = db.Column(db.String(120))
    telefono = db.Column(db.String(10))
    total = db.Column(db.Integer)
    fecha_pedido = db.Column(db.DateTime,default = datetime.datetime.now)

# tabla de usuarios
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String(255), nullable= False)
    nombre = db.Column(db.String(75))

    # generar hash de contraseña
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # verificar que la contraseña es correcta
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # obtener id
    def get_id(self):
        return str(self.id)
