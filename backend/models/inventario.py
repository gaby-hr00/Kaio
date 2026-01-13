from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base


class Inventario(Base):
    __tablename__ = "inventarios"
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), unique=True)
    stock = Column(Integer)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow)

    producto = relationship("Producto", back_populates="inventario")
