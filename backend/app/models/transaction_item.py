import uuid
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import Numeric, ForeignKey, CheckConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.inventory_item import InventoryItem

class TransactionItem(BaseModel):
    """
    Represents an individual item within a transaction.
    """
    __tablename__ = "transaction_items"

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    inventory_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("inventory_items.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    line_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    # Relationships
    transaction: Mapped["Transaction"] = relationship(back_populates="transaction_items")
    inventory_item: Mapped["InventoryItem"] = relationship(back_populates="transaction_items")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_transaction_item_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="check_transaction_item_unit_price_non_negative"),
        CheckConstraint("discount_amount >= 0", name="check_transaction_item_discount_amount_non_negative"),
        CheckConstraint("tax_amount >= 0", name="check_transaction_item_tax_amount_non_negative"),
        CheckConstraint("line_total >= 0", name="check_transaction_item_line_total_non_negative"),
    )