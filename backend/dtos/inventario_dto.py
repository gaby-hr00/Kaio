from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InventarioBase(BaseModel):
    producto_id: int
    stock: Optional[int] = 0
    fecha_actualizacion: Optional[datetime] = None


class InventarioCreate(InventarioBase):
    pass


class InventarioUpdate(InventarioBase):
    pass


class InventarioOut(InventarioBase):
    id: int

    class Config:
        from_attributes = True
