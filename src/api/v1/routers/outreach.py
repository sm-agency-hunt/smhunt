from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from src.database.connection import get_db
from src.api.v1.schemas.outreach import (
    OutreachMessage,
    OutreachMessageCreate,
    OutreachMessageUpdate
)
from src.database.models import OutreachMessage as OutreachMessageModel

router = APIRouter()


@router.get("/outreach", response_model=List[OutreachMessage])
def get_outreach_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    lead_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of outreach messages with pagination and optional filtering"""
    query = db.query(OutreachMessageModel)
    if lead_id:
        query = query.filter(OutreachMessageModel.lead_id == lead_id)

    outreach_messages = (
        query.offset(skip)
        .limit(limit)
        .all()
    )
    return outreach_messages


@router.get("/outreach/{outreach_id}", response_model=OutreachMessage)
def get_outreach_message(
    outreach_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific outreach message by ID"""
    outreach_message = (
        db.query(OutreachMessageModel)
        .filter(OutreachMessageModel.id == outreach_id)
        .first()
    )
    if not outreach_message:
        raise HTTPException(
            status_code=404,
            detail="Outreach message not found"
        )
    return outreach_message


@router.post("/outreach", response_model=OutreachMessage)
def create_outreach_message(
    outreach_message: OutreachMessageCreate,
    db: Session = Depends(get_db)
):
    """Create a new outreach message"""
    db_outreach_message = OutreachMessageModel(
        **outreach_message.model_dump()
    )
    db.add(db_outreach_message)
    db.commit()
    db.refresh(db_outreach_message)
    return db_outreach_message


@router.put("/outreach/{outreach_id}", response_model=OutreachMessage)
def update_outreach_message(
    outreach_id: int,
    outreach_message: OutreachMessageUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing outreach message"""
    db_outreach_message = (
        db.query(OutreachMessageModel)
        .filter(OutreachMessageModel.id == outreach_id)
        .first()
    )
    if not db_outreach_message:
        raise HTTPException(
            status_code=404,
            detail="Outreach message not found"
        )

    update_data = outreach_message.model_dump(
        exclude_unset=True
    )
    for field, value in update_data.items():
        setattr(db_outreach_message, field, value)

    db.commit()
    db.refresh(db_outreach_message)
    return db_outreach_message


@router.delete("/outreach/{outreach_id}")
def delete_outreach_message(
    outreach_id: int,
    db: Session = Depends(get_db)
):
    """Delete an outreach message"""
    outreach_message = (
        db.query(OutreachMessageModel)
        .filter(OutreachMessageModel.id == outreach_id)
        .first()
    )
    if not outreach_message:
        raise HTTPException(
            status_code=404,
            detail="Outreach message not found"
        )

    db.delete(outreach_message)
    db.commit()
    return {"message": "Outreach message deleted successfully"}
