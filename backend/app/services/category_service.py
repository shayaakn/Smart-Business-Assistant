from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.crud.category import (
    create_category as crud_create_category,
    get_category as crud_get_category,
    get_categories as crud_get_categories,
    update_category as crud_update_category,
    delete_category as crud_delete_category,
    get_category_by_name as crud_get_category_by_name
)

def create_category(db: Session, category: CategoryCreate) -> Category:
    # Check for duplicate name
    existing_category = crud_get_category_by_name(db, category.name)
    if existing_category:
        raise ValueError(f"A category with name '{category.name}' already exists")

    return crud_create_category(db, category)

def get_category(db: Session, category_id: UUID) -> Optional[Category]:
    return crud_get_category(db, category_id)

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return crud_get_categories(db, skip, limit)

def update_category(db: Session, category_id: UUID, category: CategoryUpdate) -> Optional[Category]:
    existing_category = crud_get_category(db, category_id)
    if not existing_category:
        return None

    # Check for name change validation
    if category.name and category.name != existing_category.name:
        existing_name_category = crud_get_category_by_name(db, category.name)
        if existing_name_category and existing_name_category.id != category_id:
            raise ValueError(f"A category with name '{category.name}' already exists")

    return crud_update_category(db, category_id, category)

def delete_category(db: Session, category_id: UUID) -> bool:
    return crud_delete_category(db, category_id)