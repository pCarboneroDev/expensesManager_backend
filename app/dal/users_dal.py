from sqlalchemy.orm import Session
from .. import models, schemas

def get_usuario(db: Session, usuario_id: int):
    return db.query(models.User).filter(models.Usuario.id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
#     # usuario es un objeto UsuarioCreate validado
#     db_usuario = models.Usuario(nombre=usuario.nombre, email=usuario.email)
#     db.add(db_usuario)
#     db.commit()
#     db.refresh(db_usuario)
#     return db_usuario