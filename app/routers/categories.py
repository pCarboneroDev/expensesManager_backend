from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas
from ..dal import categories_dal
from ..database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=list[schemas.CategoriesResponse])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = categories_dal.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=schemas.CategoriesResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = categories_dal.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="category not found")
    return db_category