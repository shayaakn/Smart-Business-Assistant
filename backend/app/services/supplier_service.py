"""
Supplier Service Layer.

This module provides business logic for Supplier operations.
It acts as an intermediary between API routes and CRUD operations,
enforcing business rules and validation without direct database access.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from app.crud.supplier import (
    create_supplier as crud_create_supplier,
    get_supplier as crud_get_supplier,
    get_suppliers as crud_get_suppliers,
    update_supplier as crud_update_supplier,
    delete_supplier as crud_delete_supplier,
    get_supplier_by_email as crud_get_supplier_by_email
)

def create_supplier(db: Session, supplier: SupplierCreate) -> Supplier:
    """
    Create a new supplier with business validation.

    Args:
        db: SQLAlchemy database session
        supplier: SupplierCreate schema containing supplier data

    Returns:
        The created Supplier ORM object

    Raises:
        ValueError: If a supplier with the same email already exists
    """
    # Check for duplicate email
    if supplier.email:
        existing_supplier = crud_get_supplier_by_email(db, supplier.email)
        if existing_supplier:
            raise ValueError(f"A supplier with email '{supplier.email}' already exists")

    # Create the supplier using CRUD function
    return crud_create_supplier(db, supplier)

def get_supplier(db: Session, supplier_id: UUID) -> Optional[Supplier]:
    """
    Retrieve a supplier by their ID.

    Args:
        db: SQLAlchemy database session
        supplier_id: UUID of the supplier to retrieve

    Returns:
        Supplier ORM object if found, None otherwise
    """
    return crud_get_supplier(db, supplier_id)

def get_suppliers(db: Session, skip: int = 0, limit: int = 100) -> list[Supplier]:
    """
    Retrieve a list of suppliers with pagination support.

    Args:
        db: SQLAlchemy database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)

    Returns:
        List of Supplier ORM objects
    """
    return crud_get_suppliers(db, skip, limit)

def update_supplier(db: Session, supplier_id: UUID, supplier: SupplierUpdate) -> Optional[Supplier]:
    """
    Update an existing supplier with business validation.

    Args:
        db: SQLAlchemy database session
        supplier_id: UUID of the supplier to update
        supplier: SupplierUpdate schema containing updated data

    Returns:
        Updated Supplier ORM object if successful, None otherwise

    Raises:
        ValueError: If attempting to change email to one that already belongs to another supplier
    """
    # Get the existing supplier
    existing_supplier = crud_get_supplier(db, supplier_id)
    if not existing_supplier:
        return None

    # Check for email change validation
    if supplier.email and supplier.email != existing_supplier.email:
        existing_email_supplier = crud_get_supplier_by_email(db, supplier.email)
        if existing_email_supplier and existing_email_supplier.id != supplier_id:
            raise ValueError(f"A supplier with email '{supplier.email}' already exists")

    # Update the supplier using CRUD function
    return crud_update_supplier(db, supplier_id, supplier)

def delete_supplier(db: Session, supplier_id: UUID) -> bool:
    """
    Delete a supplier.

    Args:
        db: SQLAlchemy database session
        supplier_id: UUID of the supplier to delete

    Returns:
        True if deletion was successful, False otherwise
    """
    return crud_delete_supplier(db, supplier_id)