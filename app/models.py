from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.sql import func
from .database import Base
import enum

class Transaction_enum(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    register_date = Column(DateTime(timezone=True), server_default=func.now())

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), index=True)
    amount = Column(Float, index=True)
    transaction_type = Column(Enum(Transaction_enum))
    user_id = Column(String, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    id_category = Column(Integer, ForeignKey("categories.id", onupdate="CASCADE"), nullable=False)

