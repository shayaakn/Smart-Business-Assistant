from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.inventory_item import InventoryItem
from app.schemas.inventory_item import InventoryItemCreate, InventoryItemUpdate
from app.crud.inventory_item import (
    create_inventory_item as crud_create_inventory_item,
    get_inventory_item as crud_get_inventory_item,
    get_inventory_items as crud_get_inventory_items,
    update_inventory_item as crud_update_inventory_item,
    delete_inventory_item as crud_delete_inventory_item,
    get_inventory_item_by_sku as crud_get_inventory_item_by_sku
)

def create_inventory_item(db: Session, item: InventoryItemCreate) -> InventoryItem:
    # Check for duplicate SKU
    existing_item = crud_get_inventory_item_by_sku(db, item.sku)
    if existing_item:
        raise ValueError(f"An item with SKU '{item.sku}' already exists")

    return crud_create_inventory_item(db, item)

def get_inventory_item(db: Session, item_id: UUID) -> Optional[InventoryItem]:
    return crud_get_inventory_item(db, item_id)

def get_inventory_items(db: Session, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
    return crud_get_inventory_items(db, skip, limit)

def update_inventory_item(db: Session, item_id: UUID, item: InventoryItemUpdate) -> Optional[InventoryItem]:
    existing_item = crud_get_inventory_item(db, item_id)
    if not existing_item:
        return None

    # Check for SKU change validation
    if item.sku and item.sku != existing_item.sku:
        existing_sku_item = crud_get_inventory_item_by_sku(db, item.sku)
        if existing_sku_item and existing_sku_item.id != item_id:
            raise ValueError(f"An item with SKU '{item.sku}' already exists")

    return crud_update_inventory_item(db, item_id, item)

def delete_inventory_item(db: Session, item_id: UUID) -> bool:
    return crud_delete_inventory_item(db, item_id)