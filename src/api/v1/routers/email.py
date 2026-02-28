from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from src.database.connection import get_db
from src.services.email.email_service import email_service


router = APIRouter(prefix="/email", tags=["Email"])


@router.post("/send-outreach", response_model=dict)
async def send_outreach_email(
    outreach_id: int,
    provider: str = Query(
        "mock",
        description="Email provider to use for sending"
    ),
    db: Session = Depends(get_db)
):
    """
    Send outreach email to a lead
    """
    try:
        result = await email_service.send_outreach_email(
            outreach_id=outreach_id,
            provider_type=provider
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-bulk-outreach", response_model=dict)
async def send_bulk_outreach_emails(
    outreach_ids: List[int],
    provider: str = Query(
        "mock",
        description="Email provider to use for sending"
    ),
    db: Session = Depends(get_db)
):
    """
    Send bulk outreach emails
    """
    try:
        result = await email_service.send_bulk_outreach_emails(
            outreach_ids=outreach_ids,
            provider_type=provider
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check-delivery-status", response_model=dict)
async def check_delivery_status(
    email_id: str,
    provider: str = Query(
        "mock",
        description="Email provider to check status from"
    ),
    db: Session = Depends(get_db)
):
    """
    Check delivery status of sent email
    """
    try:
        status = await email_service.check_delivery_status(
            email_id=email_id,
            provider_type=provider
        )
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-inbox-analytics", response_model=dict)
async def get_inbox_analytics(
    provider: str = Query(
        "mock",
        description="Email provider to get analytics from"
    ),
    db: Session = Depends(get_db)
):
    """
    Get email inbox analytics
    """
    try:
        analytics = await email_service.get_inbox_analytics(
            provider_type=provider
        )
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
