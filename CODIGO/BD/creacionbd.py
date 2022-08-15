import sqlite3

#CREACION DE LAS TABLAS DE LA BASE DE DATOS
def crearTablas():

    usuariosTable = """CREATE TABLE IF NOT EXISTS usuarios (
        id integer not null primary key AUTOINCREMENT,
        nombre varchar(100) not null,
        apellidos varchar(100) not null,
        correo varchar(100) not null,
        username varchar(100) not null unique,
        password varchar(100) not null,
        tipouser integer not null
    )"""

    informacionTable = """CREATE TABLE IF NOT EXISTS informacion (
        id integer not null primary key AUTOINCREMENT,
        accion varchar(100),
        fecha varchar(100),
        usuario varchar(100),
        FOREIGN KEY (usuario) REFERENCES usuarios(id)
    )"""

    clientesTable = """CREATE TABLE IF NOT EXISTS clientes (
        idcliente integer not null primary key AUTOINCREMENT,
        nombre varchar(100) not null,
        telefono integer not null,
        direccion varchar(100) not null,
        correoelectronico varchar(100) not null
    )"""

    productosTable = """CREATE TABLE IF NOT EXISTS productos (
        idproducto integer not null primary key AUTOINCREMENT,
        nombre varchar(100) not null,
        descripcion varchar(300) not null,
        referencia varchar(100) not null,
        precio integer not null,
        image varchar(1000)
    )"""

    proveedoresTable = """CREATE TABLE IF NOT EXISTS proveedores (
        idproovedor integer not null primary key AUTOINCREMENT,
        nombre varchar(100) not null,
        cif varchar(100) not null unique,
        telefono integer not null,
        email varchar(100),
        direccion varchar(100),
        cuentabanco varchar(100)
    )"""


    facturaTable = """CREATE TABLE IF NOT EXISTS factura (
        id integer not null primary key AUTOINCREMENT,
        cliente varchar(100) not null,
        producto varchar(100) not null,
        proveedor varchar(100) not null,
        fecha varchar(100) not null,
        total varchar(100) not null,
        FOREIGN KEY (cliente) REFERENCES clientes(idcliente),
        FOREIGN KEY (producto) REFERENCES productos(idproducto),
        FOREIGN KEY (proveedor) REFERENCES proveedores(idproovedor)
    )""" 
    
    
    updateProductosTable = """
    ALTER TABLE productos ADD COLUMN proveedorCif varchar(100) REFERENCES proveedores(cif)
    """


    try:
        #Se genera la base de datos en caso de que no exista
        conn = sqlite3.connect('CODIGO/BD/emz.db')

        #Se crea una conexion para mandar las querys
        c = conn.cursor()

        #Se ejecutan las querys
        c.execute(usuariosTable)
        c.execute(informacionTable)
        c.execute(clientesTable)
        c.execute(productosTable)
        c.execute(proveedoresTable)
        c.execute(facturaTable)
        c.execute(updateProductosTable)

    except Exception as ex:

        print(ex)
    

crearTablas()