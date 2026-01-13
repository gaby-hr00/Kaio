from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Tarjeta(Base):
    __tablename__ = "tarjetas"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cvv = Column(String(10))
    nombre_tarjeta = Column(String(120))
    numero_tarjeta = Column(String(60))
    fecha_vencimiento = Column(String(30))

    usuario = relationship("Usuario", back_populates="tarjetas")
