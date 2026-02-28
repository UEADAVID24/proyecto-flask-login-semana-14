# Clase Producto
# Representa un producto dentro del sistema de inventario
# Aplica Programación Orientada a Objetos (POO)

class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        # Identificador único del producto
        self.id = id
        # Nombre del producto
        self.nombre = nombre
        # Cantidad disponible en inventario
        self.cantidad = cantidad
        # Precio unitario del producto
        self.precio = precio

    # Obtener el ID del producto
    def get_id(self):
        return self.id

    # Obtener el nombre del producto
    def get_nombre(self):
        return self.nombre

    # Obtener la cantidad disponible
    def get_cantidad(self):
        return self.cantidad

    # Obtener el precio del producto
    def get_precio(self):
        return self.precio

    # Modificar la cantidad del producto
    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    # Modificar el precio del producto
    def set_precio(self, precio):
        self.precio = precio