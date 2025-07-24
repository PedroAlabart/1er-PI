import csv
import os

from abc import ABC, abstractmethod
from typing import Any, Dict

from sqlalchemy import insert
from sqlalchemy.orm import Session

from config import CSV_DIR
from database.models import Base

from database.models import (
    Usuario,
    Categoria,
    Producto,
    Orden,
    DetalleOrden,
    DireccionEnvio,
    Carrito,
    MetodoPago,
    OrdenMetodoPago,
    ResenaProducto,
    HistorialPago
)

class CSVLoader(ABC):
    """Abstract base class for loading data from CSV files into the database."""
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get_csv_name(self) -> str:
        """Retorna el path al archivo CSV"""
        pass
    def get_csv_path(self) -> str:
        """Devuelve el path completo al CSV, combinando el prefijo y el nombre"""
        return os.path.join(CSV_DIR, self.get_csv_name())

    @abstractmethod
    def get_model_class(self) -> type[Base]:
        """Retorna la clase del modelo ORM al que se va a insertar"""
        pass

    @abstractmethod
    def map_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """
        Mapea una fila del CSV a un diccionario compatible con insert().
        """
        pass

    def load(self):
        """Iterates through the CSV file and inserts data bulkly into the database."""
        file_path = self.get_csv_path()
        model = self.get_model_class()

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [self.map_row(row) for row in reader]

        self.session.execute(insert(model), data)
        self.session.commit()



class UsuarioLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "2.Usuarios.csv"

    def get_model_class(self):
        return Usuario

    def map_row(self, row):
        return {
            "nombre": row["Nombre"],
            "apellido": row["Apellido"],
            "dni": row["DNI"],
            "email": row["Email"],
            "contrasena": row["Contraseña"]  # <- bien escrito
        }
    

class CategoriaLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "3.Categorias.csv"

    def get_model_class(self):
        return Categoria

    def map_row(self, row):
        return {
            "nombre": row["Nombre"],
            "descripcion": row.get("Descripcion")  # puede ser null
        }
class ProductoLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "4.Productos.csv"

    def get_model_class(self):
        return Producto

    def map_row(self, row):
        return {
            "nombre": row["Nombre"],
            "descripcion": row.get("Descripcion"),
            "precio": float(row["Precio"]),
            "stock": int(row["Stock"]),
            "categoria_id": int(row["CategoriaID"])
        }

class OrdenLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "5.Ordenes.csv"

    def get_model_class(self):
        return Orden

    def map_row(self, row):
        return {
            "usuario_id": int(row["UsuarioID"]),
            "total": float(row["Total"]),
            "estado": row.get("Estado", "Pendiente"),
            "fecha_orden" : row.get("FechaOrden")  # puede ser null
            # Si fecha_orden es null, se autocompleta con la fecha actual
        }

class DetalleOrdenLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "6.detalle_ordenes.csv"

    def get_model_class(self):
        return DetalleOrden

    def map_row(self, row):
        return {
            "orden_id": int(row["OrdenID"]),
            "producto_id": int(row["ProductoID"]),
            "cantidad": int(row["Cantidad"]),
            "precio_unitario": float(row["PrecioUnitario"])
        }

class DireccionEnvioLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "7.direcciones_envio.csv"

    def get_model_class(self):
        return DireccionEnvio

    def map_row(self, row):
        return {
            "usuario_id": int(row["UsuarioID"]),
            "calle": row["Calle"],
            "ciudad": row["Ciudad"],
            "departamento": row.get("Departamento"),
            "provincia": row.get("Provincia"),
            "distrito": row.get("Distrito"),
            "estado": row.get("Estado"),
            "codigo_postal": row.get("CodigoPostal"),
            "pais": row["Pais"]
        }

class CarritoLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "8.carrito.csv"

    def get_model_class(self):
        return Carrito

    def map_row(self, row):
        return {
            "usuario_id": int(row["UsuarioID"]),
            "producto_id": int(row["ProductoID"]),
            "cantidad": int(row["Cantidad"]),
            "fecha_agregado": row.get("FechaAgregado")   # puede ser null
                            }

class MetodoPagoLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "9.metodos_pago.csv"

    def get_model_class(self):
        return MetodoPago

    def map_row(self, row):
        return {
            "nombre": row["Nombre"],
            "descripcion": row.get("Descripcion")
        }

class OrdenMetodoPagoLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "10.ordenes_metodospago.csv"

    def get_model_class(self):
        return OrdenMetodoPago

    def map_row(self, row):
        return {
            "orden_id": int(row["OrdenID"]),
            "metodo_pago_id": int(row["MetodoPagoID"]),
            "monto_pagado": float(row["MontoPagado"])
        }

class ResenaProductoLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "11.resenas_productos.csv"

    def get_model_class(self):
        return ResenaProducto

    def map_row(self, row):
        return {
            "usuario_id": int(row["UsuarioID"]),
            "producto_id": int(row["ProductoID"]),
            "calificacion": int(row["Calificacion"]),
            "comentario": row.get("Comentario"),
             "fecha": row.get("Fecha")  
             }

class HistorialPagoLoader(CSVLoader):
    def get_csv_name(self) -> str:
        return "12.historial_pagos.csv"

    def get_model_class(self):
        return HistorialPago

    def map_row(self, row):
        return {
            "orden_id": int(row["OrdenID"]),
            "metodo_pago_id": int(row["MetodoPagoID"]),
            "monto": float(row["Monto"]),
            "estado_pago": row.get("EstadoPago", "Procesando"),
            "fecha_pago": row.get("FechaPago")  # puede ser null
        }