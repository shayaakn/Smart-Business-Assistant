"""
CRUD operations for Customer model.

This module provides database operations for the Customer entity using SQLAlchemy ORM.
All functions accept a SQLAlchemy Session for dependency injection and return Customer ORM objects.
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """
    Create a new customer in the database.

    Args:
        db: SQLAlchemy database session
        customer: CustomerCreate schema containing customer data

    Returns:
        The created Customer ORM object
    """
    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        notes=customer.notes
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: UUID) -> Optional[Customer]:
    """
    Retrieve a customer by their ID.

    Args:
        db: SQLAlchemy database session
        customer_id: UUID of the customer to retrieve

    Returns:
        Customer ORM object if found and not soft-deleted, None otherwise
    """
    customer = db.get(Customer, customer_id)
    if customer and not customer.is_deleted:
        return customer
    return None

def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    """
    Retrieve a customer by their email address.

    Args:
        db: SQLAlchemy database session
        email: Email address to search for

    Returns:
        Customer ORM object if found, None otherwise
    """
    result = db.execute(
        select(Customer).where(Customer.email == email).where(Customer.is_deleted.is_(False))
    )
    return result.scalars().first()

def get_customers(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[Customer]:
    """
    Retrieve a list of customers with pagination support.

    Args:
        db: SQLAlchemy database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)

    Returns:
        List of Customer ORM objects
    """
    result = db.execute(
        select(Customer)
        .where(Customer.is_deleted.is_(False))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

def update_customer(
    db: Session,
    customer_id: UUID,
    customer: CustomerUpdate
) -> Optional[Customer]:
    """
    Update an existing customer.

    Args:
        db: SQLAlchemy database session
        customer_id: UUID of the customer to update
        customer: CustomerUpdate schema containing updated data

    Returns:
        Updated Customer ORM object if successful, None otherwise
    """
    db_customer = db.get(Customer, customer_id)
    if not db_customer:
        return None

    update_data = customer.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: UUID) -> bool:
    """
    Delete a customer (soft delete if supported, otherwise hard delete).

    Args:
        db: SQLAlchemy database session
        customer_id: UUID of the customer to delete

    Returns:
        True if deletion was successful, False otherwise
    """
    db_customer = db.get(Customer, customer_id)
    if not db_customer:
        return False

    # Perform soft delete (set is_deleted flag)
    db_customer.is_deleted = True
    db.commit()
    db.refresh(db_customer)
    return True
