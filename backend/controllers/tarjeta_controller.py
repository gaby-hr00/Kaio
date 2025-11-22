from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import SessionLocal
from dtos.tarjeta_dto import TarjetaCreate, TarjetaOut, TarjetaUpdate
from models.tarjeta import Tarjeta

router = APIRouter(prefix="/tarjetas", tags=["tarjetas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TarjetaOut)
def crear_tarjeta(t: TarjetaCreate, db: Session = Depends(get_db)):
    db_t = Tarjeta(**t.dict())
    db.add(db_t)
    db.commit()
    db.refresh(db_t)
    return db_t


@router.get("/", response_model=list[TarjetaOut])
def listar_tarjetas(db: Session = Depends(get_db)):
    return db.query(Tarjeta).all()


@router.get("/{t_id}", response_model=TarjetaOut)
def obtener_tarjeta(t_id: int, db: Session = Depends(get_db)):
    t = db.get(Tarjeta, t_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return t


@router.put("/{t_id}", response_model=TarjetaOut)
def actualizar_tarjeta(t_id: int, datos: TarjetaUpdate, db: Session = Depends(get_db)):
    t = db.get(Tarjeta, t_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(t, key, value)
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{t_id}")
def eliminar_tarjeta(t_id: int, db: Session = Depends(get_db)):
    t = db.get(Tarjeta, t_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    db.delete(t)
    db.commit()
    return {"ok": True}
