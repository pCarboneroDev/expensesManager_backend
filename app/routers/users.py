from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas
from ..dal import users_dal
from ..database import get_db

# Crear un router específico para usuarios
router = APIRouter(
    prefix="/users",          # 👈 Todos los endpoints empezarán con /usuarios
    tags=["users"],            # 👈 Se agruparán en la documentación
    responses={404: {"description": "No encontrado"}}
)

# @router.post("/users/", response_model=schemas.UsuarioResponse)
# def create_user(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
#     # Verificamos si el usuario ya existe
#     db_usuario = personas_dal.get_usuario_por_email(db, email=usuario.email)
#     if db_usuario:
#         raise HTTPException(status_code=400, detail="El email ya está registrado")
#     return personas_dal.crear_usuario(db=db, usuario=usuario)

@router.get("", response_model=list[schemas.UsersResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios = users_dal.get_usuarios(db, skip=skip, limit=limit)
    return usuarios

@router.get("/{usuario_id}", response_model=schemas.UsersResponse)
def read_user(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = users_dal.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario