from typing import List, Optional
from datetime import datetime
from sqlalchemy import (
    String, Integer, ForeignKey, DECIMAL, Text, TIMESTAMP, text
)
from sqlalchemy.orm import (
    DeclarativeBase, mapped_column, Mapped, relationship
)


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id: Mapped[int] = mapped_column("usuario_id", Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("nombre", String(100), nullable=False)
    apellido: Mapped[str] = mapped_column("apellido", String(100), nullable=False)
    dni: Mapped[str] = mapped_column("dni", String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column("email", String(255), unique=True, nullable=False)
    contrasena: Mapped[str] = mapped_column("contrasena", String(255), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column("fecha_registro", TIMESTAMP, nullable=False, server_default= text("CURRENT_TIMESTAMP"))
    # Relaciones
    ordenes: Mapped[List["Orden"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    direcciones_envio: Mapped[List["DireccionEnvio"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    carrito: Mapped[List["Carrito"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    resenas: Mapped[List["ResenaProducto"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Usuario(usuario_id={self.usuario_id!r}, nombre={self.nombre!r}, apellido={self.apellido!r}, dni={self.dni!r})"


class Categoria(Base):
    __tablename__ = "categorias"

    categoria_id: Mapped[int] = mapped_column("categoria_id", Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("nombre", String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column("descripcion", String(255), nullable=True)

    productos: Mapped[List["Producto"]] = relationship(back_populates="categoria", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Categoria(categoria_id={self.categoria_id!r}, nombre={self.nombre!r})"


class Producto(Base):
    __tablename__ = "productos"

    producto_id: Mapped[int] = mapped_column("producto_id", Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("nombre", String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column("descripcion", Text, nullable=True)
    precio: Mapped[float] = mapped_column("precio", DECIMAL(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column("stock", Integer, nullable=False)
    categoria_id: Mapped[int] = mapped_column("categoria_id", ForeignKey("categorias.categoria_id"))

    categoria: Mapped["Categoria"] = relationship(back_populates="productos")
    detalle_ordenes: Mapped[List["DetalleOrden"]] = relationship(back_populates="producto", cascade="all, delete-orphan")
    carrito: Mapped[List["Carrito"]] = relationship(back_populates="producto", cascade="all, delete-orphan")
    resenas: Mapped[List["ResenaProducto"]] = relationship(back_populates="producto", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Producto(producto_id={self.producto_id!r}, nombre={self.nombre!r}, precio={self.precio!r})"


class Orden(Base):
    __tablename__ = "ordenes"

    orden_id: Mapped[int] = mapped_column("orden_id", Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column("usuario_id", ForeignKey("usuarios.usuario_id"))
    fecha_orden: Mapped[datetime] = mapped_column("fecha_orden", TIMESTAMP, nullable=False,server_default= text("CURRENT_TIMESTAMP"))
    total: Mapped[float] = mapped_column("total", DECIMAL(10, 2), nullable=False)
    estado: Mapped[str] = mapped_column("estado", String(50), nullable=False, server_default="Pendiente")

    usuario: Mapped["Usuario"] = relationship(back_populates="ordenes")
    detalle_ordenes: Mapped[List["DetalleOrden"]] = relationship(back_populates="orden", cascade="all, delete-orphan")
    ordenes_metodos_pago: Mapped[List["OrdenMetodoPago"]] = relationship(back_populates="orden", cascade="all, delete-orphan")
    historial_pagos: Mapped[List["HistorialPago"]] = relationship(back_populates="orden", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Orden(orden_id={self.orden_id!r}, usuario_id={self.usuario_id!r}, total={self.total!r}, estado={self.estado!r})"


class DetalleOrden(Base):
    __tablename__ = "detalle_ordenes"

    detalle_id: Mapped[int] = mapped_column("detalle_id", Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column("orden_id", ForeignKey("ordenes.orden_id"))
    producto_id: Mapped[int] = mapped_column("producto_id", ForeignKey("productos.producto_id"))
    cantidad: Mapped[int] = mapped_column("cantidad", Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column("precio_unitario", DECIMAL(10, 2), nullable=False)

    orden: Mapped["Orden"] = relationship(back_populates="detalle_ordenes")
    producto: Mapped["Producto"] = relationship(back_populates="detalle_ordenes")

    def __repr__(self) -> str:
        return f"DetalleOrden(detalle_id={self.detalle_id!r}, orden_id={self.orden_id!r}, producto_id={self.producto_id!r}, cantidad={self.cantidad!r})"


class DireccionEnvio(Base):
    __tablename__ = "direcciones_envio"

    direccion_id: Mapped[int] = mapped_column("direccion_id", Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column("usuario_id", ForeignKey("usuarios.usuario_id"))
    calle: Mapped[str] = mapped_column("calle", String(255), nullable=False)
    ciudad: Mapped[str] = mapped_column("ciudad", String(100), nullable=False)
    departamento: Mapped[Optional[str]] = mapped_column("departamento", String(100))
    provincia: Mapped[Optional[str]] = mapped_column("provincia", String(100))
    distrito: Mapped[Optional[str]] = mapped_column("distrito", String(100))
    estado: Mapped[Optional[str]] = mapped_column("estado", String(100))
    codigo_postal: Mapped[Optional[str]] = mapped_column("codigo_postal", String(20))
    pais: Mapped[str] = mapped_column("pais", String(100), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="direcciones_envio")

    def __repr__(self) -> str:
        return f"DireccionEnvio(direccion_id={self.direccion_id!r}, usuario_id={self.usuario_id!r}, calle={self.calle!r}, ciudad={self.ciudad!r})"


class Carrito(Base):
    __tablename__ = "carrito"

    carrito_id: Mapped[int] = mapped_column("carrito_id", Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column("usuario_id", ForeignKey("usuarios.usuario_id"))
    producto_id: Mapped[int] = mapped_column("producto_id", ForeignKey("productos.producto_id"))
    cantidad: Mapped[int] = mapped_column("cantidad", Integer, nullable=False)
    fecha_agregado: Mapped[datetime] = mapped_column("fecha_agregado", TIMESTAMP, nullable=False,server_default= text("CURRENT_TIMESTAMP"))

    usuario: Mapped["Usuario"] = relationship(back_populates="carrito")
    producto: Mapped["Producto"] = relationship(back_populates="carrito")

    def __repr__(self) -> str:
        return f"Carrito(carrito_id={self.carrito_id!r}, usuario_id={self.usuario_id!r}, producto_id={self.producto_id!r}, cantidad={self.cantidad!r})"


class MetodoPago(Base):
    __tablename__ = "metodos_pago"

    metodo_pago_id: Mapped[int] = mapped_column("metodo_pago_id", Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column("nombre", String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column("descripcion", String(255), nullable=True)

    ordenes_metodos_pago: Mapped[List["OrdenMetodoPago"]] = relationship(back_populates="metodo_pago", cascade="all, delete-orphan")
    historial_pagos: Mapped[List["HistorialPago"]] = relationship(back_populates="metodo_pago", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"MetodoPago(metodo_pago_id={self.metodo_pago_id!r}, nombre={self.nombre!r})"


class OrdenMetodoPago(Base):
    __tablename__ = "ordenes_metodos_pago"

    orden_metodo_id: Mapped[int] = mapped_column("orden_metodo_id", Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column("orden_id", ForeignKey("ordenes.orden_id"))
    metodo_pago_id: Mapped[int] = mapped_column("metodo_pago_id", ForeignKey("metodos_pago.metodo_pago_id"))
    monto_pagado: Mapped[float] = mapped_column("monto_pagado", DECIMAL(10, 2), nullable=False)

    orden: Mapped["Orden"] = relationship(back_populates="ordenes_metodos_pago")
    metodo_pago: Mapped["MetodoPago"] = relationship(back_populates="ordenes_metodos_pago")

    def __repr__(self) -> str:
        return f"OrdenMetodoPago(orden_metodo_id={self.orden_metodo_id!r}, orden_id={self.orden_id!r}, metodo_pago_id={self.metodo_pago_id!r})"


class ResenaProducto(Base):
    __tablename__ = "resenas_productos"

    resena_id: Mapped[int] = mapped_column("resena_id", Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column("usuario_id", ForeignKey("usuarios.usuario_id"))
    producto_id: Mapped[int] = mapped_column("producto_id", ForeignKey("productos.producto_id"))
    calificacion: Mapped[int] = mapped_column("calificacion", Integer, nullable=False)
    comentario: Mapped[Optional[str]] = mapped_column("comentario", Text, nullable=True)
    fecha: Mapped[datetime] = mapped_column("fecha", TIMESTAMP, nullable=False,server_default= text("CURRENT_TIMESTAMP"))

    usuario: Mapped["Usuario"] = relationship(back_populates="resenas")
    producto: Mapped["Producto"] = relationship(back_populates="resenas")

    def __repr__(self) -> str:
        return f"ResenaProducto(resena_id={self.resena_id!r}, usuario_id={self.usuario_id!r}, producto_id={self.producto_id!r}, calificacion={self.calificacion!r})"


class HistorialPago(Base):
    __tablename__ = "historial_pagos"

    pago_id: Mapped[int] = mapped_column("pago_id", Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column("orden_id", ForeignKey("ordenes.orden_id"))
    metodo_pago_id: Mapped[int] = mapped_column("metodo_pago_id", ForeignKey("metodos_pago.metodo_pago_id"))
    monto: Mapped[float] = mapped_column("monto", DECIMAL(10, 2), nullable=False)
    fecha_pago: Mapped[datetime] = mapped_column("fecha_pago", TIMESTAMP, nullable=False,server_default= text("CURRENT_TIMESTAMP"))
    estado_pago: Mapped[str] = mapped_column("estado_pago", String(50), nullable=False, server_default="Procesando")

    orden: Mapped["Orden"] = relationship(back_populates="historial_pagos")
    metodo_pago: Mapped["MetodoPago"] = relationship(back_populates="historial_pagos")

    def __repr__(self) -> str:
        return f"HistorialPago(pago_id={self.pago_id!r}, orden_id={self.orden_id!r}, monto={self.monto!r}, estado_pago={self.estado_pago!r})"
