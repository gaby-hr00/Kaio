from db.session import SessionLocal
from models.categoria import Categoria

db = SessionLocal()

categorias = ["Maquillaje","Cuidado de la piel","Accesorios","Cuidado capilar", "Perfumería", "Uñas"]

for nombre in categorias:
    if not db.query(Categoria).filter(Categoria.nombre == nombre).first():
        db.add(Categoria(nombre=nombre))

db.commit()
db.close()
print("Categorias insertadas correctamente ✅")