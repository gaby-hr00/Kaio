from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PedidoBase(BaseModel):
    usuario_id: int
    fecha_pedido: Optional[datetime] = None
    fecha_envio: Optional[datetime] = None
    fecha_entrega: Optional[datetime] = None
    nombre_destinatario: Optional[str] = None
    direccion_destino: Optional[str] = None
    valor_total: Optional[float] = 0.0
    id_transporte: Optional[int] = None


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(PedidoBase):
    pass


class PedidoOut(PedidoBase):
    id: int

    class Config:
        from_attributes = True
