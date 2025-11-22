from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import SessionLocal
from dtos.carrito_dto import CarritoCreate, CarritoOut, CarritoUpdate
from models.carrito import Carrito

router = APIRouter(prefix="/carritos", tags=["carritos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CarritoOut)
def crear_carrito(item: CarritoCreate, db: Session = Depends(get_db)):
    db_item = Carrito(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[CarritoOut])
def listar_carritos(db: Session = Depends(get_db)):
    return db.query(Carrito).all()


@router.get("/{item_id}", response_model=CarritoOut)
def obtener_carrito(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Carrito, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item de carrito no encontrado")
    return item


@router.put("/{item_id}", response_model=CarritoOut)
def actualizar_carrito(item_id: int, datos: CarritoUpdate, db: Session = Depends(get_db)):
    item = db.get(Carrito, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item de carrito no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def eliminar_carrito(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Carrito, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item de carrito no encontrado")
    db.delete(item)
    db.commit()
    return {"ok": True}
