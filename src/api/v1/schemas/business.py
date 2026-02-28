"""
Business-related API schemas
"""
from pydantic import BaseModel
from typing import Optional


class BusinessBase(BaseModel):
    business_name: str
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: str
    country: str
    industry: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BaseModel):
    business_name: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None


class Business(BusinessBase):
    id: int

    class Config:
        from_attributes = True
