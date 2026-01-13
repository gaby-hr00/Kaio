from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from dtos.categoria_dto import CategoriaCreate, CategoriaOut, CategoriaUpdate
from models.categoria import Categoria

router = APIRouter(prefix="/categorias", tags=["categorias"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.post("/", response_model=CategoriaOut)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@router.get("/", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()


@router.get("/{categoria_id}", response_model=CategoriaOut)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.put("/{categoria_id}", response_model=CategoriaOut)
def actualizar_categoria(
    categoria_id: int, datos: CategoriaUpdate, db: Session = Depends(get_db)
):
    categoria = db.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(categoria, key, value)
        
    db.commit()
    db.refresh(categoria)
    return categoria


@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db.delete(categoria)
    db.commit()
    
    return {"ok": True}