from typing import Optional

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy import extract

from app.dto.transaction_entity import TransactionEntity
from .. import models, schemas
from .categories_dal import get_category
from ..utils.filters import transaction_filters


def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    #return db.query(models.Transaction).offset(skip).limit(limit).all()
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    trans_ent = []
    for t in transactions:
        new_category = get_category(db, t.id_category)

        trans_ent.append(
            TransactionEntity(
                id=t.id,
                date=t.date,
                amount=t.amount,
                transaction_type=t.transaction_type,
                user_id=t.user_id,
                category = models.Category(
                    id= new_category.id,
                    name= new_category.name
                )
            )
        )  
    return trans_ent

def get_last_transactions(db: Session, limit: int = 10, user_id: Optional[str] = None):
    #return db.query(models.Transaction).offset(skip).limit(limit).all()
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.date.desc()).limit(limit).all()
    
    trans_ent = []
    for t in transactions:
        new_category = get_category(db, t.id_category)

        trans_ent.append(
            TransactionEntity(
                id=t.id,
                date=t.date,
                amount=t.amount,
                transaction_type=t.transaction_type,
                user_id=t.user_id,
                category = models.Category(
                    id= new_category.id,
                    name= new_category.name
                )
            )
        )  
    return trans_ent

def get_month_transactions(db: Session, skip: int = 0, limit: int = 100):
    transactions = db.query(models.Transaction).filter(
    extract('month', models.Transaction.date) == datetime.now().month,  
    extract('year', models.Transaction.date) == datetime.now().year).all()
    trans_ent = []
    for t in transactions:
        new_category = get_category(db, t.id_category)

        trans_ent.append(
            TransactionEntity(
                id=t.id,
                date=t.date,
                amount=t.amount,
                transaction_type=t.transaction_type,
                user_id=t.user_id,
                category = models.Category(
                    id= new_category.id,
                    name= new_category.name
                )
            )
        )  
    return trans_ent

def create_transaction(db: Session, transaction: schemas.CreateTransaction):
    # usuario es un objeto UsuarioCreate validado
    db_transaction = models.Transaction(
        date = transaction.date, 
        amount = transaction.amount, 
        transaction_type = transaction.transaction_type, 
        user_id = transaction.user_id,
        id_category = transaction.id_category
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    t = db.query(models.Transaction).filter(models.Transaction.id == db_transaction.id).first()
    category = get_category(db, t.id_category)

    transaction = TransactionEntity(
        id=t.id,
        date=t.date,
        amount=t.amount,
        transaction_type=t.transaction_type,
        user_id=t.user_id,
        category = models.Category(
            id= category.id,
            name= category.name
        )
    )
    return transaction

def delete_transaction(db: Session, transaction_id: int):
    try:
        transaction_del = get_transaction(db=db, transaction_id=transaction_id)
        if not transaction_del:
            return None
        db.delete(transaction_del)
        db.commit()
        return True
    except:
        db.rollback()
        return False
    
def update_transaction(db: Session, transaction_id: int, transaction: schemas.CreateTransaction):
    try:
        transaction_upd = get_transaction(db=db, transaction_id=transaction_id)
        if not transaction_upd:
            return None
        transaction_upd.date = transaction.date
        transaction_upd.amount = transaction.amount
        transaction_upd.transaction_type = transaction.transaction_type
        transaction_upd.user_id = transaction.user_id
        transaction_upd.id_category = transaction.id_category

        db.commit()
        db.refresh(transaction_upd)
        return _get_transaction_complete(db, transaction_upd.id)
    except:
        db.rollback()
        return False
    

def get_filtered_transactions(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None,
    date: Optional[str] = None,
    user_id: Optional[str] = None
):
    query = db.query(models.Transaction)

    if user_id:
        query = query.filter(models.Transaction.user_id == user_id)
    
    # Aplicar filtros
    if category_id:
        query = query.filter(models.Transaction.id_category == category_id)
    
    if date:
        now = datetime.now()

        if date.lower() in [transaction_filters.MONTH.value, transaction_filters.MONTH.name.lower()]:
            query = query.filter(
                extract('month', models.Transaction.date) == now.month,
                extract('year', models.Transaction.date) == now.year
            )
        elif date.lower() in [transaction_filters.YEAR.value, transaction_filters.YEAR.name.lower()]:
            # Filtrar por año actual
            query = query.filter(extract('year', models.Transaction.date) == now.year)
        elif date.lower() in [transaction_filters.WEEK.value, transaction_filters.WEEK.name.lower()]:
            # Filtrar por semana actual
            start_of_week = now - timedelta(days=now.weekday())  # Lunes de la semana actual
            end_of_week = start_of_week + timedelta(days=6)  # Domingo de la semana actual
            query = query.filter(models.Transaction.date >= start_of_week, models.Transaction.date <= end_of_week)
            
    
    transactions = query.offset(skip).limit(limit).all()
    response = []

    for t in transactions:
        response.append(_get_transaction_complete(db = db, transaction_id = t.id))

    # Aplicar paginación
    return response
    

# conseguir la transaccion completo
def _get_transaction_complete(db: Session, transaction_id: int):
    t = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    category = get_category(db, t.id_category)

    transaction = TransactionEntity(
        id=t.id,
        date=t.date,
        amount=t.amount,
        transaction_type=t.transaction_type,
        user_id=t.user_id,
        category = models.Category(
            id= category.id,
            name= category.name
        )
    )
    return transaction
