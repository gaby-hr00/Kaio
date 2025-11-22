from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db import Base


class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(60))
    estado = Column(Boolean)

    usuarios = relationship("Usuario", back_populates="rol")
