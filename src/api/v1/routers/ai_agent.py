"""
AI Lead Agent API router - Endpoints for automated lead generation
and client communication
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from src.database.connection import get_db
from src.services.ai.ai_lead_agent import AILeadAgent

router = APIRouter(prefix="/ai-agent", tags=["AI Agent"])


@router.post("/generate-leads", response_model=List[Dict[str, Any]])
async def generate_leads_endpoint(
    industry: str = Query(..., description="Target industry/niche"),
    location: str = Query(..., description="Target location"),
    count: int = Query(10, ge=1, le=100, description="Number of leads"),
    provider: str = Query("mock", description="Discovery provider"),
    db: Session = Depends(get_db)
):
    """
    Generate qualified leads using AI agent
    """
    try:
        agent = AILeadAgent()
        
        leads = await agent.generate_leads(
            industry=industry,
            location=location,
            count=count,
            provider_type=provider
        )
        
        return {
            "success": True,
            "leads": leads,
            "count": len(leads),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating leads: {str(e)}"
        )


@router.post("/create-outreach", response_model=Dict[str, Any])
async def create_outreach_message(
    lead_data: Dict[str, Any] = Body(...),
    campaign_settings: Dict[str, Any] = Body(...),
    provider: str = Query("mock", description="AI provider"),
    db: Session = Depends(get_db)
):
    """
    Create personalized outreach message for a lead
    """
    try:
        agent = AILeadAgent()
        
        message = await agent.create_personalized_outreach(
            lead=lead_data,
            campaign_settings=campaign_settings,
            provider_type=provider
        )
        
        return {
            "success": True,
            "message": message,
            "created_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating outreach: {str(e)}"
        )


@router.post("/send-campaign", response_model=Dict[str, Any])
async def send_outreach_campaign(
    messages: List[Dict[str, str]] = Body(...),
    auto_followup: bool = Query(True, description="Enable auto follow-up"),
    db: Session = Depends(get_db)
):
    """
    Send outreach campaign to multiple leads
    """
    try:
        agent = AILeadAgent()
        
        result = await agent.send_outreach_campaign(
            messages=messages,
            auto_followup=auto_followup
        )
        
        return {
            "success": True,
            "campaign_result": result,
            "sent_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending campaign: {str(e)}"
        )


@router.post("/handle-response", response_model=Dict[str, Any])
async def handle_lead_response(
    response_text: str = Body(..., embed=True),
    conversation_history: List[Dict[str, str]] = Body(default=[]),
    db: Session = Depends(get_db)
):
    """
    Handle lead response and generate appropriate reply
    """
    try:
        agent = AILeadAgent()
        
        result = await agent.handle_response(
            response_text=response_text,
            conversation_history=conversation_history
        )
        
        return {
            "success": True,
            "response_analysis": result,
            "processed_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error handling response: {str(e)}"
        )


@router.post("/send-followup", response_model=Dict[str, Any])
async def send_followup_message(
    original_message: Dict[str, str] = Body(...),
    days_since_contact: int = Query(..., ge=0),
    provider: str = Query("mock", description="AI provider"),
    db: Session = Depends(get_db)
):
    """
    Generate and send follow-up message
    """
    try:
        agent = AILeadAgent()
        
        followup = await agent.send_followup(
            original_message=original_message,
            days_since_contact=days_since_contact,
            provider_type=provider
        )
        
        return {
            "success": True,
            "followup_message": followup,
            "created_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending follow-up: {str(e)}"
        )


@router.get("/campaign-status/{campaign_id}", response_model=Dict[str, Any])
async def get_campaign_status(
    campaign_id: str,
    db: Session = Depends(get_db)
):
    """
    Get status of an outreach campaign
    """
    try:
        # This would query the database for campaign status
        # For now, returning mock data
        return {
            "success": True,
            "campaign_id": campaign_id,
            "status": "active",
            "total_sent": 10,
            "responses_received": 3,
            "meetings_booked": 1,
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting campaign status: {str(e)}"
        )
