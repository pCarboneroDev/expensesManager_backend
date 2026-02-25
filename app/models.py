from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    # Aquí puedes añadir más campos según tu app

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), index=True)
    quantity = Column(Float, index=True)
    id_category = Column(Integer, ForeignKey("categories.id", onupdate="CASCADE"), nullable=False)

