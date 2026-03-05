import enum
from typing import Optional
from fastapi import Query

class transaction_filters(enum.Enum):
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class PaginatedTransaction:
    def __init__(
        self,
        # Paginación
        page: int = Query(1, ge=1, description="number of pages"),
        limit: int = Query(20, ge=1, le=100, description="Elemens per page"),
        # Filtros
        category: Optional[int] = Query(None, description="Filter by category"),
        date_filter: Optional[str] = Query(None, description="Filter by date")
    ):
        self.page = page
        self.limit = limit
        self.category = category
        self.date_filter = date_filter