from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import SessionLocal
from dtos.detalle_pedido_dto import DetallePedidoCreate, DetallePedidoOut, DetallePedidoUpdate
from models.detalle_pedido import DetallePedido

router = APIRouter(prefix="/detalle-pedidos", tags=["detalle-pedidos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DetallePedidoOut)
def crear_detalle(detalle: DetallePedidoCreate, db: Session = Depends(get_db)):
    db_det = DetallePedido(**detalle.dict())
    db.add(db_det)
    db.commit()
    db.refresh(db_det)
    return db_det


@router.get("/", response_model=list[DetallePedidoOut])
def listar_detalles(db: Session = Depends(get_db)):
    return db.query(DetallePedido).all()


@router.get("/{det_id}", response_model=DetallePedidoOut)
def obtener_detalle(det_id: int, db: Session = Depends(get_db)):
    det = db.get(DetallePedido, det_id)
    if not det:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return det


@router.put("/{det_id}", response_model=DetallePedidoOut)
def actualizar_detalle(det_id: int, datos: DetallePedidoUpdate, db: Session = Depends(get_db)):
    det = db.get(DetallePedido, det_id)
    if not det:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(det, key, value)
    db.commit()
    db.refresh(det)
    return det


@router.delete("/{det_id}")
def eliminar_detalle(det_id: int, db: Session = Depends(get_db)):
    det = db.get(DetallePedido, det_id)
    if not det:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    db.delete(det)
    db.commit()
    return {"ok": True}
