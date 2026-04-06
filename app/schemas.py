from typing import List, Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.models import Category
from app.utils.filters import transaction_filters
from .models import Transaction_enum

# Esquema para crear un usuario (lo que la API recibe)
class CreateUser(BaseModel):
    id: str
    email: EmailStr

# Esquema para responder con un usuario (lo que la API devuelve)
class UsersResponse(BaseModel):
    id: str
    email: str
    register_date: datetime

    class Config:
        from_attributes = True  # Permite crear el esquema desde un modelo de SQLAlchemy

class CategoriesResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# class TransactionsResponse(BaseModel):
#     id: int
#     date: datetime
#     amount: float
#     transaction_type: Transaction_enum
#     user_id: str
#     id_category: int

#     class Config:
#         from_attributes = True

class TransactionsResponse(BaseModel):
    id: int
    date: datetime
    amount: float
    transaction_type: Transaction_enum
    user_id: str
    category: CategoriesResponse

    class Config:
        from_attributes = True

class CreateTransaction(BaseModel):
    date: datetime
    amount: float
    transaction_type: Transaction_enum
    user_id: str
    id_category: int

    class Config:
        from_attributes = True

class PaginatedTransactionsResponse(BaseModel):
    items: List[TransactionsResponse]
    skip: int
    limit: int

    class Config:
        from_attributes = True
