import uuid
import enum
from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, DateTime, Enum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.inventory_item import InventoryItem

class MovementType(str, enum.Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    RETURN = "RETURN"
    MANUAL_ADJUSTMENT = "MANUAL_ADJUSTMENT"

class InventoryMovement(BaseModel):
    """
    Records every stock movement (in/out) for an inventory item.
    """
    __tablename__ = "inventory_movements"

    inventory_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("inventory_items.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    movement_type: Mapped[MovementType] = mapped_column(Enum(MovementType), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    movement_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    transaction_item_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)

    inventory_item: Mapped["InventoryItem"] = relationship(back_populates="movements")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_movement_quantity_positive"),
    )
