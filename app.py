# Aplicación Flask para un Sistema Avanzado de Gestión de Inventario
# Implementa Programación Orientada a Objetos (POO), SQLite,
# operaciones CRUD reales, búsqueda de productos
# persistencia en TXT, JSON y CSV
# y configuración con SQLAlchemy ORM

from flask import Flask, render_template, request, redirect, url_for
from models.producto import Producto
from models.inventario import Inventario
from db import get_connection

from flask_sqlalchemy import SQLAlchemy

import json
import csv
import os

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SQLAlchemy
# =========================

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# MODELO ORM (SQLAlchemy)
# =========================

class ProductoORM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)

# =========================
# Inventario (POO + SQLite)
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
# Rutas principales
# =========================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/productos')
def productos():
    productos = inventario.obtener_todos()
    return render_template('productos.html', productos=productos)

# =========================
# BUSCAR PRODUCTOS
# =========================

@app.route('/productos/buscar', methods=['GET'])
def buscar_producto():

    nombre = request.args.get('nombre', '')
    productos = inventario.buscar_por_nombre(nombre)

    return render_template(
        'productos.html',
        productos=productos,
        busqueda=nombre
    )

# =========================
# OTRAS PÁGINAS
# =========================

@app.route('/factura')
def factura():
    return render_template('factura.html')


@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

# =========================
# CRUD DE PRODUCTOS
# =========================

@app.route('/productos/agregar', methods=['GET', 'POST'])
def agregar_producto():

    if request.method == 'POST':

        id = int(request.form['id'])
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        inventario.agregar_producto(
            Producto(id, nombre, cantidad, precio)
        )

        return redirect(url_for('productos'))

    return render_template('agregar_producto.html')


@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    if request.method == 'POST':

        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        inventario.actualizar_producto(id, cantidad, precio)

        return redirect(url_for('productos'))

    return render_template('editar_producto.html', id=id)


@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):

    inventario.eliminar_producto(id)

    return redirect(url_for('productos'))

# =========================
# PERSISTENCIA DE DATOS
# TXT - JSON - CSV
# =========================

@app.route('/guardar_txt', methods=['POST'])
def guardar_txt():

    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    ruta = os.path.join('data', 'datos.txt')

    with open(ruta, 'a') as f:
        f.write(f"{nombre},{cantidad},{precio}\n")

    return redirect(url_for('productos'))


@app.route('/guardar_json', methods=['POST'])
def guardar_json():

    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    datos = {
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio
    }

    ruta = os.path.join('data', 'datos.json')

    with open(ruta, 'a') as f:
        json.dump(datos, f)
        f.write("\n")

    return redirect(url_for('productos'))


@app.route('/guardar_csv', methods=['POST'])
def guardar_csv():

    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    ruta = os.path.join('data', 'datos.csv')

    with open(ruta, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nombre, cantidad, precio])

    return redirect(url_for('productos'))

# =========================
# LEER DATOS TXT
# =========================

@app.route('/ver_txt')
def ver_txt():

    ruta = os.path.join('data', 'datos.txt')
    datos = []

    if os.path.exists(ruta):

        with open(ruta, 'r') as f:
            datos = f.readlines()

    return render_template('datos.html', datos=datos)

# =========================
# LEER DATOS JSON
# =========================

@app.route('/ver_json')
def ver_json():

    ruta = os.path.join('data', 'datos.json')
    datos = []

    if os.path.exists(ruta):

        with open(ruta, 'r') as f:
            for linea in f:
                datos.append(json.loads(linea))

    return render_template('datos.html', datos=datos)

# =========================
# LEER DATOS CSV
# =========================

@app.route('/ver_csv')
def ver_csv():

    ruta = os.path.join('data', 'datos.csv')
    datos = []

    if os.path.exists(ruta):

        with open(ruta, 'r') as f:
            reader = csv.reader(f)

            for fila in reader:
                datos.append(fila)

    return render_template('datos.html', datos=datos)

# =========================
# EJECUTAR APLICACIÓN
# =========================

if __name__ == '__main__':
    app.run(debug=True)