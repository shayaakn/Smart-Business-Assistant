from decimal import Decimal
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class InventoryItemBase(BaseModel):
    """
    Base schema for InventoryItem containing common fields.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the inventory item."
    )
    sku: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique Stock Keeping Unit (SKU)."
    )
    barcode: Optional[str] = Field(
        None,
        max_length=100,
        description="Optional barcode for the item."
    )
    description: Optional[str] = Field(
        None,
        description="Detailed description of the item."
    )
    cost_price: Decimal = Field(
        ...,
        ge=0,
        description="Cost price of the item. Must be non-negative."
    )
    selling_price: Decimal = Field(
        ...,
        ge=0,
        description="Selling price of the item. Must be non-negative."
    )
    reorder_level: int = Field(
        0,
        ge=0,
        description="Minimum stock level before reordering. Must be non-negative."
    )
    unit: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Unit of measurement (e.g., kg, pcs)."
    )
    category_id: UUID = Field(
        ...,
        description="ID of the category this item belongs to."
    )

class InventoryItemCreate(InventoryItemBase):
    """
    Schema for creating a new InventoryItem.
    """
    pass

class InventoryItemUpdate(BaseModel):
    """
    Schema for updating an existing InventoryItem.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    barcode: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    cost_price: Optional[Decimal] = Field(None, ge=0)
    selling_price: Optional[Decimal] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = Field(None, min_length=1, max_length=50)
    category_id: Optional[UUID] = None

class InventoryItemResponse(InventoryItemBase):
    """
    Schema for returning InventoryItem data in API responses.
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime] = None