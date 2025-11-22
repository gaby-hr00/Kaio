from typing import Optional
from pydantic import BaseModel


class FavoritoBase(BaseModel):
    usuario_id: int
    producto_id: int


class FavoritoCreate(FavoritoBase):
    pass


class FavoritoUpdate(FavoritoBase):
    pass


class FavoritoOut(FavoritoBase):
    id: int

    class Config:
        from_attributes = True
