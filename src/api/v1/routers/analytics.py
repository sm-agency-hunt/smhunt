from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.database.models import (
    Lead, OutreachMessage, Meeting, DailyReport
)
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter()


@router.get("/analytics/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    """Get overall analytics summary"""
    total_leads = db.query(Lead).count()
    total_outreach = db.query(OutreachMessage).count()
    scheduled_meetings = db.query(Meeting).count()

    # Get recent activity (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_leads = (
        db.query(Lead)
        .filter(Lead.created_at >= seven_days_ago)
        .count()
    )
    recent_outreach = (
        db.query(OutreachMessage)
        .filter(OutreachMessage.created_at >= seven_days_ago)
        .count()
    )

    return {
        "total_leads": total_leads,
        "total_outreach_messages": total_outreach,
        "scheduled_meetings": scheduled_meetings,
        "recent_leads": recent_leads,
        "recent_outreach": recent_outreach,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/analytics/leads")
def get_lead_analytics(db: Session = Depends(get_db)):
    """Get detailed lead analytics"""
    # Count leads by status
    leads_by_status = defaultdict(int)
    all_leads = db.query(Lead).all()
    for lead in all_leads:
        status = (
            lead.lead_status.value
            if hasattr(lead.lead_status, 'value')
            else str(lead.lead_status)
        )
        leads_by_status[status] += 1

    # Count leads by industry
    leads_by_industry = defaultdict(int)
    for lead in all_leads:
        if lead.industry:
            leads_by_industry[lead.industry] += 1

    # Average scores
    avg_opportunity_score = (
        db.query(Lead.opportunity_score)
        .filter(Lead.opportunity_score.isnot(None))
        .scalar() or 0
    )
    avg_overall_score = (
        db.query(Lead.overall_score)
        .filter(Lead.overall_score.isnot(None))
        .scalar() or 0
    )

    return {
        "total_leads": len(all_leads),
        "leads_by_status": dict(leads_by_status),
        "leads_by_industry": dict(leads_by_industry),
        "average_opportunity_score": round(avg_opportunity_score, 2),
        "average_overall_score": round(avg_overall_score, 2)
    }


@router.get("/analytics/outreach")
def get_outreach_analytics(db: Session = Depends(get_db)):
    """Get outreach campaign analytics"""
    # Count outreach by status
    outreach_by_status = defaultdict(int)
    all_outreach = db.query(OutreachMessage).all()
    for outreach in all_outreach:
        status = (
            outreach.status.value
            if hasattr(outreach.status, 'value')
            else str(outreach.status)
        )
        outreach_by_status[status] += 1

    # Count sent, opened, replied
    sent_count = sum(1 for o in all_outreach if o.sent_at)
    opened_count = sum(1 for o in all_outreach if o.opened_at)
    replied_count = sum(1 for o in all_outreach if o.replied_at)

    # Calculate rates
    open_rate = (opened_count / sent_count * 100) if sent_count > 0 else 0
    reply_rate = (replied_count / sent_count * 100) if sent_count > 0 else 0

    return {
        "total_outreach": len(all_outreach),
        "sent_count": sent_count,
        "opened_count": opened_count,
        "replied_count": replied_count,
        "open_rate": round(open_rate, 2),
        "reply_rate": round(reply_rate, 2),
        "outreach_by_status": dict(outreach_by_status)
    }


@router.get("/reports/daily")
def get_daily_report(db: Session = Depends(get_db)):
    """Get daily report with key metrics"""
    today = datetime.utcnow().date()

    # Get or create today's report
    daily_report = db.query(DailyReport).filter(
        DailyReport.date.like(f"{today}%")
    ).first()

    if not daily_report:
        # Calculate metrics for today
        total_leads_today = db.query(Lead).filter(
            Lead.created_at.like(f"{today}%")
        ).count()

        total_outreach_today = db.query(OutreachMessage).filter(
            OutreachMessage.created_at.like(f"{today}%")
        ).count()

        # Create a basic report
        daily_report = {
            "date": str(today),
            "metrics": {
                "total_leads_added": total_leads_today,
                "total_outreach_sent": total_outreach_today,
                "meetings_scheduled": 0,  # Placeholder
                "replies_received": 0  # Placeholder
            }
        }
    else:
        daily_report = {
            "date": str(daily_report.date.date()),
            "metrics": {
                "total_leads_added": daily_report.total_leads_found,
                "total_outreach_sent": daily_report.emails_sent,
                "meetings_scheduled": daily_report.meetings_scheduled,
                "replies_received": daily_report.replies_received
            }
        }

    return daily_report
