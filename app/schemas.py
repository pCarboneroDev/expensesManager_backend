from pydantic import BaseModel, EmailStr
from datetime import datetime

# Esquema para crear un usuario (lo que la API recibe)
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr  # Validación automática de email

# Esquema para responder con un usuario (lo que la API devuelve)
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    fecha_registro: datetime

    class Config:
        from_attributes = True  # Permite crear el esquema desde un modelo de SQLAlchemy