from typing import Optional
from pydantic import BaseModel


class TarjetaBase(BaseModel):
    usuario_id: int
    cvv: Optional[str] = None
    nombre_tarjeta: Optional[str] = None
    numero_tarjeta: Optional[str] = None
    fecha_vencimiento: Optional[str] = None


class TarjetaCreate(TarjetaBase):
    pass


class TarjetaUpdate(TarjetaBase):
    pass


class TarjetaOut(TarjetaBase):
    id: int

    class Config:
        from_attributes = True
