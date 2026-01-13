from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base


class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_pedido = Column(DateTime, default=datetime.utcnow)
    fecha_envio = Column(DateTime)
    fecha_entrega = Column(DateTime)
    nombre_destinatario = Column(String(120))
    direccion_destino = Column(String(255))
    valor_total = Column(Float)
    id_transporte = Column(Integer)

    usuario = relationship("Usuario", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido")
