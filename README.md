🚀 Sistema Avanzado de Gestión de Inventario – Flask
📌 Descripción del Proyecto

Este proyecto corresponde a un Sistema Avanzado de Gestión de Inventario desarrollado con Flask, como continuación del trabajo realizado en las semanas 9, 10, 11, 12, 13 y 14.

El sistema permite administrar productos de una tienda (ferretería) aplicando Programación Orientada a Objetos (POO), operaciones CRUD, persistencia de datos en múltiples formatos (TXT, JSON, CSV), uso de SQLite y ahora también integración con MySQL y autenticación de usuarios.

🎯 Objetivos

Aplicar Programación Orientada a Objetos (POO).

Implementar operaciones CRUD completas.

Utilizar bases de datos SQLite y MySQL.

Implementar persistencia en TXT, JSON y CSV.

Desarrollar interfaces web con Flask y Jinja2.

Implementar autenticación de usuarios con Flask-Login.

Proteger rutas del sistema.

🆕 Semana 14 – Autenticación de Usuarios

En esta fase se implementó un sistema completo de autenticación utilizando Flask-Login.

🔐 Funcionalidades añadidas:

Registro de usuarios

Inicio de sesión (login)

Cierre de sesión (logout)

Protección de rutas con @login_required

Control de acceso a funcionalidades del sistema

🧑‍💻 Sistema de Usuarios (MySQL)

Se integró una base de datos MySQL con la tabla:

📋 Tabla: usuarios

id_usuario

nombre

email

password

Los usuarios pueden registrarse y luego autenticarse para acceder al sistema.

🔒 Seguridad y Acceso

Las siguientes rutas están protegidas:

/panel

/productos

/clientes

/factura

/ver_txt

/usuarios

Si el usuario no ha iniciado sesión, es redirigido automáticamente al login.

🛠 Tecnologías Utilizadas

Python 3

Flask

Flask-Login

Flask-SQLAlchemy

SQLite

MySQL

HTML + Jinja2

CSS

Git y GitHub

Visual Studio Code

📂 Estructura del Proyecto
Mi_proyecto_flask_Clinton_Alvarado/
│
├── app.py
├── db.py
├── init_db.py
├── desarrollo_web.sql
├── requirements.txt
│
├── Conexion/
│   └── conexion.py
│
├── models/
│   ├── producto.py
│   └── inventario.py
│
├── database/
│   └── database.db
│
├── data/
│   ├── datos.txt
│   ├── datos.json
│   └── datos.csv
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── registro.html
│   ├── productos.html
│   ├── agregar_producto.html
│   ├── clientes.html
│   └── datos.html
│
├── static/
│   └── styles.css
│
└── README.md
🧠 Programación Orientada a Objetos (POO)
Clase Producto

id

nombre

cantidad

precio

Clase Inventario

Gestión de productos

Operaciones CRUD

💾 Persistencia de Datos

El sistema guarda información en:

TXT

JSON

CSV

Rutas disponibles:

/ver_txt

/ver_json

/ver_csv

🗄 Bases de Datos
SQLite

Tabla: productos

MySQL

Tabla: usuarios

🔄 Operaciones CRUD

✔ Crear productos
✔ Leer productos
✔ Actualizar productos
✔ Eliminar productos

🌐 Interfaz de Usuario

El sistema permite:

Login y registro de usuarios

Visualizar inventario

Buscar productos

Agregar productos

Eliminar productos

Ver datos en TXT

▶️ Ejecución del Proyecto
1️⃣ Activar entorno virtual
.\venv\Scripts\activate
2️⃣ Crear base de datos SQLite
py init_db.py
3️⃣ Configurar MySQL

Importar archivo desarrollo_web.sql en phpMyAdmin

4️⃣ Ejecutar la aplicación
py app.py
5️⃣ Abrir en navegador
http://127.0.0.1:5000
👨‍🎓 Autor

Clinton David Alvarado Chongo

Proyecto académico – Desarrollo de aplicaciones web con Flask 🚀
