from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.database.connection import get_db
from src.services.discovery.discovery_service import discovery_service
from src.services.enrichment.enrichment_service import enrichment_service
from src.services.ai import ai_service
from src.services.email.email_service import email_service


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/discover-businesses-background",
    response_model=Dict[str, Any]
)
async def discover_businesses_background(
    niche: str = Query(
        ...,
        description="Business niche/industry to search for"
    ),
    location: str = Query(
        ...,
        description="Location to search in"
    ),
    count: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of businesses to return"
    ),
    provider: str = Query(
        "mock",
        description="Discovery provider to use"
    ),
    db: Session = Depends(get_db)
):
    """
    Queue a background task to discover businesses
    """
    try:
        # This would queue the task in a real implementation
        # For now, we'll simulate the task execution
        task_result = await discovery_service.discover_businesses(
            niche=niche,
            location=location,
            count=count,
            provider_type=provider
        )
        return {
            "status": "completed",
            "result": task_result,
            "task_type": "business_discovery"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enrich-contacts-background", response_model=Dict[str, Any])
async def enrich_contacts_background(
    email: str = Query(..., description="Email to enrich"),
    provider: str = Query("mock", description="Enrichment provider to use"),
    db: Session = Depends(get_db)
):
    """
    Queue a background task to enrich contact information
    """
    try:
        # This would queue the task in a real implementation
        # For now, we'll simulate the task execution
        task_result = await enrichment_service.enrich_contact(
            email=email,
            provider_type=provider
        )
        return {
            "status": "completed",
            "result": task_result,
            "task_type": "contact_enrichment"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-outreach-background", response_model=Dict[str, Any])
async def generate_outreach_background(
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
    Queue a background task to generate outreach message
    """
    try:
        # This would queue the task in a real implementation
        # For now, we'll simulate the task execution
        task_result = await ai_service.generate_outreach_message(
            business_id=business_id,
            lead_id=lead_id,
            message_type=message_type,
            provider_type=provider
        )
        return {
            "status": "completed",
            "result": task_result,
            "task_type": "outreach_generation"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-email-background", response_model=Dict[str, Any])
async def send_email_background(
    outreach_id: int,
    provider: str = Query(
        "mock",
        description="Email provider to use for sending"
    ),
    db: Session = Depends(get_db)
):
    """
    Queue a background task to send email outreach
    """
    try:
        # This would queue the task in a real implementation
        # For now, we'll simulate the task execution
        task_result = await email_service.send_outreach_email(
            outreach_id=outreach_id,
            provider_type=provider
        )
        return {
            "status": "completed",
            "result": task_result,
            "task_type": "email_sending"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task-status/{task_id}", response_model=Dict[str, Any])
async def get_task_status(
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the status of a background task
    """
    try:
        # In a real implementation, this would check Celery task status
        # For now, we'll return a mock response
        return {
            "task_id": task_id,
            # Status could be pending, started, success, failure
            "status": "completed",
            "result": "Task completed successfully",
            "progress": 100
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
