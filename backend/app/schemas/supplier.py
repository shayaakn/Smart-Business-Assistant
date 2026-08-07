"""
Pydantic schemas for Supplier model.

This module defines the Pydantic schemas for the Supplier model,
following FastAPI and Pydantic v2 best practices.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class SupplierBase(BaseModel):
    """
    Base schema for Supplier containing common fields.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Supplier's name. Maximum length: 150 characters."
    )
    contact_person: Optional[str] = Field(
        None,
        max_length=150,
        description="Contact person's name. Maximum length: 150 characters."
    )
    email: Optional[EmailStr] = Field(
        None,
        max_length=254,
        description="Supplier's email address. Must be a valid email format. Maximum length: 254 characters."
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Supplier's phone number. Maximum length: 20 characters."
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes about the supplier."
    )

class SupplierCreate(SupplierBase):
    """
    Schema for creating a new Supplier.
    """
    pass

class SupplierUpdate(BaseModel):
    """
    Schema for updating an existing Supplier.
    """
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=150,
        description="Supplier's name. Maximum length: 150 characters."
    )
    contact_person: Optional[str] = Field(
        None,
        max_length=150,
        description="Contact person's name. Maximum length: 150 characters."
    )
    email: Optional[EmailStr] = Field(
        None,
        max_length=254,
        description="Supplier's email address. Must be a valid email format. Maximum length: 254 characters."
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Supplier's phone number. Maximum length: 20 characters."
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes about the supplier."
    )

class SupplierResponse(SupplierBase):
    """
    Schema for returning Supplier data in API responses.
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        ...,
        description="Unique identifier for the supplier."
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the supplier record was created."
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the supplier record was last updated."
    )
    is_deleted: bool = Field(
        False,
        description="Flag indicating whether the supplier record is marked as deleted."
    )
    deleted_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the supplier record was marked as deleted, if applicable."
    )