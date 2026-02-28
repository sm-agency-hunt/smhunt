from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from src.database.connection import get_db
from src.services.scheduling.scheduling_service import scheduling_service


router = APIRouter(prefix="/scheduling", tags=["Scheduling"])

@router.post("/schedule-meeting", response_model=dict)
async def schedule_meeting(
    lead_id: int,
    meeting_datetime: datetime,
    duration: int = Query(
        30, 
        description="Meeting duration in minutes"
    ),
    provider: str = Query(
        "mock", 
        description="Calendar provider to use for scheduling"
    ),
    db: Session = Depends(get_db)
):
    """
    Schedule a meeting with a lead
    """
    try:
        result = await scheduling_service.schedule_meeting(
            lead_id=lead_id,
            meeting_datetime=meeting_datetime,
            duration=duration,
            provider_type=provider
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedule-followup", response_model=dict)
async def schedule_followup(
    outreach_id: int,
    followup_datetime: datetime,
    provider: str = Query(
        "mock", 
        description="Calendar provider to use for scheduling"
    ),
    db: Session = Depends(get_db)
):
    """
    Schedule a follow-up with a lead based on outreach activity
    """
    try:
        result = await scheduling_service.schedule_followup(
            outreach_id=outreach_id,
            followup_datetime=followup_datetime,
            provider_type=provider
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-available-times", response_model=List[datetime])
async def get_available_times(
    lead_id: int,
    start_date: datetime,
    end_date: datetime,
    provider: str = Query(
        "mock", 
        description="Calendar provider to check availability from"
    ),
    db: Session = Depends(get_db)
):
    """
    Get available meeting times for a lead
    """
    try:
        available_times = await scheduling_service.get_available_times(
            lead_id=lead_id,
            start_date=start_date,
            end_date=end_date,
            provider_type=provider
        )
        return available_times
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/cancel-meeting", response_model=dict)
async def cancel_meeting(
    meeting_id: str,
    provider: str = Query(
        "mock", 
        description="Calendar provider to use for cancellation"
    ),
    db: Session = Depends(get_db)
):
    """
    Cancel a scheduled meeting
    """
    try:
        result = await scheduling_service.cancel_meeting(
            meeting_id=meeting_id,
            provider_type=provider
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))