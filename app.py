# Aplicación Flask para un Sistema Avanzado de Gestión de Inventario
# Implementa Programación Orientada a Objetos (POO), SQLite,
# operaciones CRUD reales y búsqueda de productos

from flask import Flask, render_template, request, redirect, url_for
from models.producto import Producto
from models.inventario import Inventario
from db import get_connection

app = Flask(__name__)

# =========================
# Inventario (POO + SQLite)
# =========================
# Se crea una instancia de Inventario que gestiona los productos
inventario = Inventario()

# Inserta productos iniciales SOLO si la base de datos está vacía
# Esto evita duplicados al reiniciar la aplicación
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

# Página de inicio
@app.route('/')
def home():
    return render_template('index.html')

# Página "Acerca de"
@app.route('/about')
def about():
    return render_template('about.html')

# Mostrar todos los productos del inventario
@app.route('/productos')
def productos():
    productos = inventario.obtener_todos()
    return render_template('productos.html', productos=productos)

# 🔍 BUSCAR productos por nombre
@app.route('/productos/buscar', methods=['GET'])
def buscar_producto():
    nombre = request.args.get('nombre', '')
    productos = inventario.buscar_por_nombre(nombre)
    return render_template(
        'productos.html',
        productos=productos,
        busqueda=nombre
    )

# Página de facturación (extensible)
@app.route('/factura')
def factura():
    return render_template('factura.html')

# Página de clientes (extensible)
@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

# =========================
# CRUD DE PRODUCTOS
# =========================

# CREATE: Agregar un nuevo producto
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

# UPDATE: Editar cantidad y precio de un producto
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        inventario.actualizar_producto(id, cantidad, precio)
        return redirect(url_for('productos'))

    return render_template('editar_producto.html', id=id)

# DELETE: Eliminar un producto por ID
@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    inventario.eliminar_producto(id)
    return redirect(url_for('productos'))

# =========================
# Ejecución de la aplicación
# =========================
if __name__ == '__main__':
    app.run(debug=True)