from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.database.connection import get_db
from src.services.analysis.analysis_service import analysis_service


router = APIRouter(
    prefix="/website-intelligence", 
    tags=["Website Intelligence"]
)


@

@router.get("/analyze", response_model=Dict[str, Any])
async def analyze_website(
    url: str = Query(..., description="URL of the website to analyze"),
    analysis_type: str = Query(
        "full", 
        description="Type of analysis to perform: full, tech_stack, contact_info, social_links"
    ),
    provider: str = Query(
        "mock", 
        description="Analysis provider to use"
    ),
    db: Session = Depends(get_db)
):
    """
    Analyze a website for technology stack, contact information, and other intelligence
    """
    try:
        analysis_result = await analysis_service.analyze_website(
            url=url,
            analysis_type=analysis_type,
            provider_type=provider
        )
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/extract-contact-info", response_model=Dict[str, Any])
async def extract_contact_info(
    url: str = Query(..., description="URL of the website to extract contact info from"),
    provider: str = Query(
        "mock", 
        description="Extraction provider to use"
    ),
    db: Session = Depends(get_db)
):
    """
    Extract contact information from a website
    """
    try:
        contact_info = await analysis_service.extract_contact_info(
            url=url,
            provider_type=provider
        )
        return contact_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-tech-stack", response_model=Dict[str, Any])
async def get_tech_stack(
    url: str = Query(..., description="URL of the website to analyze technology stack"),
    provider: str = Query(
        "mock", 
        description="Technology detection provider to use"
    ),
    db: Session = Depends(get_db)
):
    """
    Get the technology stack of a website
    """
    try:
        tech_stack = await analysis_service.get_tech_stack(
            url=url,
            provider_type=provider
        )
        return tech_stack
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/find-social-links", response_model=Dict[str, Any])
async def find_social_links(
    url: str = Query(..., description="URL of the website to find social links from"),
    provider: str = Query(
        "mock", 
        description="Link extraction provider to use"
    ),
    db: Session = Depends(get_db)
):
    """
    Find social media links from a website
    """
    try:
        social_links = await analysis_service.find_social_links(
            url=url,
            provider_type=provider
        )
        return social_links
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))