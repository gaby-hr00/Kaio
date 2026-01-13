from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from db import Base


class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(120))
    descripcion = Column(Text)
    imagen = Column(String(255))
    precio_unidad = Column(Float)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    calificacion = Column(Float)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))

    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    inventario = relationship("Inventario", back_populates="producto", uselist=False)
    detalle_pedidos = relationship("DetallePedido", back_populates="producto")
