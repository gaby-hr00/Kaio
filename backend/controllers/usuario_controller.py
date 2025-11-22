from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import SessionLocal
from dtos.usuario_dto import UsuarioCreate, UsuarioOut, UsuarioUpdate
from models.usuario import Usuario
from utils.security import get_password_hash

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    data = usuario.dict()
    plain = data.pop("contrasena", None)
    if plain:
        data["hashed_password"] = get_password_hash(plain)

    # prevent duplicates
    correo = data.get("correo")
    if correo:
        existing = db.query(Usuario).filter(Usuario.correo == correo).first()
        if existing:
            raise HTTPException(status_code=400, detail="Correo ya registrado")

    identificacion = data.get("identificacion")
    if identificacion:
        existing = db.query(Usuario).filter(Usuario.identificacion == identificacion).first()
        if existing:
            raise HTTPException(status_code=400, detail="Identificación ya registrada")

    celular = data.get("celular")
    if celular:
        existing = db.query(Usuario).filter(Usuario.celular == celular).first()
        if existing:
            raise HTTPException(status_code=400, detail="Celular ya registrado")

    db_usuario = Usuario(**data)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.get("/", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    update_data = datos.dict(exclude_unset=True)
    # handle password separately
    if "contrasena" in update_data:
        plain = update_data.pop("contrasena")
        if plain:
            usuario.hashed_password = get_password_hash(plain)
    for key, value in update_data.items():
        setattr(usuario, key, value)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"ok": True}
