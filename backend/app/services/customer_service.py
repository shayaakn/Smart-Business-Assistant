"""
Customer Service Layer.

This module provides business logic for Customer operations.
It acts as an intermediary between API routes and CRUD operations,
enforcing business rules and validation without direct database access.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.crud.customer import (
    create_customer as crud_create_customer,
    get_customer as crud_get_customer,
    get_customers as crud_get_customers,
    update_customer as crud_update_customer,
    delete_customer as crud_delete_customer,
    get_customer_by_email as crud_get_customer_by_email
)

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """
    Create a new customer with business validation.

    Args:
        db: SQLAlchemy database session
        customer: CustomerCreate schema containing customer data

    Returns:
        The created Customer ORM object

    Raises:
        ValueError: If a customer with the same email already exists
    """
    # Check for duplicate email
    if customer.email:
        existing_customer = crud_get_customer_by_email(db, customer.email)
        if existing_customer:
            raise ValueError(f"A customer with email '{customer.email}' already exists")

    # Create the customer using CRUD function
    return crud_create_customer(db, customer)

def get_customer(db: Session, customer_id: UUID) -> Optional[Customer]:
    """
    Retrieve a customer by their ID.

    Args:
        db: SQLAlchemy database session
        customer_id: UUID of the customer to retrieve

    Returns:
        Customer ORM object if found, None otherwise
    """
    return crud_get_customer(db, customer_id)

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> list[Customer]:
    """
    Retrieve a list of customers with pagination support.

    Args:
        db: SQLAlchemy database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)

    Returns:
        List of Customer ORM objects
    """
    return crud_get_customers(db, skip, limit)

def update_customer(db: Session, customer_id: UUID, customer: CustomerUpdate) -> Optional[Customer]:
    """
    Update an existing customer with business validation.

    Args:
        db: SQLAlchemy database session
        customer_id: UUID of the customer to update
        customer: CustomerUpdate schema containing updated data

    Returns:
        Updated Customer ORM object if successful, None otherwise

    Raises:
        ValueError: If attempting to change email to one that already belongs to another customer
    """
    # Get the existing customer
    existing_customer = crud_get_customer(db, customer_id)
    if not existing_customer:
        return None

    # Check for email change validation
    if customer.email and customer.email != existing_customer.email:
        existing_email_customer = crud_get_customer_by_email(db, customer.email)
        if existing_email_customer and existing_email_customer.id != customer_id:
            raise ValueError(f"A customer with email '{customer.email}' already exists")

    # Update the customer using CRUD function
    return crud_update_customer(db, customer_id, customer)

def delete_customer(db: Session, customer_id: UUID) -> bool:
    """
    Delete a customer.

    Args:
        db: SQLAlchemy database session
        customer_id: UUID of the customer to delete

    Returns:
        True if deletion was successful, False otherwise
    """
    return crud_delete_customer(db, customer_id)