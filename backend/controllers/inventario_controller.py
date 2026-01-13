from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import SessionLocal
from dtos.inventario_dto import InventarioCreate, InventarioOut, InventarioUpdate
from models.inventario import Inventario

router = APIRouter(prefix="/inventarios", tags=["inventarios"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=InventarioOut)
def crear_inventario(inv: InventarioCreate, db: Session = Depends(get_db)):
    db_inv = Inventario(**inv.dict())
    db.add(db_inv)
    db.commit()
    db.refresh(db_inv)
    return db_inv


@router.get("/", response_model=list[InventarioOut])
def listar_inventarios(db: Session = Depends(get_db)):
    return db.query(Inventario).all()


@router.get("/{inv_id}", response_model=InventarioOut)
def obtener_inventario(inv_id: int, db: Session = Depends(get_db)):
    inv = db.get(Inventario, inv_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inv


@router.put("/{inv_id}", response_model=InventarioOut)
def actualizar_inventario(inv_id: int, datos: InventarioUpdate, db: Session = Depends(get_db)):
    inv = db.get(Inventario, inv_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(inv, key, value)
    db.commit()
    db.refresh(inv)
    return inv


@router.delete("/{inv_id}")
def eliminar_inventario(inv_id: int, db: Session = Depends(get_db)):
    inv = db.get(Inventario, inv_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    db.delete(inv)
    db.commit()
    return {"ok": True}
