from typing import Optional
from pydantic import BaseModel


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    precio_unidad: Optional[float] = None
    categoria_id: Optional[int] = None
    calificacion: Optional[float] = None
    proveedor_id: Optional[int] = None


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoOut(ProductoBase):
    id: int

    class Config:
        from_attributes = True
