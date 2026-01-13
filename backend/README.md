# Kaio — Backend

Este repositorio contiene el backend del proyecto "Kaio", desarrollado con FastAPI y SQLAlchemy. Este README está adaptado al estado actual del código en la carpeta `backend/` y explica cómo configurar, ejecutar y manejar migraciones (Alembic) y aspectos básicos de seguridad.

Resumen rápido:
- FastAPI para la API.
- SQLAlchemy (ORM) para modelos.
- Alembic para migraciones (carpeta `migraciones/` ya incluida).
- Hashing de contraseñas con `passlib` (archivo `utils/security.py`).

Contenido principal del backend (carpetas relevantes):
- `main.py` — aplicación FastAPI y montaje de routers.
- `models/` — modelos SQLAlchemy (Categoria, Producto, Usuario, Rol, Proveedor, Inventario, Pedido, DetallePedido, Carrito, Favorito, Tarjeta, ...).
- `dtos/` — esquemas pydantic para validación/serialización.
- `controllers/` — routers por recurso (categorias, productos, usuarios, etc.).
- `db/` — base, engine y session.
- `migraciones/` — carpeta de Alembic con `env.py` y `versions/`.
- `utils/security.py` — funciones para hashear/verificar contraseñas.

Requisitos
---------
- Python 3.9+
- Dependencias listadas en `requirements.txt`

Instalación (PowerShell)
------------------------
```powershell
# desde la carpeta raíz del repo
cd backend
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Variables de entorno
--------------------
Crea un archivo `.env` en `backend/` o exporta estas variables en el entorno:
- `SQLALCHEMY_DATABASE_URL` o editar `db/database.py` según tu conexión (ej: `mysql+pymysql://user:pass@localhost:3306/KAIO`).
- `ALLOWED_ORIGINS` (opcional) — orígenes permitidos para CORS.
- `ENVIRONMENT` — `development` o `production`.

Configuración de base de datos y migraciones (Alembic)
----------------------------------------------------
El proyecto incluye una carpeta `migraciones/` con `env.py` y versiones. Para generar y aplicar migraciones:

1) Crear una revisión nueva (autogenerate):

```powershell
cd backend
# generar una nueva revisión (autogenerate inspecciona los modelos actuales)
alembic -c alembic.ini revision --autogenerate -m "describe cambios"
```

2) Revisar el archivo generado en `migraciones/versions/` y ajustarlo manualmente si es necesario (siempre revisa antes de aplicar en producción).

3) Aplicar migraciones:

```powershell
alembic -c alembic.ini upgrade head
```

4) Si necesitas revertir la última migración:

```powershell
alembic -c alembic.ini downgrade -1
```

Notas sobre Alembic en este proyecto:
- El archivo `migraciones/env.py` ya está configurado para cargar `models` desde el paquete `models` del backend. Si cambias el nombre de la carpeta o el path, actualiza `sys.path` en `migraciones/env.py`.
- Si tu `db/database.py` usa una variable distinta para la URL de la base, asegúrate que `alembic.ini` y `migraciones/env.py` apunten a la misma conexión.

Arrancar la aplicación
----------------------
En desarrollo (PowerShell):

```powershell
cd backend
uvicorn main:app --reload --port 8000
```

Endpoints útiles de documentación:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Probar (tests)
--------------
Si agregas tests, puedes ejecutarlos con `pytest` desde `backend/`:

```powershell
pytest -q
```

Seguridad (resumen y recomendaciones)
------------------------------------
- Las contraseñas se almacenan como `hashed_password` usando `passlib` (bcrypt). No guardes contraseñas en texto plano.
- Evita devolver campos sensibles en DTOs de salida (por ejemplo, número completo de tarjeta). Usa DTOs de salida que no incluyan información sensible.
- Implementa autenticación JWT para proteger rutas. Recomendación: usar `python-jose` o `PyJWT` y un middleware/dependency que valide tokens.
- En `main.py` la configuración CORS usa la variable `ALLOWED_ORIGINS` y respeta `ENVIRONMENT`. En producción, fija orígenes explícitos y `ENVIRONMENT=production`.
- Usa HTTPS en producción y configura `Strict-Transport-Security` (ya existe header en `main.py`).

Cómo agregar un nuevo modelo y migración rápida
---------------------------------------------
1) Crear archivo de modelo en `models/` (seguir estilo de `models/categoria.py`).
2) Exportar el modelo en `models/__init__.py` (añadir import en esa lista).
3) Generar una migración autogenerate: `alembic -c alembic.ini revision --autogenerate -m "add X"`.
4) Revisar y aplicar: `alembic -c alembic.ini upgrade head`.

