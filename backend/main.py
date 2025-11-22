from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import re
import urllib.parse
from dotenv import load_dotenv

from controllers.categoria_controller import router as categoria_router
from controllers.producto_controller import router as producto_router
from controllers.usuario_controller import router as usuario_router
from controllers.auth_controller import router as auth_router
from controllers.rol_controller import router as rol_router
from controllers.inventario_controller import router as inventario_router
from controllers.pedido_controller import router as pedido_router
from controllers.detalle_pedido_controller import router as detalle_pedido_router
from controllers.proveedor_controller import router as proveedor_router
from controllers.carrito_controller import router as carrito_router
from controllers.favoritos_controller import router as favoritos_router
from controllers.tarjeta_controller import router as tarjeta_router

app = FastAPI()

load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))
static_dir = os.path.join(base_dir, 'static')
uploads_dir = os.path.join(static_dir, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.middleware("http")
async def sanitize_static_path(request, call_next):
    try:
        path = request.scope.get('path', '')
        if path.startswith('/static/'):
            decoded = urllib.parse.unquote(path)
            prefix = '/static/'
            rel = decoded[len(prefix):]
            last_slash = rel.rfind('/')
            if last_slash != -1:
                dir_part = rel[: last_slash + 1]
                file_part = rel[last_slash + 1 :]
            else:
                dir_part = ''
                file_part = rel
            safe_file = re.sub(r'[<>:\\"|?*]', '_', file_part)
            safe = prefix + dir_part + safe_file
            if safe != decoded:
                request.scope['path'] = safe
                try:
                    request.scope['raw_path'] = safe.encode('utf-8')
                except Exception:
                    pass
    except Exception:
        pass
    return await call_next(request)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

allowed_origins_str = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
)
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

environment = os.getenv("ENVIRONMENT", "development").lower()
if environment == "production":
    allow_credentials_cors = False
else:
    allow_credentials_cors = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials_cors,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    return response

app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(usuario_router)
app.include_router(auth_router)
app.include_router(rol_router)
app.include_router(inventario_router)
app.include_router(pedido_router)
app.include_router(detalle_pedido_router)
app.include_router(proveedor_router)
app.include_router(carrito_router)
app.include_router(favoritos_router)
app.include_router(tarjeta_router)
