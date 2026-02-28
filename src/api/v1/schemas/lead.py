"""
Lead-related API schemas
"""
from pydantic import BaseModel
from typing import Optional


class LeadBase(BaseModel):
    business_name: str
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: str
    country: str
    industry: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    lead_status: Optional[str] = "new"
    overall_score: Optional[float] = 0.0


class Lead(LeadBase):
    id: int
    lead_status: str = "new"
    overall_score: float = 0.0

    class Config:
        from_attributes = True
