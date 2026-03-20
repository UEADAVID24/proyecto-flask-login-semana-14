# Aplicación Flask para un Sistema Avanzado de Gestión de Inventario

from flask import Flask, render_template, request, redirect, url_for
from models.producto import Producto
from models.inventario import Inventario
from db import get_connection
from Conexion.conexion import obtener_conexion

from flask_sqlalchemy import SQLAlchemy

# 🔐 LOGIN
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import json
import csv
import os

app = Flask(__name__)

# 🔐 CONFIG LOGIN
app.secret_key = "clave_secreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# =========================
# MODELO USUARIO
# =========================

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()

    conexion.close()

    if user:
        return Usuario(user[0], user[1], user[2], user[3])
    return None

# =========================
# CONFIGURACIÓN SQLAlchemy
# =========================

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# MODELO ORM
# =========================

class ProductoORM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)

# =========================
# Inventario
# =========================

inventario = Inventario()

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM productos")

if cursor.fetchone()[0] == 0:
    inventario.agregar_producto(Producto(1, "Martillo", 10, 5.50))
    inventario.agregar_producto(Producto(2, "Clavos", 100, 0.10))
    inventario.agregar_producto(Producto(3, "Taladro", 5, 120.00))

conn.close()

# =========================
# 🔑 LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s AND password = %s",
            (email, password)
        )

        user = cursor.fetchone()
        conexion.close()

        if user:
            usuario = Usuario(user[0], user[1], user[2], user[3])
            login_user(usuario)
            return redirect(url_for('panel'))

        return "Credenciales incorrectas"

    return render_template('login.html')


# =========================
# 📝 REGISTRO
# =========================

@app.route('/registro', methods=['GET', 'POST'])
def registro():

    # 🔒 SI YA ESTÁ LOGUEADO, LO REDIRIGE
    if current_user.is_authenticated:
        return redirect(url_for('panel'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Verificar si ya existe el email
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existente = cursor.fetchone()

        if existente:
            conexion.close()
            return "El correo ya está registrado"

        # Insertar nuevo usuario
        sql = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
        valores = (nombre, email, password)

        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()

        return redirect(url_for('login'))

    return render_template('registro.html')


# =========================
# 🔓 LOGOUT
# =========================

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# =========================
# 🔐 PANEL PROTEGIDO
# =========================

@app.route('/panel')
@login_required
def panel():
    return f"Bienvenido {current_user.nombre}"


# =========================
# RUTAS PRINCIPALES
# =========================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/productos')
@login_required
def productos():
    productos = inventario.obtener_todos()
    return render_template('productos.html', productos=productos)


# =========================
# BUSCAR PRODUCTOS
# =========================

@app.route('/productos/buscar')
@login_required
def buscar_producto():
    nombre = request.args.get('nombre', '')
    productos = inventario.buscar_por_nombre(nombre)

    return render_template('productos.html', productos=productos, busqueda=nombre)


# =========================
# OTRAS PÁGINAS
# =========================

@app.route('/factura')
@login_required
def factura():
    return render_template('factura.html')


@app.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html')


# =========================
# CRUD PRODUCTOS
# =========================

@app.route('/productos/agregar', methods=['GET', 'POST'])
@login_required
def agregar_producto():

    if request.method == 'POST':
        id = int(request.form['id'])
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        inventario.agregar_producto(Producto(id, nombre, cantidad, precio))

        return redirect(url_for('productos'))

    return render_template('agregar_producto.html')


@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminar_producto(id):
    inventario.eliminar_producto(id)
    return redirect(url_for('productos'))


# =========================
# DATOS TXT
# =========================

@app.route('/ver_txt')
@login_required
def ver_txt():
    ruta = os.path.join('data', 'datos.txt')
    datos = []

    if os.path.exists(ruta):
        with open(ruta, 'r') as f:
            datos = f.readlines()

    return render_template('datos.html', datos=datos)


# =========================
# USUARIOS MYSQL
# =========================

@app.route('/usuarios')
@login_required
def usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    conexion.close()

    return render_template("usuarios.html", usuarios=usuarios)


# =========================
# EJECUTAR
# =========================

if __name__ == '__main__':
    app.run(debug=True)