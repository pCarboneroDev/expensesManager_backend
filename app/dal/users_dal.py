import datetime

from sqlalchemy.orm import Session
from .. import models, schemas

def get_usuario(db: Session, usuario_id: int):
    return db.query(models.User).filter(models.User.id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.CreateUser):
    db_user = models.User(email=user.email, id=user.id, register_date= datetime.datetime.now())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user