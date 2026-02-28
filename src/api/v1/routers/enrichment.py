"""
Contact enrichment API router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any
from src.database.connection import get_db

from src.database.models import Lead as LeadModel
from src.services.enrichment.enrichment_service import EnrichmentService

router = APIRouter()


@router.post("/enrichment/contact", response_model=Dict[str, Any])
async def enrich_contact(
    business_id: int,
    provider: str = Query(
        "mock", description="Provider to use for enrichment"
    ),
    db: Session = Depends(get_db)
):
    """Enrich contact information for a business"""
    try:
        business = db.query(LeadModel).filter(
            LeadModel.id == business_id
        ).first()
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")

        service = EnrichmentService()
        enriched_data = await service.enrich_contact(
            business.__dict__, provider_type=provider
        )

        # Update the business record with enriched data
        for key, value in enriched_data.items():
            if hasattr(business, key):
                setattr(business, key, value)

        db.commit()
        db.refresh(business)

        return enriched_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error enriching contact: {str(e)}"
        )


@router.post("/enrichment/email", response_model=Dict[str, str])
async def find_email(
    business_name: str = Query(..., description="Name of the business"),
    domain: str = Query(..., description="Domain of the business"),
    provider: str = Query(
        "mock", description="Provider to use for email finding"
    ),
):
    """Find email for a business"""
    try:
        service = EnrichmentService()
        email = await service.find_email(
            business_name, domain, provider_type=provider
        )

        return {
            "email": email,
            "business_name": business_name,
            "domain": domain,
            "provider_used": provider
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error finding email: {str(e)}"
        )


@router.post("/enrichment/social-profiles", response_model=Dict[str, Any])
async def find_social_profiles(
    business_id: int,
    provider: str = Query(
        "mock", description="Provider to use for social profile finding"
    ),
    db: Session = Depends(get_db)
):
    """Find social media profiles for a business"""
    try:
        business = db.query(LeadModel).filter(
            LeadModel.id == business_id
        ).first()
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")

        service = EnrichmentService()
        profiles = await service.find_social_profiles(
            business.__dict__,
            provider_type=provider
        )

        return profiles
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error finding social profiles: {str(e)}"
        )
