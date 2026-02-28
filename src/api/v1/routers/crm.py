from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.database.connection import get_db
from src.services.enrichment.enrichment_service import enrichment_service
from src.services.scoring.scoring_service import scoring_service
from src.api.v1.schemas.lead import Lead, LeadCreate, LeadUpdate
from src.database.models import Lead as LeadModel


router = APIRouter(prefix="/crm", tags=["CRM"])


@router.get("/", response_model=List[Lead])
async def get_leads(
    skip: int = Query(0, ge=0, description="Number of leads to skip"),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Maximum number of leads to return"
    ),
    status: Optional[str] = Query(
        None,
        description="Filter by lead status"
    ),
    min_score: Optional[float] = Query(
        None,
        ge=0,
        le=100,
        description="Minimum lead score"
    ),
    db: Session = Depends(get_db)
):
    """
    Get list of leads with optional filters
    """
    try:
        leads = db.query(Lead).filter()

        if status:
            leads = leads.filter(Lead.status == status)
        if min_score is not None:
            leads = leads.filter(Lead.score >= min_score)

        leads = leads.offset(skip).limit(limit).all()
        return leads
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{lead_id}", response_model=Lead)
async def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific lead by ID
    """
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        return lead
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Lead)
async def create_lead(
    lead_data: LeadCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new lead
    """
    try:
        # Create new lead record
        from src.database.models import Lead as LeadModel
        lead = LeadModel(**lead_data.dict())
        db.add(lead)
        db.commit()
        db.refresh(lead)
        return lead
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{lead_id}", response_model=Lead)
async def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing lead
    """
    try:
        lead = db.query(LeadModel).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Update lead with new data
        for field, value in lead_data.dict(exclude_unset=True).items():
            setattr(lead, field, value)

        db.commit()
        db.refresh(lead)
        return lead
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a lead
    """
    try:
        lead = db.query(LeadModel).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        db.delete(lead)
        db.commit()
        return {"message": "Lead deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/enrich")
async def enrich_lead(
    lead_id: int,
    provider: str = Query("mock", description="Enrichment provider to use"),
    db: Session = Depends(get_db)
):
    """
    Enrich lead data with additional information
    """
    try:
        # Get the lead
        lead = db.query(LeadModel).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Enrich the lead using the enrichment service
        enriched_data = await enrichment_service.enrich_contact(
            email=lead.email if lead.email else "",
            phone=lead.phone if lead.phone else "",
            provider_type=provider
        )

        # Update the lead with enriched data
        for field, value in enriched_data.items():
            if hasattr(lead, field):
                setattr(lead, field, value)

        db.commit()
        db.refresh(lead)
        return lead
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{lead_id}/rescore")
async def rescore_lead(
    lead_id: int,
    criteria: List[str] = Query(
        ["relevance", "interest", "budget"],
        description="Scoring criteria"
    ),
    db: Session = Depends(get_db)
):
    """
    Rescore a lead based on specified criteria
    """
    try:
        # Get the lead
        lead = db.query(LeadModel).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Rescore the lead
        score_result = await scoring_service.score_lead(
            lead_id=lead_id,
            criteria=criteria
        )

        # Update the lead score
        lead.score = score_result.get("overall_score", lead.score)
        db.commit()
        db.refresh(lead)
        return lead
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
