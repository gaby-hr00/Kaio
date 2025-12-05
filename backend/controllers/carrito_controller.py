from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from db.session import SessionLocal
from models.carrito import Carrito
from models.producto import Producto
from dtos.carrito_dto import CarritoCreate, CarritoOut, CarritoUpdate

router = APIRouter(prefix="/carritos", tags=["carritos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CarritoOut)
def crear_carrito(item: CarritoCreate, db: Session = Depends(get_db)):
    existente = db.query(Carrito).filter(
        Carrito.usuario_id == item.usuario_id,
        Carrito.producto_id == item.producto_id
    ).first()

    if existente:
        existente.cantidad += item.cantidad
        db.commit()
        db.refresh(existente)
        return existente

    nuevo = Carrito(**item.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo



@router.get("/{item_id}", response_model=CarritoOut)
def obtener_carrito(item_id: int, db: Session = Depends(get_db)):
    try:
        item = (
            db.query(Carrito)
            .options(joinedload(Carrito.producto))
            .filter(Carrito.id == item_id)
            .first()
        )
        if not item:
            raise HTTPException(status_code=404, detail="Item de carrito no encontrado")
        return item
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{item_id}", response_model=CarritoOut)
def actualizar_carrito(item_id: int, datos: CarritoUpdate, db: Session = Depends(get_db)):
    try:
        item = db.get(Carrito, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item de carrito no encontrado")
        for key, value in datos.dict(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/vaciar")
def vaciar_carrito(user_id: int, db: Session = Depends(get_db)):
    try:
        db.query(Carrito).filter(Carrito.usuario_id == user_id).delete()
        db.commit()
        return {"ok": True}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
