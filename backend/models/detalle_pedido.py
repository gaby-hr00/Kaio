from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class DetallePedido(Base):
    __tablename__ = "detalle_pedidos"
    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    precio_unidad = Column(Float)
    descuento = Column(Float)
    subtotal = Column(Float)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))

    producto = relationship("Producto", back_populates="detalle_pedidos")
    pedido = relationship("Pedido", back_populates="detalles")
