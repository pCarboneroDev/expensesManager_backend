from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.utils.filters import transaction_filters

from .. import schemas
from ..dal import transactions_dal
from ..database import get_db

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}}
)

# @router.get("", response_model=list[schemas.TransactionsResponse])
# def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     # transactions = transactions_dal.get_month_transactions(db, skip=skip, limit=limit)
#     transactions = transactions_dal.get_transactions(db, skip=skip, limit=limit)
#     return transactions



@router.get("", response_model=list[schemas.TransactionsResponse])
def get_transactions(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=500, description="Límite de registros"),
    category_id: Optional[int] = Query(None, description="Filtrar por ID de categoría"),
    date: Optional[str] = Query(None, min_length=1, description="Filtrar por cantidad (búsqueda parcial)"),
    db: Session = Depends(get_db)
):
    transactions = transactions_dal.get_filtered_transactions(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        date=date
    )
    
    return transactions
    # return schemas.PaginatedTransactionsResponse(
    #     items=transactions,
    #     skip=skip,
    #     limit=limit,
    # )





@router.get("/{transaction_id}", response_model=schemas.TransactionsResponse)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = transactions_dal.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="transaction not found")
    return db_transaction

@router.post("", response_model=schemas.TransactionsResponse)
def create_transaction(transaction: schemas.CreateTransaction, db: Session = Depends(get_db)):
    # Verificamos si el usuario ya existe
    # db_transaction = transactions_dal.get_transaction(db, transaction_id=transaction.id)
    # if db_transaction:
    #     raise HTTPException(status_code=400, detail="El transaction already exists (how did you do it??)")
    return transactions_dal.create_transaction(db=db, transaction=transaction)

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    deleted = transactions_dal.delete_transaction(db = db, transaction_id = transaction_id)
    
    if deleted is None:
        raise HTTPException(status_code=404, detail="transaction not found")
    elif deleted:
        return {"detail": "transaction deleted successfully"}
    else:       
        raise HTTPException(status_code=500, detail="Error deleting transaction")
    
@router.put("/{transaction_id}", response_model=schemas.TransactionsResponse)
def update_transaction(transaction_id: int, transaction: schemas.CreateTransaction, db: Session = Depends(get_db)):
    updated_transaction = transactions_dal.update_transaction(db=db, transaction_id=transaction_id, transaction=transaction)
    
    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="transaction not found")
    elif updated_transaction:
        return updated_transaction
    else:       
        raise HTTPException(status_code=500, detail="Error updating transaction")
    
