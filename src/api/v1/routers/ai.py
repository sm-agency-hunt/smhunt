from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from src.database.connection import get_db
from src.services.ai import ai_service
from src.api.v1.schemas.outreach import OutreachMessage


router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate-outreach", response_model=OutreachMessage)
async def generate_outreach_message(
    business_id: int,
    lead_id: int,
    message_type: str = Query(
        "cold_email",
        description="Type of outreach message to generate"
    ),
    provider: str = Query(
        "mock",
        description="AI provider to use for generation"
    ),
    db: Session = Depends(get_db)
):
    """
    Generate personalized outreach message for a business and lead
    """
    try:
        message = await ai_service.generate_outreach_message(
            business_id=business_id,
            lead_id=lead_id,
            message_type=message_type,
            provider_type=provider
        )
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-followup", response_model=OutreachMessage)
async def generate_followup_message(
    outreach_id: int,
    provider: str = Query(
        "mock", description="AI provider to use for generation"
    ),
    db: Session = Depends(get_db)
):
    """
    Generate follow-up message based on previous outreach
    """
    try:
        message = await ai_service.generate_followup_message(
            outreach_id=outreach_id,
            provider_type=provider
        )
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-business-intelligence", response_model=dict)
async def analyze_business_intelligence(
    business_id: int,
    analysis_type: str = Query(
        "competitor_analysis",
        description="Type of analysis to perform"
    ),
    provider: str = Query(
        "mock",
        description="AI provider to use for analysis"
    ),
    db: Session = Depends(get_db)
):
    """
    Analyze business intelligence for a given business
    """
    try:
        analysis_result = await ai_service.analyze_business_intelligence(
            business_id=business_id,
            analysis_type=analysis_type,
            provider_type=provider
        )
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/score-lead", response_model=dict)
async def score_lead_intelligence(
    lead_id: int,
    criteria: List[str] = Query(
        ["relevance", "interest", "budget"],
        description="Scoring criteria"
    ),
    provider: str = Query(
        "mock",
        description="AI provider to use for scoring"
    ),
    db: Session = Depends(get_db)
):
    """
    Score a lead using AI intelligence
    """
    try:
        score_result = await ai_service.score_lead_intelligence(
            lead_id=lead_id,
            criteria=criteria,
            provider_type=provider
        )
        return score_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
