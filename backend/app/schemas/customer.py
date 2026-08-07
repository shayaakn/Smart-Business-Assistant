"""
Pydantic schemas for Customer model.

This module defines the Pydantic schemas for the Customer model,
following FastAPI and Pydantic v2 best practices.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class CustomerBase(BaseModel):
    """
    Base schema for Customer containing common fields.

    This schema is used as a base for other schemas and contains
    the core fields that are shared across different operations.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Customer's full name. Maximum length: 150 characters."
    )
    email: Optional[EmailStr] = Field(
        None,
        max_length=254,
        description="Customer's email address. Must be a valid email format. Maximum length: 254 characters."
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Customer's phone number. Maximum length: 20 characters."
    )
    address: Optional[str] = Field(
        None,
        max_length=500,
        description="Customer's physical address. Maximum length: 500 characters."
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes about the customer."
    )

class CustomerCreate(CustomerBase):
    """
    Schema for creating a new Customer.

    This schema inherits all fields from CustomerBase and is used
    for customer creation operations.
    """
    pass

class CustomerUpdate(BaseModel):
    """
    Schema for updating an existing Customer.

    This schema allows partial updates and makes all fields optional.
    """
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=150,
        description="Customer's full name. Maximum length: 150 characters."
    )
    email: Optional[EmailStr] = Field(
        None,
        max_length=254,
        description="Customer's email address. Must be a valid email format. Maximum length: 254 characters."
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Customer's phone number. Maximum length: 20 characters."
    )
    address: Optional[str] = Field(
        None,
        max_length=500,
        description="Customer's physical address. Maximum length: 500 characters."
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes about the customer."
    )

class CustomerResponse(CustomerBase):
    """
    Schema for returning Customer data in API responses.

    This schema includes the database ID and timestamps for full
    customer representation in API responses.
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        ...,
        description="Unique identifier for the customer."
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the customer record was created."
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the customer record was last updated."
    )
    is_deleted: bool = Field(
        False,
        description="Flag indicating whether the customer record is marked as deleted."
    )
    deleted_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the customer record was marked as deleted, if applicable."
    )