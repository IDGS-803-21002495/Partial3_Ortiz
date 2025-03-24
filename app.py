from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_login import LoginManager, login_user, logout_user, login_required
import os, datetime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash
import forms
from models import db
from models import Pedido, Usuario


app = Flask(__name__)
csrf = CSRFProtect()
app.config.from_object(DevelopmentConfig)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Inicia sesión para acceder a esta página.'

# inicializar el archivo 
def iniciar_archivo():
    archivo = open('pedidos.txt', 'w')
    archivo.close()

# guardar el pedido en el archivo 
def guardar_pedido(pedido):
    archivo = open('pedidos.txt', 'r')
    # Leer las lineas del archivo para darle un ID a cada pedido
    lineas = archivo.readlines()
    id_pedido = len(lineas) + 1 
    archivo.close()

    archivo = open('pedidos.txt','a')
    pedido_str = f"ID: {id_pedido}, Nombre: {pedido['nombre']}, Direccion: {pedido['direccion']}, Telefono: {pedido['telefono']}, Tamanio: {pedido['tamanio']}, Ingredientes: {pedido['ingredientes']}, Numero de Pizzas: {pedido['numero_pizzas']}, Subtotal: {pedido['subtotal']}\n"
    archivo.write(pedido_str)
    archivo.close()  

# organizar los pedidos del archivo para mostrarlos en la tabla
def cargar_pedidos():
    pedidos = []
    archivo = open('pedidos.txt', 'r')
    for linea in archivo:
        datos = linea.strip().split(', ')
        pedido = {}
        for dato in datos:
            clave, valor = dato.split(': ', 1)
            pedido[clave] = valor
        pedidos.append(pedido)
    
    archivo.close()
    return pedidos

# Quitar pizza de la tabla de pedidos 
def eliminar_pedido(id_pedido):
    archivo = open('pedidos.txt', 'r')
    lineas = archivo.readlines()
    archivo.close()

    # escribir de nuevo pero sin la linea seleccionada 
    archivo = open('pedidos.txt','w')
    for linea in lineas:
        if f"ID: {id_pedido}" not in linea:
            archivo.write(linea)
    archivo.close()

# calcular el total del pedido
def calcular_total_pedido():
    archivo = open('pedidos.txt', 'r') 
    total = 0  

    for linea in archivo:
        datos = linea.strip().split(', ')
        subtotal = 0

        for dato in datos:
            if dato.startswith('Subtotal'):
                subtotal = int(dato.split(': ')[1])  

        total += subtotal 

    archivo.close()  
    return total  


# ver todos los pedidos hechos y filtrar por mes o día
@app.route("/ver_pedidos", methods=['GET', 'POST'])
@login_required
def ver_pedidos():
    create_form = forms.DeliveryForm(request.form)
    pedidos = Pedido.query.all()
    total_ventas = 0.0

    if request.method == 'POST':
        tipo_busqueda = request.form.get('tipo_busqueda')
        fecha_input = request.form.get('fecha')

        # buscar por día
        if tipo_busqueda == 'dia':
            pedidos = Pedido.query.filter(func.date(Pedido.fecha_pedido) == fecha_input).all()
        # buscar por mes
        if tipo_busqueda == 'mes':
            anio, mes, dia = fecha_input.split('-')
            pedidos = Pedido.query.filter(
                func.year(Pedido.fecha_pedido) == int(anio),
                func.month(Pedido.fecha_pedido) == int(mes)
            ).all()

    total_ventas = sum([pedido.total for pedido in pedidos])

    return render_template("ver_pedidos.html", form = create_form, pedidos = pedidos, total_ventas = total_ventas)

# generar un pedido nuevo
@app.route('/pedidos', methods=['GET', 'POST'])
@login_required
def pedidos():
    create_form = forms.DeliveryForm(request.form)
    
    if request.method == 'POST':
        if create_form.validate():
            # Recuperar los datos del formulario
            nombre = create_form.nombre.data
            direccion = create_form.direccion.data
            telefono = create_form.telefono.data
            numero_pizzas = int(create_form.numero_pizzas.data)
            tamanio = request.form.get('tamanio')
            ingredientes = request.form.getlist('ingredientes')

            # calcular subtotal
            precio_tamanio = int(tamanio)  # Chica=40, Mediana=80, Grande=120
            precio_ingredientes = len(ingredientes) * 10  # Cada ingrediente cuesta $10
            subtotal = (precio_tamanio + precio_ingredientes) * numero_pizzas

            # determinar el tamaño
            tamanio_presentacion = ''
            if tamanio == '40':
                tamanio_presentacion = 'Chica'
            elif tamanio == '80':
                tamanio_presentacion = 'Mediana'
            elif tamanio == '120':
                tamanio_presentacion = 'Grande'

            # crear el pedido
            pedido = {
                "nombre": nombre,
                "direccion": direccion,
                "telefono": telefono,
                "tamanio": tamanio_presentacion,
                "ingredientes": len(ingredientes),
                "numero_pizzas": numero_pizzas,
                "subtotal": subtotal
            }

            # guardar el pedido en el archivo
            guardar_pedido(pedido)

            
    # cargar los pedidos desde el archivo
    pedidos = cargar_pedidos() 
    return render_template('pedidos.html', form=create_form, pedidos=pedidos)

# eliminar una pedido (pizza) por ID
@app.route('/eliminar_pedido/<int:id_pedido>', methods=['POST','GET'])
@login_required
def eliminar(id_pedido):
    if request.method == 'POST': 
        eliminar_pedido(id_pedido)  
    create_form = forms.DeliveryForm(request.form)
    pedidos = cargar_pedidos()
    return render_template('pedidos.html', form=create_form, pedidos=pedidos)

# registrar un pedido en la base de datos 
@app.route('/registrar_pedido', methods=['GET', 'POST'])
@login_required
def registrar_pedido():
    create_form = forms.DeliveryForm(request.form)
    
    if request.method == 'POST' and create_form.validate():
        total = calcular_total_pedido()
        nombre = create_form.nombre.data
        direccion = create_form.direccion.data
        telefono = create_form.telefono.data

        # crear instancia del objeto pedido
        ped = Pedido(
            nombre=nombre,  
            direccion=direccion,
            telefono=telefono,
            total=total
        )

        # guardar en la base de datos
        db.session.add(ped)
        db.session.commit()

        # borrar registros del archivo de texto
        iniciar_archivo()

        # mostrar mensaje informando el total
        flash(f"Pedido registrado correctamente. Total a pagar: ${total}", "success")
        return redirect(url_for('ver_pedidos'))

    return render_template('pedidos.html', form=create_form)


# cargar el usuario desde la base de datos utilizando su ID
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id)) 

# permitir acceso si el usuario esta registrado o denegar si no lo esta
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def login():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST' and create_form.validate():
        username = create_form.Usuario.data
        password = create_form.Contraseña.data

        # recuperar el usuario que coincida con el username capturada
        user = Usuario.query.filter_by(username=username).first()

        hash = generate_password_hash(password)
        print(f"Hash de la contraseña: {hash}")

        # validar si la contraseña coincide con el username
        if user and user.check_password(password):  
            login_user(user)
            return redirect(url_for('ver_pedidos'))
        else:
            flash("Nombre de usuario o contraseña incorrectos", "danger")

    return render_template('login.html', form=create_form)

# salir de la aplicación
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        print('Sesión cerrada')
        return redirect('index')

if __name__ == '__main__':
    iniciar_archivo()
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)