Consideraciones adicionales
---------------------------
- Revisa `db/database.py` para configurar correctamente el motor (sync vs async) según tu despliegue.
- Si vas a manejar información de tarjetas (`tarjeta`), considera no almacenar CVV y encriptar/mascarar números.
- Mantén las dependencias actualizadas y ejecuta `pip-audit`/`safety` en producción.

Lista rápida de routers y modelos incluidos actualmente
----------------------------------------------------
- Routers (carpeta `controllers/`): `categoria`, `producto`, `usuario`, `rol`, `inventario`, `pedido`, `detalle_pedido`, `proveedor`, `carrito`, `favoritos`, `tarjeta`.
- Modelos (carpeta `models/`): `Categoria`, `Producto`, `Usuario`, `Rol`, `Proveedor`, `Inventario`, `Pedido`, `DetallePedido`, `Carrito`, `Favorito`, `Tarjeta`.

Soporte y próximas tareas sugeridas
---------------------------------
- Añadir autenticación JWT y endpoints `/auth/login` y `/auth/refresh`.
- Añadir tests unitarios y de integración para endpoints críticos.
- Revisar controladores que manejan datos sensibles (tarjetas, pagos) y aplicar encriptación/mascarado.
- Crear un pipeline CI que valide linting, tests y ejecute migraciones en entornos de staging.

Si quieres, puedo:
- Añadir el endpoint de login con JWT ahora.
- Generar una migración ejemplo que renombre `contrasena` a `hashed_password` (ya hemos modificado el modelo localmente).
- Actualizar `alembic.ini` o `migraciones/env.py` si quieres centralizar la variable `SQLALCHEMY_DATABASE_URL` desde `.env`.

---

Fin del README — si quieres que lo adapte con tu URL de repositorio, secretos de entorno ejemplo u otros detalles, dime y lo actualizo.
@limiter.limit("5/minute")
async def rate_limited_route():
    return {"message": "Rate limited endpoint"}
```

#### Validación de Datos
```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    nombre: str = Field(..., max_length=50)
```

#### Protección XSS
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["josnishop.com"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://josnishop.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Calidad de Código

#### Code Formatting
```bash
# Formatear código
black .

# Ordenar imports
isort .

# Lint y fix
ruff check . --fix
```

#### Type Checking
```python
from typing import List, Optional

def get_user_orders(
    user_id: int,
    status: Optional[str] = None
) -> List[Order]:
    # Implementation...
```

#### Testing
```python
# tests/test_productos.py
import pytest
from fastapi.testclient import TestClient

def test_crear_producto():
    response = client.post(
        "/api/v1/productos",
        json={
            "nombre": "Test Producto",
            "precio": 100.00
        }
    )
    assert response.status_code == 201
```

### 3. Optimización de Rendimiento

#### Caché
```python
from fastapi_cache.decorator import cache

@router.get("/productos/{id}")
@cache(expire=300)  # Cache por 5 minutos
async def get_producto(id: int):
    return await find_producto(id)
```

#### Consultas Optimizadas
```python
# Eager Loading
query = select(Producto).options(
    joinedload(Producto.categoria),
    joinedload(Producto.resenas)
)
```

#### Paginación Eficiente
```python
from fastapi_pagination import Page, paginate

@router.get("/productos", response_model=Page[ProductoResponse])
async def list_productos(search: str = ""):
    productos = await get_productos_filtered(search)
    return paginate(productos)
```

### 4. Manejo de Errores

#### Error Handling Global
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )
```

#### Validación de Modelos
```python
class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    
    @validator('precio')
    def precio_valido(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v
```

### 5. Logging y Monitoreo

#### Sistema de Logging
```python
import logging

logger = logging.getLogger(__name__)

@router.post("/productos")
async def create_producto(producto: ProductoCreate):
    logger.info(f"Creando producto: {producto.nombre}")
    try:
        # Implementación...
    except Exception as e:
        logger.error(f"Error al crear producto: {str(e)}")
        raise
```

#### Métricas y Monitoreo
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

## 📚 API Documentation

### 🔑 Autenticación

#### JWT Authentication
```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
```

### 📦 Endpoints Principales

#### 1. Gestión de Productos
```python
# Listar productos con filtros
GET /api/v1/productos?categoria={id}&precio_min={valor}&precio_max={valor}

# Crear nuevo producto
POST /api/v1/productos
{
    "nombre": "string",
    "descripcion": "string",
    "precio": float,
    "categoria_id": int,
    "stock": int
}

# Actualizar producto
PUT /api/v1/productos/{id}
```

