from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre_completo: str
    tipo_identificacion: Optional[str] = None
    identificacion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    correo: Optional[EmailStr] = None
    estado: Optional[bool] = True
    celular: Optional[str] = None
    foto_perfil: Optional[str] = None
    direccion: Optional[str] = None
    rol_id: Optional[int] = None


class UsuarioCreate(UsuarioBase):
    correo: EmailStr
    contrasena: str


class UsuarioUpdate(UsuarioBase):
    contrasena: Optional[str] = None
    pass


class UsuarioOut(UsuarioBase):
    id: int
    model_config = {"from_attributes": True}


class UsuarioLogin(BaseModel):
    correo: EmailStr
    contrasena: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
