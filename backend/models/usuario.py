from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(120))
    tipo_identificacion = Column(String(30))
    identificacion = Column(String(60))
    fecha_nacimiento = Column(Date)
    hashed_password = Column(String(200))
    correo = Column(String(120), unique=True, index=True)
    estado = Column(Boolean, default=True)
    celular = Column(String(30))
    identificacion = Column(String(60), unique=True, index=True)
    celular = Column(String(30), unique=True, index=True)
    foto_perfil = Column(String(255))
    direccion = Column(String(255))
    rol_id = Column(Integer, ForeignKey("roles.id"))

    rol = relationship("Rol", back_populates="usuarios")
    pedidos = relationship("Pedido", back_populates="usuario")
    tarjetas = relationship("Tarjeta", back_populates="usuario")
    carrito = relationship("Carrito", back_populates="usuario")
    favoritos = relationship("Favorito", back_populates="usuario")
