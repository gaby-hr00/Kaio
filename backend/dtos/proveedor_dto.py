from typing import Optional
from pydantic import BaseModel


class ProveedorBase(BaseModel):
    nombre_empresa: str
    nombre_contacto: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(ProveedorBase):
    pass


class ProveedorOut(ProveedorBase):
    id: int

    class Config:
        from_attributes = True
