from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Carrito(Base):
    __tablename__ = "carritos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, default=1)

    usuario = relationship("Usuario", back_populates="carrito")
