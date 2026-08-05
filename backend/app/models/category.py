from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from app.models.base_model import BaseModel
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.inventory_item import InventoryItem

class Category(BaseModel):
    """
    Represents a product category for grouping inventory items.
    """
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    items: Mapped[List["InventoryItem"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan"
    )
