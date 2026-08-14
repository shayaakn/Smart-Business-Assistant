from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    """
    Base schema for Category containing common fields.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the category. Must be unique."
    )
    description: Optional[str] = Field(
        None,
        description="Optional description of the category."
    )

class CategoryCreate(CategoryBase):
    """
    Schema for creating a new Category.
    """
    pass

class CategoryUpdate(BaseModel):
    """
    Schema for updating an existing Category.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    """
    Schema for returning Category data in API responses.
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime] = None