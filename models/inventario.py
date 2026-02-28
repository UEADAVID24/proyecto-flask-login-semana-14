# Clase Inventario
# Gestiona los productos del sistema mediante operaciones CRUD
# Conectada a una base de datos SQLite

from models.producto import Producto
from db import get_connection


class Inventario:

    # CREATE
    # Agrega un nuevo producto a la base de datos
    def agregar_producto(self, producto):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
            (producto.id, producto.nombre, producto.cantidad, producto.precio)
        )

        conn.commit()
        conn.close()

    # READ
    # Obtiene todos los productos almacenados en la base de datos
    def obtener_todos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM productos")
        rows = cursor.fetchall()
        conn.close()

        return [
            Producto(row["id"], row["nombre"], row["cantidad"], row["precio"])
            for row in rows
        ]

    # UPDATE
    # Actualiza la cantidad y el precio de un producto existente
    def actualizar_producto(self, id, cantidad, precio):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
            (cantidad, precio, id)
        )

        conn.commit()
        conn.close()

    # DELETE
    # Elimina un producto del inventario usando su ID
    def eliminar_producto(self, id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    # SEARCH
    # Busca productos por nombre en la base de datos
    def buscar_por_nombre(self, nombre):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM productos WHERE nombre LIKE ?",
            ('%' + nombre + '%',)
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            Producto(row["id"], row["nombre"], row["cantidad"], row["precio"])
            for row in rows
        ]