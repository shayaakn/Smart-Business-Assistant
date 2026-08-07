"""
CRUD operations for Supplier model.

This module provides database operations for the Supplier entity using SQLAlchemy ORM.
All functions accept a SQLAlchemy Session for dependency injection and return Supplier ORM objects.
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate

def create_supplier(db: Session, supplier: SupplierCreate) -> Supplier:
    """
    Create a new supplier in the database.

    Args:
        db: SQLAlchemy database session
        supplier: SupplierCreate schema containing supplier data

    Returns:
        The created Supplier ORM object
    """
    db_supplier = Supplier(
        name=supplier.name,
        contact_person=supplier.contact_person,
        email=supplier.email,
        phone=supplier.phone,
        notes=supplier.notes
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def get_supplier(db: Session, supplier_id: UUID) -> Optional[Supplier]:
    """
    Retrieve a supplier by their ID.

    Args:
        db: SQLAlchemy database session
        supplier_id: UUID of the supplier to retrieve

    Returns:
        Supplier ORM object if found and not soft-deleted, None otherwise
    """
    supplier = db.get(Supplier, supplier_id)
    if supplier and not supplier.is_deleted:
        return supplier
    return None

def get_supplier_by_email(db: Session, email: str) -> Optional[Supplier]:
    """
    Retrieve a supplier by their email address.

    Args:
        db: SQLAlchemy database session
        email: Email address to search for

    Returns:
        Supplier ORM object if found, None otherwise
    """
    result = db.execute(
        select(Supplier).where(Supplier.email == email).where(Supplier.is_deleted.is_(False))
    )
    return result.scalars().first()

def get_suppliers(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[Supplier]:
    """
    Retrieve a list of suppliers with pagination support.

    Args:
        db: SQLAlchemy database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)

    Returns:
        List of Supplier ORM objects
    """
    result = db.execute(
        select(Supplier)
        .where(Supplier.is_deleted.is_(False))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

def update_supplier(
    db: Session,
    supplier_id: UUID,
    supplier: SupplierUpdate
) -> Optional[Supplier]:
    """
    Update an existing supplier.

    Args:
        db: SQLAlchemy database session
        supplier_id: UUID of the supplier to update
        supplier: SupplierUpdate schema containing updated data

    Returns:
        Updated Supplier ORM object if successful, None otherwise
    """
    db_supplier = db.get(Supplier, supplier_id)
    if not db_supplier:
        return None

    update_data = supplier.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_supplier, field, value)

    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session, supplier_id: UUID) -> bool:
    """
    Delete a supplier (soft delete if supported, otherwise hard delete).

    Args:
        db: SQLAlchemy database session
        supplier_id: UUID of the supplier to delete

    Returns:
        True if deletion was successful, False otherwise
    """
    db_supplier = db.get(Supplier, supplier_id)
    if not db_supplier:
        return False

    # Perform soft delete (set is_deleted flag)
    db_supplier.is_deleted = True
    db.commit()
    db.refresh(db_supplier)
    return True