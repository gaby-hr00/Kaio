from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from sqlalchemy.orm import Session
from datetime import timedelta
import os

from db.session import SessionLocal
from dtos.usuario_dto import UsuarioCreate, UsuarioLogin, UsuarioOut, Token, RecuperarContrasena, RecuperarContrasenaResponse
from models.usuario import Usuario
from utils.security import get_password_hash, verify_password, create_access_token
from utils.auth import get_current_user
from utils.email import send_recovery_email, generate_temp_password

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UsuarioOut)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    data = usuario.dict()
    plain = data.pop("contrasena", None)
    if plain:
        data["hashed_password"] = get_password_hash(plain)

    # check duplicates: correo, identificacion, celular (if provided)
    correo = data.get("correo")
    if correo:
        existing = db.query(Usuario).filter(Usuario.correo == correo).first()
        if existing:
            raise HTTPException(status_code=400, detail="Correo ya registrado")

    identificacion = data.get("identificacion")
    if identificacion:
        existing = db.query(Usuario).filter(Usuario.identificacion == identificacion).first()
        if existing:
            raise HTTPException(status_code=400, detail="Identificación ya registrada")

    celular = data.get("celular")
    if celular:
        existing = db.query(Usuario).filter(Usuario.celular == celular).first()
        if existing:
            raise HTTPException(status_code=400, detail="Celular ya registrado")

    db_usuario = Usuario(**data)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.post("/login", response_model=Token)
def login(form: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == form.correo).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not verify_password(form.contrasena, usuario.hashed_password or ""):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    access_token = create_access_token({"sub": str(usuario.id), "correo": usuario.correo}, expires_delta=expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2 compatible token endpoint (form data)
    usuario = db.query(Usuario).filter(Usuario.correo == form_data.username).first()
    if not usuario or not verify_password(form_data.password, usuario.hashed_password or ""):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    access_token = create_access_token({"sub": str(usuario.id), "correo": usuario.correo}, expires_delta=expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioOut)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.post("/recuperar-contrasena", response_model=RecuperarContrasenaResponse)
def recuperar_contrasena(data: RecuperarContrasena, db: Session = Depends(get_db)):
    """
    Endpoint para recuperar contraseña.
    Envía una contraseña temporal al email del usuario si existe en la base de datos.
    
    El usuario deberá cambiar esta contraseña temporal en su panel después de iniciar sesión.
    """
    # Verificar si el usuario existe
    usuario = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    
    if not usuario:
        # No revelar si el email existe o no por seguridad
        raise HTTPException(
            status_code=404,
            detail="No encontramos una cuenta con ese correo"
        )
    
    # Generar contraseña temporal
    temp_password = generate_temp_password(8)
    
    # Hashear la contraseña temporal
    hashed_temp_password = get_password_hash(temp_password)
    
    # Actualizar contraseña en la base de datos
    usuario.hashed_password = hashed_temp_password
    db.commit()
    
    # Enviar email con la contraseña temporal
    email_sent = send_recovery_email(usuario.correo, temp_password)
    
    if not email_sent:
        raise HTTPException(
            status_code=500,
            detail="Error al enviar el email. Por favor, intenta más tarde."
        )
    
    return {
        "message": "Se ha enviado una contraseña temporal a tu correo. Por favor, revisa tu bandeja de entrada.",
        "success": True
    }
