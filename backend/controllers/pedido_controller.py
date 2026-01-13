from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import SessionLocal
from dtos.pedido_dto import PedidoCreate, PedidoOut, PedidoUpdate
from models.pedido import Pedido

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PedidoOut)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    db_pedido = Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


@router.get("/", response_model=list[PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()


@router.get("/{pedido_id}", response_model=PedidoOut)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.put("/{pedido_id}", response_model=PedidoOut)
def actualizar_pedido(pedido_id: int, datos: PedidoUpdate, db: Session = Depends(get_db)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(pedido, key, value)
    db.commit()
    db.refresh(pedido)
    return pedido


@router.delete("/{pedido_id}")
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(pedido)
    db.commit()
    return {"ok": True}
