from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Favorito(Base):
    __tablename__ = "favoritos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))

    usuario = relationship("Usuario", back_populates="favoritos")
