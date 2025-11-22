from typing import Optional
from pydantic import BaseModel


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

    class Config:
        from_attributes = True
