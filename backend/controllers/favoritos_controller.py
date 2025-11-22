from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import SessionLocal
from dtos.favoritos_dto import FavoritoCreate, FavoritoOut, FavoritoUpdate
from models.favoritos import Favorito

router = APIRouter(prefix="/favoritos", tags=["favoritos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=FavoritoOut)
def crear_favorito(fav: FavoritoCreate, db: Session = Depends(get_db)):
    db_fav = Favorito(**fav.dict())
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav


@router.get("/", response_model=list[FavoritoOut])
def listar_favoritos(db: Session = Depends(get_db)):
    return db.query(Favorito).all()


@router.get("/{fav_id}", response_model=FavoritoOut)
def obtener_favorito(fav_id: int, db: Session = Depends(get_db)):
    fav = db.get(Favorito, fav_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    return fav


@router.put("/{fav_id}", response_model=FavoritoOut)
def actualizar_favorito(fav_id: int, datos: FavoritoUpdate, db: Session = Depends(get_db)):
    fav = db.get(Favorito, fav_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(fav, key, value)
    db.commit()
    db.refresh(fav)
    return fav


@router.delete("/{fav_id}")
def eliminar_favorito(fav_id: int, db: Session = Depends(get_db)):
    fav = db.get(Favorito, fav_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    db.delete(fav)
    db.commit()
    return {"ok": True}
