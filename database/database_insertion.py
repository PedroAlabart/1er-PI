from sqlalchemy.orm import Session
from sqlalchemy import insert
from database.database_connection import engine

from config import CSV_DIR

from database.insertion_helper import(
    UsuarioLoader,
    CategoriaLoader,
    ProductoLoader,
    OrdenLoader,
    DetalleOrdenLoader,
    DireccionEnvioLoader,
    CarritoLoader,
    MetodoPagoLoader,
    OrdenMetodoPagoLoader,
    ResenaProductoLoader,
    HistorialPagoLoader
)


def load_all():
    """Loads all data from CSV files into the database."""
    with Session(engine) as session:
        for loader_class in [
            UsuarioLoader,          # usuarios
            CategoriaLoader,        # categorias
            ProductoLoader,         # productos → requiere categorias
            OrdenLoader,            # ordenes → requiere usuarios
            DetalleOrdenLoader,     # detalle_ordenes → requiere ordenes y productos
            DireccionEnvioLoader,   # direcciones_envio → requiere usuarios
            CarritoLoader,          # carrito → requiere usuarios y productos
            MetodoPagoLoader,       # metodos_pago
            OrdenMetodoPagoLoader,  # ordenes_metodos_pago → requiere ordenes y metodos_pago
            ResenaProductoLoader,   # resenas_productos → requiere usuarios y productos
            HistorialPagoLoader     # historial_pagos → requiere ordenes y metodos_pago
        ]:
            print(f"▶ Loading: {loader_class.__name__}")
            loader = loader_class(session)
            loader.load()
            print(f"✔ {loader_class.__name__} Loaded Succesfully.\n")








