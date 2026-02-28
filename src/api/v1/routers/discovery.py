"""
Business discovery API router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from src.database.connection import get_db
from src.api.v1.schemas.business import Business
from src.database.models import Lead as BusinessModel
from src.services.discovery.discovery_service import DiscoveryService

router = APIRouter()


@router.get("/discovery/search", response_model=List[Business])
async def search_businesses(
    niche: str = Query(
        ..., description="Business niche/industry to search for"
    ),
    location: str = Query(..., description="Location to search in"),
    count: int = Query(
        10, ge=1, le=100, description="Number of businesses to return"
    ),
    provider: str = Query("mock", description="Provider to use for discovery"),
    db: Session = Depends(get_db)
):
    """Search for businesses by niche and location"""
    try:
        service = DiscoveryService()
        businesses = await service.discover_businesses(
            niche=niche,
            location=location,
            count=count,
            provider_type=provider
        )

        # Save businesses to database
        saved_businesses = []
        for business_data in businesses:
            business = BusinessModel(**business_data)
            db.add(business)
            db.commit()
            db.refresh(business)
            saved_businesses.append(business)

        return saved_businesses
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error searching businesses: {str(e)}"
        )


@router.get("/discovery/competitors", response_model=List[Business])
async def search_competitors(
    business_name: str = Query(
        ..., description="Name of business to find competitors for"
    ),
    location: str = Query(..., description="Location to search in"),
    count: int = Query(
        10, ge=1, le=100, description="Number of competitors to return"
    ),
    provider: str = Query("mock", description="Provider to use for discovery"),
    db: Session = Depends(get_db)
):
    """Search for competitor businesses"""
    try:
        service = DiscoveryService()
        competitors = await service.search_competitors(
            business_name=business_name,
            location=location,
            count=count,
            provider_type=provider
        )

        # Save competitors to database
        saved_competitors = []
        for business_data in competitors:
            business = BusinessModel(**business_data)
            db.add(business)
            db.commit()
            db.refresh(business)
            saved_competitors.append(business)

        return saved_competitors
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error searching competitors: {str(e)}"
        )


@router.post("/discovery/enrich", response_model=Business)
async def enrich_business(
    business_id: int,
    provider: str = Query(
        "mock", description="Provider to use for enrichment"
    ),
    db: Session = Depends(get_db)
):
    """Enrich business information"""
    try:
        business = db.query(BusinessModel).filter(
            BusinessModel.id == business_id
        ).first()
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")

        # In a real implementation, this would call an enrichment service
        # For now, return the existing business
        return business
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error enriching business: {str(e)}"
        )
