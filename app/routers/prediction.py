from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic.dataclasses import dataclass
from sqlalchemy.orm import Session
from joblib import load

from app.dal import transactions_dal
from app.dto.transaction_entity import TransactionEntity
from app.models import Transaction_enum
from ..database import get_db
from typing import List, Optional


router = APIRouter(
    prefix="/prediction",
    tags=["prediction"],
    responses={404: {"description": "Not found"}}
)
 
@router.get("/")
def predict(
    db: Session = Depends(get_db),
    user_id: Optional[str] = Query(None, description="Filter user ID"),
):
    transactions = transactions_dal.get_filtered_transactions(
        db,
        skip=0,
        limit=1000,
        category_id=None,
        date='month',
        user_id=user_id
    )
    # ir a ruta raiz/models
    model = load('./models/random_forest_model.pkl')  
    data = generate_user(transactions)

    prediction = model.predict([[
        data.age,
        data.gender,
        data.income,
        data.day_of_month,
        data.current_spend,
        data.n_transactions,
        data.avg_tx_value,
        data.active_days,
        data.purchase_frequency
    ]])
    
    return {"message": "Predicción realizada con éxito", "user_id": user_id, "prediction": prediction[0].round(2)}


# n_transactions	avg_tx_value	active_days	purchase_frequency	target_total_spend
@dataclass
class PredictionRequest:
    age: int
    gender: int
    income: float
    day_of_month: int
    current_spend: float
    n_transactions: int
    avg_tx_value: float
    active_days: int
    purchase_frequency: float



def generate_user(transactions) -> PredictionRequest:
    age = 30
    gender = 1
    income = sum(map(lambda t: t.amount, filter(lambda t: t.transaction_type == Transaction_enum.INCOME, transactions)))

    day_of_month = datetime.now().day

    current_spend = sum(map(lambda t: t.amount, filter(lambda t: t.transaction_type == Transaction_enum.EXPENSE, transactions)))

    n_transactions = len(transactions)

    avg_tx_value = current_spend / n_transactions if n_transactions > 0 else 0

    active_days = len([transaction.date for transaction in transactions if transaction.date is not None])


    purchase_frequency = n_transactions / active_days if active_days > 0 else 0
    # target_total_spend = current_spend * (1 + purchase_frequency)

    #print(f"age: {age}, gender: {gender}, income: {income}, day_of_month: {day_of_month}, current_spend: {current_spend}, n_transactions: {n_transactions}, avg_tx_value: {avg_tx_value}, active_days: {active_days}, purchase_frequency: {purchase_frequency}")

    return PredictionRequest(
        age=age,
        gender=gender,
        income=income,
        day_of_month=day_of_month,
        current_spend=current_spend,
        n_transactions=n_transactions,
        avg_tx_value=avg_tx_value,
        active_days=active_days,
        purchase_frequency=purchase_frequency
    )
