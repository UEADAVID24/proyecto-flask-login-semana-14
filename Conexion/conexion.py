import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="desarrollo_web"  # 🔥 CORREGIDO
    )
    return conexion