import uuid
import enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, ForeignKey, DateTime, Enum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.transaction_item import TransactionItem

class TransactionStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Transaction(BaseModel):
    """
    Represents a financial transaction (invoice/sale).
    """
    __tablename__ = "transactions"

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow, 
        nullable=False,
        index=True
    )
    
    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=True,
        index=True
    )
    
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus), 
        default=TransactionStatus.DRAFT, 
        nullable=False
    )
    
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    customer: Mapped["Customer | None"] = relationship(
        foreign_keys=[customer_id]
    )
    transaction_items: Mapped[list["TransactionItem"]] = relationship(
        back_populates="transaction",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="check_subtotal_non_negative"),
        CheckConstraint("discount_amount >= 0", name="check_discount_amount_non_negative"),
        CheckConstraint("tax_amount >= 0", name="check_tax_amount_non_negative"),
        CheckConstraint("total_amount >= 0", name="check_total_amount_non_negative"),
    )