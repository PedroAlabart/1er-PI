from typing import List, Optional
from datetime import datetime
from sqlalchemy import (
    String, Integer, ForeignKey, DECIMAL, Text, TIMESTAMP
)
from sqlalchemy.orm import (
    DeclarativeBase, mapped_column, Mapped, relationship
)


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id: Mapped[int] = mapped_column("UsuarioID", Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("Nombre", String(100), nullable=False)
    apellido: Mapped[str] = mapped_column("Apellido", String(100), nullable=False)
    dni: Mapped[str] = mapped_column("DNI", String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column("Email", String(255), unique=True, nullable=False)
    contraseña: Mapped[str] = mapped_column("Contraseña", String(255), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column("FechaRegistro", TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")

    # Relaciones
    ordenes: Mapped[List["Orden"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    direcciones_envio: Mapped[List["DireccionEnvio"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    carrito: Mapped[List["Carrito"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    reseñas: Mapped[List["ReseñaProducto"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Usuario(usuario_id={self.usuario_id!r}, nombre={self.nombre!r}, apellido={self.apellido!r}, dni={self.dni!r})"


class Categoria(Base):
    __tablename__ = "categorias"

    categoria_id: Mapped[int] = mapped_column("CategoriaID", Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("Nombre", String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column("Descripcion", String(255), nullable=True)

    productos: Mapped[List["Producto"]] = relationship(back_populates="categoria", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Categoria(categoria_id={self.categoria_id!r}, nombre={self.nombre!r})"


class Producto(Base):
    __tablename__ = "productos"

    producto_id: Mapped[int] = mapped_column("ProductoID", Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("Nombre", String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column("Descripcion", Text, nullable=True)
    precio: Mapped[float] = mapped_column("Precio", DECIMAL(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column("Stock", Integer, nullable=False)
    categoria_id: Mapped[int] = mapped_column("CategoriaID", ForeignKey("categorias.CategoriaID"))

    categoria: Mapped["Categoria"] = relationship(back_populates="productos")
    detalle_ordenes: Mapped[List["DetalleOrden"]] = relationship(back_populates="producto", cascade="all, delete-orphan")
    carrito: Mapped[List["Carrito"]] = relationship(back_populates="producto", cascade="all, delete-orphan")
    reseñas: Mapped[List["ReseñaProducto"]] = relationship(back_populates="producto", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Producto(producto_id={self.producto_id!r}, nombre={self.nombre!r}, precio={self.precio!r})"


class Orden(Base):
    __tablename__ = "ordenes"

    orden_id: Mapped[int] = mapped_column("OrdenID", Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column("UsuarioID", ForeignKey("usuarios.UsuarioID"))
    fecha_orden: Mapped[datetime] = mapped_column("FechaOrden", TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    total: Mapped[float] = mapped_column("Total", DECIMAL(10, 2), nullable=False)
    estado: Mapped[str] = mapped_column("Estado", String(50), nullable=False, server_default="Pendiente")

    usuario: Mapped["Usuario"] = relationship(back_populates="ordenes")
    detalle_ordenes: Mapped[List["DetalleOrden"]] = relationship(back_populates="orden", cascade="all, delete-orphan")
    ordenes_metodos_pago: Mapped[List["OrdenMetodoPago"]] = relationship(back_populates="orden", cascade="all, delete-orphan")
    historial_pagos: Mapped[List["HistorialPago"]] = relationship(back_populates="orden", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Orden(orden_id={self.orden_id!r}, usuario_id={self.usuario_id!r}, total={self.total!r}, estado={self.estado!r})"


class DetalleOrden(Base):
    __tablename__ = "detalleordenes"

    detalle_id: Mapped[int] = mapped_column("DetalleID", Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column("OrdenID", ForeignKey("ordenes.OrdenID"))
    producto_id: Mapped[int] = mapped_column("ProductoID", ForeignKey("productos.ProductoID"))
    cantidad: Mapped[int] = mapped_column("Cantidad", Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column("PrecioUnitario", DECIMAL(10, 2), nullable=False)

    orden: Mapped["Orden"] = relationship(back_populates="detalle_ordenes")
    producto: Mapped["Producto"] = relationship(back_populates="detalle_ordenes")

    def __repr__(self) -> str:
        return f"DetalleOrden(detalle_id={self.detalle_id!r}, orden_id={self.orden_id!r}, producto_id={self.producto_id!r}, cantidad={self.cantidad!r})"


class DireccionEnvio(Base):
    __tablename__ = "direccionesenvio"

    direccion_id: Mapped[int] = mapped_column("DireccionID", Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column("UsuarioID", ForeignKey("usuarios.UsuarioID"))
    calle: Mapped[str] = mapped_column("Calle", String(255), nullable=False)
    ciudad: Mapped[str] = mapped_column("Ciudad", String(100), nullable=False)
    departamento: Mapped[Optional[str]] = mapped_column("Departamento", String(100))
    provincia: Mapped[Optional[str]] = mapped_column("Provincia", String(100))
    distrito: Mapped[Optional[str]] = mapped_column("Distrito", String(100))
    estado: Mapped[Optional[str]] = mapped_column("Estado", String(100))
    codigo_postal: Mapped[Optional[str]] = mapped_column("CodigoPostal", String(20))
    pais: Mapped[str] = mapped_column("Pais", String(100), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="direcciones_envio")

    def __repr__(self) -> str:
        return f"DireccionEnvio(direccion_id={self.direccion_id!r}, usuario_id={self.usuario_id!r}, calle={self.calle!r}, ciudad={self.ciudad!r})"


class Carrito(Base):
    __tablename__ = "carrito"

    carrito_id: Mapped[int] = mapped_column("CarritoID", Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column("UsuarioID", ForeignKey("usuarios.UsuarioID"))
    producto_id: Mapped[int] = mapped_column("ProductoID", ForeignKey("productos.ProductoID"))
    cantidad: Mapped[int] = mapped_column("Cantidad", Integer, nullable=False)
    fecha_agregado: Mapped[datetime] = mapped_column("FechaAgregado", TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")

    usuario: Mapped["Usuario"] = relationship(back_populates="carrito")
    producto: Mapped["Producto"] = relationship(back_populates="carrito")

    def __repr__(self) -> str:
        return f"Carrito(carrito_id={self.carrito_id!r}, usuario_id={self.usuario_id!r}, producto_id={self.producto_id!r}, cantidad={self.cantidad!r})"


class MetodoPago(Base):
    __tablename__ = "metodospago"

    metodo_pago_id: Mapped[int] = mapped_column("MetodoPagoID", Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("Nombre", String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column("Descripcion", String(255), nullable=True)

    ordenes_metodos_pago: Mapped[List["OrdenMetodoPago"]] = relationship(back_populates="metodo_pago", cascade="all, delete-orphan")
    historial_pagos: Mapped[List["HistorialPago"]] = relationship(back_populates="metodo_pago", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"MetodoPago(metodo_pago_id={self.metodo_pago_id!r}, nombre={self.nombre!r})"


class OrdenMetodoPago(Base):
    __tablename__ = "ordenesmetodospago"

    orden_metodo_id: Mapped[int] = mapped_column("OrdenMetodoID", Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column("OrdenID", ForeignKey("ordenes.OrdenID"))
    metodo_pago_id: Mapped[int] = mapped_column("MetodoPagoID", ForeignKey("metodospago.MetodoPagoID"))
    monto_pagado: Mapped[float] = mapped_column("MontoPagado", DECIMAL(10, 2), nullable=False)

    orden: Mapped["Orden"] = relationship(back_populates="ordenes_metodos_pago")
    metodo_pago: Mapped["MetodoPago"] = relationship(back_populates="ordenes_metodos_pago")

    def __repr__(self) -> str:
        return f"OrdenMetodoPago(orden_metodo_id={self.orden_metodo_id!r}, orden_id={self.orden_id!r}, metodo_pago_id={self.metodo_pago_id!r})"


class ReseñaProducto(Base):
    __tablename__ = "reseñasproductos"

    reseña_id: Mapped[int] = mapped_column("ReseñaID", Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column("UsuarioID", ForeignKey("usuarios.UsuarioID"))
    producto_id: Mapped[int] = mapped_column("ProductoID", ForeignKey("productos.ProductoID"))
    calificacion: Mapped[int] = mapped_column("Calificacion", Integer, nullable=False)
    comentario: Mapped[Optional[str]] = mapped_column("Comentario", Text, nullable=True)
    fecha: Mapped[datetime] = mapped_column("Fecha", TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")

    usuario: Mapped["Usuario"] = relationship(back_populates="reseñas")
    producto: Mapped["Producto"] = relationship(back_populates="reseñas")

    def __repr__(self) -> str:
        return f"ReseñaProducto(reseña_id={self.reseña_id!r}, usuario_id={self.usuario_id!r}, producto_id={self.producto_id!r}, calificacion={self.calificacion!r})"


class HistorialPago(Base):
    __tablename__ = "historialpagos"

    pago_id: Mapped[int] = mapped_column("PagoID", Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column("OrdenID", ForeignKey("ordenes.OrdenID"))
    metodo_pago_id: Mapped[int] = mapped_column("MetodoPagoID", ForeignKey("metodospago.MetodoPagoID"))
    monto: Mapped[float] = mapped_column("Monto", DECIMAL(10, 2), nullable=False)
    fecha_pago: Mapped[datetime] = mapped_column("FechaPago", TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    estado_pago: Mapped[str] = mapped_column("EstadoPago", String(50), nullable=False, server_default="Procesando")

    orden: Mapped["Orden"] = relationship(back_populates="historial_pagos")
    metodo_pago: Mapped["MetodoPago"] = relationship(back_populates="historial_pagos")

    def __repr__(self) -> str:
        return f"HistorialPago(pago_id={self.pago_id!r}, orden_id={self.orden_id!r}, monto={self.monto!r}, estado_pago={self.estado_pago!r})"
