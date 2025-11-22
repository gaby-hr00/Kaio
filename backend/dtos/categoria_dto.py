from datetime import date
from typing import Optional

from pydantic import BaseModel


class CategoriaBase(BaseModel):
    nombre: str
    estado: Optional[bool] = True


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        from_attributes = True  # en vez de orm_mode = True
