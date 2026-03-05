from dataclasses import dataclass
import datetime

from app.models import Category, Transaction_enum

# @dataclass
# class CategoryEntity:
#     id: int
#     name: str


@dataclass
class TransactionEntity:
    id: int
    date: datetime
    user_id: str
    amount: float
    category: Category
    transaction_type: Transaction_enum
    
    # Propiedad calculada (opcional)
    @property
    def is_expense(self) -> bool:
        return self.transaction_type == Transaction_enum.EXPENSE
    
    @property
    def is_income(self) -> bool:
        return self.transaction_type == Transaction_enum.INCOME