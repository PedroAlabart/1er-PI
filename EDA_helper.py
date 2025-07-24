from database.models import (
    Usuario, Categoria, Producto, Orden, DetalleOrden,
    DireccionEnvio, 
    Carrito,
    MetodoPago, OrdenMetodoPago,
    ResenaProducto, HistorialPago
)
from sqlalchemy import select, func


def find_invalid_user_references(session):
    consultas = {
        "ordenes": Orden,
        "carrito": Carrito,
        "direcciones_envio": DireccionEnvio,
        "resenas": ResenaProducto,
    }
    resultados = {}
    for nombre, tabla in consultas.items():
        stmt = (
            select(tabla.usuario_id)
            .outerjoin(Usuario, tabla.usuario_id == Usuario.usuario_id)
            .where(Usuario.usuario_id == None)
        )
        usuarios_no_validos = session.execute(stmt).scalars().all()
        resultados[nombre] = usuarios_no_validos
    return resultados



def find_invalid_product_references(session):
    tablas = {
        "detalle_ordenes": DetalleOrden,
        "carrito": Carrito,
        "resenas": ResenaProducto,
    }
    resultados = {}
    for nombre, tabla in tablas.items():
        stmt = (
            select(tabla.producto_id)
            .outerjoin(Producto, tabla.producto_id == Producto.producto_id)
            .where(Producto.producto_id == None)
        )
        productos_no_validos = session.execute(stmt).scalars().all()
        resultados[nombre] = productos_no_validos
    return resultados


 


def check_duplicates(session, tables):
    for table in tables:
        result_distinct = session.execute(select(table).distinct()).all()
        result = session.execute(select(table)).all()
        print("Quantity of repeated values in table", table.__name__, ":", len(result) - len(result_distinct))

