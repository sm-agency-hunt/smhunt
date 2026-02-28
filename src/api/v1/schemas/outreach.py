"""
Outreach-related API schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OutreachBase(BaseModel):
    lead_id: int
    subject: str
    content: str
    status: Optional[str] = "pending"


class OutreachCreate(OutreachBase):
    pass


class OutreachUpdate(BaseModel):
    status: Optional[str] = None
    content: Optional[str] = None


class Outreach(OutreachBase):
    id: int
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OutreachMessageBase(BaseModel):
    lead_id: int
    message_type: str
    subject: Optional[str] = None
    content: str
    channel: str
    status: Optional[str] = "pending"


class OutreachMessageCreate(OutreachMessageBase):
    pass


class OutreachMessageUpdate(BaseModel):
    status: Optional[str] = None
    content: Optional[str] = None


class OutreachMessage(OutreachMessageBase):
    id: int
    tracking_id: Optional[str] = None
    sent_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    replied_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
