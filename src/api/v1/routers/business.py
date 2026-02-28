from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from src.database.connection import get_db
from src.api.v1.schemas.business import (
    Business,
    BusinessCreate,
    BusinessUpdate
)
from src.database.models import Lead as BusinessModel

router = APIRouter()


@router.get("/businesses", response_model=List[Business])
def get_businesses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    industry: str = Query(None),
    location: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of businesses with filtering and pagination"""
    query = db.query(BusinessModel)

    if industry:
        query = query.filter(BusinessModel.industry == industry)
    if location:
        query = query.filter(BusinessModel.city == location)

    businesses = query.offset(skip).limit(limit).all()
    return businesses


@router.get("/businesses/{business_id}", response_model=Business)
def get_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific business by ID"""
    business = (
        db.query(BusinessModel)
        .filter(BusinessModel.id == business_id)
        .first()
    )
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.post("/businesses", response_model=Business)
def create_business(
    business: BusinessCreate,
    db: Session = Depends(get_db)
):
    """Create a new business"""
    db_business = BusinessModel(**business.model_dump())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


@router.put("/businesses/{business_id}", response_model=Business)
def update_business(
    business_id: int,
    business: BusinessUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing business"""
    db_business = (
        db.query(BusinessModel)
        .filter(BusinessModel.id == business_id)
        .first()
    )
    if not db_business:
        raise HTTPException(status_code=404, detail="Business not found")

    update_data = business.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_business, field, value)

    db.commit()
    db.refresh(db_business)
    return db_business


@router.delete("/businesses/{business_id}")
def delete_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Delete a business"""
    business = (
        db.query(BusinessModel)
        .filter(BusinessModel.id == business_id)
        .first()
    )
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    db.delete(business)
    db.commit()
    return {"message": "Business deleted successfully"}
