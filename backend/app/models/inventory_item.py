import uuid
from decimal import Decimal
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.inventory_movement import InventoryMovement

class InventoryItem(BaseModel):
    """
    Represents an individual product or item in the inventory.
    """
    __tablename__ = "inventory_items"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    barcode: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    cost_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    selling_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    reorder_level: Mapped[int] = mapped_column(nullable=False, default=0)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    
    category: Mapped["Category"] = relationship(back_populates="items")
    movements: Mapped[List["InventoryMovement"]] = relationship(
        back_populates="inventory_item",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("cost_price >= 0", name="check_cost_price_positive"),
        CheckConstraint("selling_price >= 0", name="check_selling_price_positive"),
        CheckConstraint("reorder_level >= 0", name="check_reorder_level_positive"),
    )
