"""
Supplier API Router.

This module provides FastAPI endpoints for supplier management operations.
All endpoints delegate business logic to the Supplier service layer.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.services.supplier_service import (
    create_supplier,
    get_supplier,
    get_suppliers,
    update_supplier,
    delete_supplier,
)
from app.schemas.supplier import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
)

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)

@router.post(
    "/",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new supplier",
    description="Create a new supplier record in the system."
)
async def create_new_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db)
) -> SupplierResponse:
    """
    Create a new supplier.

    This endpoint creates a new supplier record with the provided data.
    It validates that no supplier with the same email already exists.

    Args:
        supplier: SupplierCreate schema containing supplier data
        db: Database session (injected via dependency)

    Returns:
        The created supplier response with ID and timestamps

    Raises:
        HTTPException: 400 if supplier with email already exists
    """
    try:
        created_supplier = create_supplier(db, supplier)
        return SupplierResponse.model_validate(created_supplier)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[SupplierResponse],
    status_code=status.HTTP_200_OK,
    summary="List all suppliers",
    description="Retrieve a paginated list of all suppliers."
)
async def list_suppliers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[SupplierResponse]:
    """
    Retrieve a paginated list of suppliers.

    This endpoint returns all suppliers with pagination support.
    Use skip and limit query parameters to control pagination.

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        db: Database session (injected via dependency)

    Returns:
        List of supplier responses
    """
    suppliers = get_suppliers(db, skip=skip, limit=limit)
    return [SupplierResponse.model_validate(supplier) for supplier in suppliers]

@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a supplier by ID",
    description="Retrieve a specific supplier by their unique identifier."
)
async def get_supplier_by_id(
    supplier_id: UUID,
    db: Session = Depends(get_db)
) -> SupplierResponse:
    """
    Retrieve a supplier by their ID.

    This endpoint returns a single supplier record matching the provided UUID.

    Args:
        supplier_id: UUID of the supplier to retrieve
        db: Database session (injected via dependency)

    Returns:
        The supplier response if found

    Raises:
        HTTPException: 404 if supplier not found
    """
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    return SupplierResponse.model_validate(supplier)

@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a supplier",
    description="Update an existing supplier record."
)
async def update_existing_supplier(
    supplier_id: UUID,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db)
) -> SupplierResponse:
    """
    Update an existing supplier.

    This endpoint updates a supplier record with the provided data.
    It validates email uniqueness and applies business rules.

    Args:
        supplier_id: UUID of the supplier to update
        supplier: SupplierUpdate schema containing updated data
        db: Database session (injected via dependency)

    Returns:
        The updated supplier response if successful

    Raises:
        HTTPException: 400 if email conflict occurs
        HTTPException: 404 if supplier not found
    """
    try:
        updated_supplier = update_supplier(db, supplier_id, supplier)
        if not updated_supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )
        return SupplierResponse.model_validate(updated_supplier)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a supplier",
    description="Soft-delete a supplier record from the system."
)
async def remove_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a supplier.

    This endpoint soft-deletes a supplier record from the system.
    The supplier is marked as deleted but remains in the database.

    Args:
        supplier_id: UUID of the supplier to delete
        db: Database session (injected via dependency)

    Returns:
        Empty response on success
    """
    success = delete_supplier(db, supplier_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )