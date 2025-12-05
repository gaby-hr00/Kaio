from typing import Optional
from pydantic import BaseModel
from dtos.producto_dto import ProductoOut

class CarritoBase(BaseModel):
    usuario_id: int
    producto_id: int
    cantidad: Optional[int] = 1


class CarritoCreate(CarritoBase):
    pass


class CarritoUpdate(CarritoBase):
    pass


class CarritoOut(CarritoBase):
    id: int
    producto: ProductoOut  # 🔥 el producto completo gracias al JOIN

    class Config:
        from_attributes = True
