from typing import Optional
from pydantic import BaseModel


class DetallePedidoBase(BaseModel):
    cantidad: int
    precio_unidad: float
    descuento: Optional[float] = 0.0
    subtotal: Optional[float] = 0.0
    producto_id: int
    pedido_id: int


class DetallePedidoCreate(DetallePedidoBase):
    pass


class DetallePedidoUpdate(DetallePedidoBase):
    pass


class DetallePedidoOut(DetallePedidoBase):
    id: int

    class Config:
        from_attributes = True
