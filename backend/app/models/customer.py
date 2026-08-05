from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from app.models.base_model import BaseModel

class Customer(BaseModel):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=True, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)