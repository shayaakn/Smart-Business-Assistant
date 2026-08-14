from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.models.inventory_item import InventoryItem
from app.schemas.inventory_item import InventoryItemCreate, InventoryItemUpdate

def create_inventory_item(db: Session, item: InventoryItemCreate) -> InventoryItem:
    db_item = InventoryItem(
        name=item.name,
        sku=item.sku,
        barcode=item.barcode,
        description=item.description,
        cost_price=item.cost_price,
        selling_price=item.selling_price,
        reorder_level=item.reorder_level,
        unit=item.unit,
        category_id=item.category_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_inventory_item(db: Session, item_id: UUID) -> Optional[InventoryItem]:
    item = db.get(InventoryItem, item_id)
    if item and not item.is_deleted:
        return item
    return None

def get_inventory_item_by_sku(db: Session, sku: str) -> Optional[InventoryItem]:
    result = db.execute(
        select(InventoryItem).where(InventoryItem.sku == sku).where(InventoryItem.is_deleted.is_(False))
    )
    return result.scalars().first()

def get_inventory_items(db: Session, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
    result = db.execute(
        select(InventoryItem)
        .where(InventoryItem.is_deleted.is_(False))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

def update_inventory_item(db: Session, item_id: UUID, item: InventoryItemUpdate) -> Optional[InventoryItem]:
    db_item = db.get(InventoryItem, item_id)
    if not db_item or db_item.is_deleted:
        return None

    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item

def delete_inventory_item(db: Session, item_id: UUID) -> bool:
    db_item = db.get(InventoryItem, item_id)
    if not db_item or db_item.is_deleted:
        return False

    db_item.is_deleted = True
    db_item.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_item)
    return True
