"""
Customer API Router.

This module provides FastAPI endpoints for customer management operations.
All endpoints delegate business logic to the Customer service layer.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.services.customer_service import (
    create_customer,
    get_customer,
    get_customers,
    update_customer,
    delete_customer,
)
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
    description="Create a new customer record in the system."
)
async def create_new_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
) -> CustomerResponse:
    """
    Create a new customer.

    This endpoint creates a new customer record with the provided data.
    It validates that no customer with the same email already exists.

    Args:
        customer: CustomerCreate schema containing customer data
        db: Database session (injected via dependency)

    Returns:
        The created customer response with ID and timestamps

    Raises:
        HTTPException: 400 if customer with email already exists
    """
    try:
        created_customer = create_customer(db, customer)
        return CustomerResponse.model_validate(created_customer)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[CustomerResponse],
    status_code=status.HTTP_200_OK,
    summary="List all customers",
    description="Retrieve a paginated list of all customers."
)
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[CustomerResponse]:
    """
    Retrieve a paginated list of customers.

    This endpoint returns all customers with pagination support.
    Use skip and limit query parameters to control pagination.

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        db: Database session (injected via dependency)

    Returns:
        List of customer responses
    """
    customers = get_customers(db, skip=skip, limit=limit)
    return [CustomerResponse.model_validate(customer) for customer in customers]

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a customer by ID",
    description="Retrieve a specific customer by their unique identifier."
)
async def get_customer_by_id(
    customer_id: UUID,
    db: Session = Depends(get_db)
) -> CustomerResponse:
    """
    Retrieve a customer by their ID.

    This endpoint returns a single customer record matching the provided UUID.

    Args:
        customer_id: UUID of the customer to retrieve
        db: Database session (injected via dependency)

    Returns:
        The customer response if found

    Raises:
        HTTPException: 404 if customer not found
    """
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return CustomerResponse.model_validate(customer)

@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a customer",
    description="Update an existing customer record."
)
async def update_existing_customer(
    customer_id: UUID,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
) -> CustomerResponse:
    """
    Update an existing customer.

    This endpoint updates a customer record with the provided data.
    It validates email uniqueness and applies business rules.

    Args:
        customer_id: UUID of the customer to update
        customer: CustomerUpdate schema containing updated data
        db: Database session (injected via dependency)

    Returns:
        The updated customer response if successful

    Raises:
        HTTPException: 400 if email conflict occurs
        HTTPException: 404 if customer not found
    """
    try:
        updated_customer = update_customer(db, customer_id, customer)
        if not updated_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        return CustomerResponse.model_validate(updated_customer)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a customer",
    description="Soft-delete a customer record from the system."
)
async def remove_customer(
    customer_id: UUID,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a customer.

    This endpoint soft-deletes a customer record from the system.
    The customer is marked as deleted but remains in the database.

    Args:
        customer_id: UUID of the customer to delete
        db: Database session (injected via dependency)

    Returns:
        Empty response on success
    """
    success = delete_customer(db, customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
