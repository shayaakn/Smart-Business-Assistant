from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from app.models.base_model import BaseModel

class Supplier(BaseModel):
    __tablename__ = "suppliers"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    contact_person: Mapped[str] = mapped_column(String(150), nullable=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=True, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)