#### 2. Sistema de Usuarios
```python
# Registro de usuario
POST /api/v1/usuarios/registro
{
    "nombre": "string",
    "email": "string",
    "password": "string",
    "rol_id": int
}

# Perfil de usuario
GET /api/v1/usuarios/perfil
Authorization: Bearer {token}
```

#### 3. Gestión de Pedidos
```python
# Crear pedido
POST /api/v1/pedidos
{
    "usuario_id": int,
    "items": [
        {
            "producto_id": int,
            "cantidad": int
        }
    ]
}

# Listar pedidos con filtros
GET /api/v1/pedidos?estado={estado}&fecha_inicio={date}&fecha_fin={date}
```

#### 4. Sistema de Reseñas
```python
# Añadir reseña
POST /api/v1/resenas
{
    "producto_id": int,
    "usuario_id": int,
    "calificacion": int,
    "comentario": "string"
}

# Listar reseñas por producto
GET /api/v1/resenas/producto/{id}
```

### 🔄 Respuestas Estandarizadas

#### Éxito
```json
{
    "status": "success",
    "data": {
        // datos solicitados
    },
    "message": "Operación exitosa"
}
```

#### Error
```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "Descripción del error"
    }
}
```

### 📝 Paginación Estándar
```python
@router.get("/productos")
async def list_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    sort: str = Query("nombre"),
    order: str = Query("asc")
):
    productos = await get_productos(skip, limit, sort, order)
    return PaginatedResponse(
        data=productos,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )
```

### 🔍 Filtros y Búsqueda
```python
# Ejemplo de endpoint con filtros
GET /api/v1/productos?
    categoria=1&
    precio_min=100&
    precio_max=500&
    ordenar=precio&
    direccion=desc&
    buscar=zapatillas
```

### 📊 Endpoints de Análisis
```python
# Métricas de ventas
GET /api/v1/metricas/ventas?periodo=mensual

# Análisis de productos
GET /api/v1/metricas/productos/top-vendidos

# Estadísticas de usuarios
GET /api/v1/metricas/usuarios/actividad
```

Consulta la documentación interactiva completa en:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Pruebas con Bruno

- En la carpeta `ENDPOINTS/` tienes subcarpetas con archivos `.bru` para probar todos los endpoints principales.
- Abre Bruno, importa la carpeta y ejecuta las requests para verificar el funcionamiento de la API.

---

## 📝 Notas y Funcionalidades Especiales

- **Organización:** Los modelos, controladores y esquemas están organizados por entidad para facilitar la escalabilidad y el mantenimiento.
- **Migraciones:** Todas las migraciones de base de datos se gestionan con Alembic en la carpeta `migraciones/`.
- **Validación:** Los esquemas de validación y serialización están en la carpeta `dtos/`.
- **Pruebas:** Requests de prueba para Bruno en la carpeta `ENDPOINTS/`.
- **Notificaciones:** El sistema envía alertas por correo al vendedor cada vez que se publica una nueva reseña (ver `utils/email_utils.py` y `controllers/resena_controller.py`).
- **Filtrado de comentarios:** Los comentarios ofensivos o inapropiados son detectados y bloqueados antes de publicar o editar una reseña.
- **Configuración de IDE:** La carpeta `.idea/` es solo para configuración de PyCharm/VSCode y puede ser ignorada.
- **Calidad de código:** Usa `black`, `isort` y `ruff` para mantener el código limpio y consistente.

---

## 🤝 Contribuciones

¿Quieres contribuir? ¡Eres bienvenido!  
Por favor, abre un issue o pull request para sugerencias, mejoras o reportar errores.

---

## 👤 Autor

Josthin Paz y Nicol Amaya

---

### 📦 ¿Cómo guardar todas tus dependencias actuales?

Para guardar todas las dependencias instaladas en tu entorno virtual en el archivo `requirements.txt`, ejecuta este comando en la terminal:

```sh
pip freeze > requirements.txt
```

Luego, sube el archivo `requirements.txt` a tu repositorio con tu gestor de versiones.

---

## 🛠️ Recomendaciones para Ingenieros en Sistemas

- Lee y entiende la estructura del proyecto antes de modificar o agregar nuevas funcionalidades.
- Usa entornos virtuales para evitar conflictos de dependencias.
- Mantén la base de datos y las migraciones actualizadas.
- Realiza pruebas de los endpoints con Bruno o la documentación interactiva de FastAPI.
- Sigue las convenciones de estilo y calidad de código (black, isort, ruff).
- Documenta cualquier cambio relevante en el código o en este README.