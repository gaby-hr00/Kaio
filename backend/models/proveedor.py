from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Proveedor(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True)
    nombre_empresa = Column(String(120))
    nombre_contacto = Column(String(120))
    telefono = Column(String(60))
    direccion = Column(String(255))

    productos = relationship("Producto", back_populates="proveedor")
