from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(
        name=category.name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: UUID) -> Optional[Category]:
    category = db.get(Category, category_id)
    if category and not category.is_deleted:
        return category
    return None

def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    result = db.execute(
        select(Category).where(Category.name == name).where(Category.is_deleted.is_(False))
    )
    return result.scalars().first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    result = db.execute(
        select(Category)
        .where(Category.is_deleted.is_(False))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

def update_category(db: Session, category_id: UUID, category: CategoryUpdate) -> Optional[Category]:
    db_category = db.get(Category, category_id)
    if not db_category or db_category.is_deleted:
        return None

    update_data = category.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)

    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: UUID) -> bool:
    db_category = db.get(Category, category_id)
    if not db_category or db_category.is_deleted:
        return False

    db_category.is_deleted = True
    db_category.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_category)
    return True