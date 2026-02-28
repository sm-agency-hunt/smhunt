from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    Float, Enum, ForeignKey, JSON, Index
)
from sqlalchemy.orm import relationship

# Import Base from the connection module to ensure shared base class
from src.database.connection import Base
from datetime import datetime
from src.core.constants import (
    LeadStatus, OutreachStatus, MeetingStatus, 
    LeadScoreCategory, DataSource
)


class User(Base):
    """User model for system authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    leads = relationship("Lead", back_populates="assigned_user")
    
    __table_args__ = (
        Index('ix_users_email', 'email'),
    )


class Lead(Base):
    """Main lead model"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False, index=True)
    website = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    address = Column(Text)
    city = Column(String, index=True)
    country = Column(String, index=True)
    industry = Column(String, index=True)
    company_size = Column(String)
    
    # Contact Information
    contact_name = Column(String, index=True)
    contact_title = Column(String)
    contact_email = Column(String, index=True)
    contact_phone = Column(String)
    linkedin_profile = Column(String)
    
    # Lead Scoring
    opportunity_score = Column(Float, default=0.0)
    business_activity_score = Column(Float, default=0.0)
    digital_presence_score = Column(Float, default=0.0)
    budget_probability_score = Column(Float, default=0.0)
    engagement_potential_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    lead_category = Column(Enum(LeadScoreCategory), index=True)
    
    # Status Tracking
    lead_status = Column(Enum(LeadStatus), default=LeadStatus.NEW, index=True)
    outreach_status = Column(Enum(OutreachStatus), default=OutreachStatus.PENDING)
    meeting_status = Column(Enum(MeetingStatus), default=MeetingStatus.SCHEDULED)
    priority_level = Column(String, default="medium")
    
    # Opportunity Information
    opportunity_notes = Column(Text)
    estimated_budget = Column(String)
    service_interest = Column(String)
    
    # Data Source Tracking
    source = Column(Enum(DataSource), index=True)
    source_id = Column(String)  # ID from the source platform
    
    # Website Analysis
    website_analysis = Column(JSON)
    identified_issues = Column(JSON)
    opportunity_summary = Column(Text)
    
    # Timestamps
    date_added = Column(DateTime, default=datetime.utcnow, index=True)
    last_contacted = Column(DateTime)
    next_follow_up = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    assigned_user = relationship("User", back_populates="leads")
    outreach_messages = relationship("OutreachMessage", back_populates="lead")
    meetings = relationship("Meeting", back_populates="lead")
    
    __table_args__ = (
        Index('ix_leads_business_name', 'business_name'),
        Index('ix_leads_city', 'city'),
        Index('ix_leads_country', 'country'),
        Index('ix_leads_industry', 'industry'),
        Index('ix_leads_contact_email', 'contact_email'),
        Index('ix_leads_date_added', 'date_added'),
        Index('ix_leads_lead_status', 'lead_status'),
        Index('ix_leads_lead_category', 'lead_category'),
    )


class OutreachMessage(Base):
    """Outreach message tracking"""
    __tablename__ = "outreach_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    message_type = Column(String, nullable=False)  # email, linkedin, etc.
    subject = Column(String)
    content = Column(Text, nullable=False)
    channel = Column(String, nullable=False)
    follow_up_sequence = Column(Integer, default=1)
    
    # Status Tracking
    status = Column(Enum(OutreachStatus), default=OutreachStatus.PENDING, index=True)
    sent_at = Column(DateTime)
    opened_at = Column(DateTime)
    replied_at = Column(DateTime)
    bounce_reason = Column(String)
    
    # Tracking Data
    tracking_id = Column(String, unique=True)
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    
    # AI Generated Data
    prompt_used = Column(Text)
    ai_model = Column(String)
    temperature = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="outreach_messages")
    
    __table_args__ = (
        Index('ix_outreach_messages_lead_id', 'lead_id'),
        Index('ix_outreach_messages_status', 'status'),
        Index('ix_outreach_messages_tracking_id', 'tracking_id'),
    )


class Meeting(Base):
    """Meeting scheduling and tracking"""
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # Scheduling
    proposed_date = Column(DateTime, nullable=False)
    confirmed_date = Column(DateTime)
    duration_minutes = Column(Integer, default=30)
    timezone = Column(String)
    
    # Meeting Details
    meeting_type = Column(String)  # initial, follow-up, proposal
    meeting_link = Column(String)
    location = Column(String)
    
    # Status
    status = Column(Enum(MeetingStatus), default=MeetingStatus.SCHEDULED, index=True)
    cancellation_reason = Column(Text)
    
    # Confirmation
    confirmed_by_client = Column(Boolean, default=False)
    confirmation_sent_at = Column(DateTime)
    reminder_sent = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="meetings")
    
    __table_args__ = (
        Index('ix_meetings_lead_id', 'lead_id'),
        Index('ix_meetings_status', 'status'),
        Index('ix_meetings_proposed_date', 'proposed_date'),
    )


class WebsiteAudit(Base):
    """Website analysis and audit results"""
    __tablename__ = "website_audits"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    website_url = Column(String, nullable=False)
    
    # Analysis Results
    performance_score = Column(Float)
    mobile_score = Column(Float)
    seo_score = Column(Float)
    security_score = Column(Float)
    
    # Detailed Findings
    issues_found = Column(JSON)
    recommendations = Column(JSON)
    competitors_analysis = Column(JSON)
    
    # Audit Summary
    executive_summary = Column(Text)
    audit_pdf_url = Column(String)
    
    # Technical Data
    analysis_timestamp = Column(DateTime, default=datetime.utcnow)
    analysis_tool = Column(String)
    screenshots = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('ix_website_audits_lead_id', 'lead_id'),
        Index('ix_website_audits_website_url', 'website_url'),
    )


class SystemLog(Base):
    """System activity and error logging"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    level = Column(String, nullable=False)
    module = Column(String, nullable=False)
    function = Column(String)
    message = Column(Text, nullable=False)
    trace = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    __table_args__ = (
        Index('ix_system_logs_timestamp', 'timestamp'),
        Index('ix_system_logs_level', 'level'),
        Index('ix_system_logs_module', 'module'),
    )


class DailyReport(Base):
    """Daily performance and summary reports"""
    __tablename__ = "daily_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Metrics
    total_leads_found = Column(Integer, default=0)
    leads_analyzed = Column(Integer, default=0)
    high_priority_leads = Column(Integer, default=0)
    
    # Outreach Metrics
    emails_sent = Column(Integer, default=0)
    emails_opened = Column(Integer, default=0)
    replies_received = Column(Integer, default=0)
    
    # Meeting Metrics
    meetings_scheduled = Column(Integer, default=0)
    meetings_completed = Column(Integer, default=0)
    meetings_converted = Column(Integer, default=0)
    
    # Financial Metrics
    estimated_revenue = Column(Float, default=0.0)
    cost_per_lead = Column(Float, default=0.0)
    roi_percentage = Column(Float, default=0.0)
    
    # Report Data
    top_performing_niches = Column(JSON)
    conversion_rates = Column(JSON)
    system_performance = Column(JSON)
    recommendations = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('ix_daily_reports_date', 'date'),
    )