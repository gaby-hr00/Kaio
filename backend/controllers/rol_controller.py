from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import SessionLocal
from dtos.rol_dto import RolCreate, RolOut, RolUpdate
from models.rol import Rol

router = APIRouter(prefix="/roles", tags=["roles"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=RolOut)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = Rol(**rol.dict())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol


@router.get("/", response_model=list[RolOut])
def listar_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()


@router.get("/{rol_id}", response_model=RolOut)
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.get(Rol, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@router.put("/{rol_id}", response_model=RolOut)
def actualizar_rol(rol_id: int, datos: RolUpdate, db: Session = Depends(get_db)):
    rol = db.get(Rol, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(rol, key, value)
    db.commit()
    db.refresh(rol)
    return rol


@router.delete("/{rol_id}")
def eliminar_rol(rol_id: int, db: Session = Depends(get_db)):
    rol = db.get(Rol, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(rol)
    db.commit()
    return {"ok": True}
