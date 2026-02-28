"""
Lead scoring service module
"""
from typing import Dict
from src.core.logger import log
from src.core.constants import (
    LeadScoreCategory, PriorityLevel
)


class ScoringService:
    """Handles lead scoring and categorization"""

    def __init__(self):
        # Define scoring weights
        self.weights = {
            "opportunity": 0.3,
            "business_activity": 0.2,
            "digital_presence": 0.2,
            "budget_probability": 0.15,
            "engagement_potential": 0.15
        }

    async def score_lead(self, lead_data: Dict) -> Dict:
        """
        Score a lead based on various factors
        """
        try:
            # Calculate individual scores
            opportunity_score = self._calculate_opportunity_score(lead_data)
            business_activity_score = (
                self._calculate_business_activity_score(lead_data)
            )
            digital_presence_score = (
                self._calculate_digital_presence_score(lead_data)
            )
            budget_probability_score = (
                self._calculate_budget_probability_score(lead_data)
            )
            engagement_potential_score = (
                self._calculate_engagement_potential_score(lead_data)
            )
                
            # Calculate overall score
            opportunity_component = (
                opportunity_score * self.weights['opportunity']
            )
            business_activity_component = (
                business_activity_score * self.weights['business_activity']
            )
            digital_presence_component = (
                digital_presence_score * self.weights['digital_presence']
            )
            budget_probability_component = (
                budget_probability_score * self.weights['budget_probability']
            )
            engagement_potential_component = (
                engagement_potential_score *
                self.weights['engagement_potential']
            )
                
            overall_score = (
                opportunity_component +
                business_activity_component +
                digital_presence_component +
                budget_probability_component +
                engagement_potential_component
            )
                
            # Determine lead category based on score
            lead_category = self.categorize_lead(overall_score)
            priority_level = self._determine_priority_level(overall_score)
                
            result = {
                "opportunity_score": opportunity_score,
                "business_activity_score": business_activity_score,
                "digital_presence_score": digital_presence_score,
                "budget_probability_score": budget_probability_score,
                "engagement_potential_score": engagement_potential_score,
                "overall_score": round(overall_score, 2),
                "lead_category": lead_category,
                "priority_level": priority_level
            }
                
            log.info(
                f"Lead scored successfully. Overall score: {overall_score}, "
                f"Category: {lead_category}, Priority: {priority_level}"
            )
                
            return result
        except Exception as e:
            log.error(f"Error scoring lead: {e}")
            # Return default scores in case of error
            return {
                "opportunity_score": 0.0,
                "business_activity_score": 0.0,
                "digital_presence_score": 0.0,
                "budget_probability_score": 0.0,
                "engagement_potential_score": 0.0,
                "overall_score": 0.0,
                "lead_category": LeadScoreCategory.LOW_PRIORITY,
                "priority_level": PriorityLevel.LOW
            }

    def _calculate_opportunity_score(self, lead_data: Dict) -> float:
        """Calculate opportunity score based on industry, size, and needs"""
        score = 0.0

        # Industry match (if we know what industries are high-value)
        industry = lead_data.get('industry', '').lower()
        industries_high_value = [
            'technology', 'healthcare', 'finance', 'ecommerce'
        ]
        industries_medium_value = [
            'manufacturing', 'retail', 'education'
        ]

        if industry in industries_high_value:
            score += 25
        elif industry in industries_medium_value:
            score += 15
        else:
            score += 10

        # Company size (assuming larger companies have higher budgets)
        company_size = lead_data.get('company_size', '').lower()
        if 'large' in company_size or 'enterprise' in company_size:
            score += 30
        elif 'medium' in company_size:
            score += 20
        elif 'small' in company_size:
            score += 10
        else:
            score += 5

        # Service interest (if lead has shown interest in specific services)
        service_interest = lead_data.get('service_interest', '').lower()
        if service_interest:
            score += 25

        # Normalize to 0-100 scale, then convert to 0-10 scale
        return min(score / 10.0, 10.0)

    def _calculate_business_activity_score(self, lead_data: Dict) -> float:
        """Calculate business activity score based on recent activity"""
        score = 0.0

        # Check if business is active (exists in recent business databases)
        # For now, assume all businesses are active
        score += 40

        # Check for recent hiring (would require external data)
        # For simulation purposes
        score += 30

        # Check for recent investments or funding (would require external data)
        # For simulation purposes
        score += 30

        # Normalize to 0-100 scale, then convert to 0-10 scale
        return min(score / 10.0, 10.0)

    def _calculate_digital_presence_score(self, lead_data: Dict) -> float:
        """Calculate digital presence score based on online footprint"""
        score = 0.0

        # Presence of website
        if lead_data.get('website'):
            score += 30

        # Social media presence (LinkedIn, Twitter, etc.)
        if lead_data.get('linkedin_profile'):
            score += 25

        # Activity level (would require analysis of website/social presence)
        # For simulation, assume average activity
        score += 25

        # Quality of online presence (SEO, content quality, etc.)
        # For simulation, assume average quality
        score += 20

        # Normalize to 0-100 scale, then convert to 0-10 scale
        return min(score / 10.0, 10.0)

    def _calculate_budget_probability_score(self, lead_data: Dict) -> float:
        """Calculate budget probability based on company size and industry"""
        score = 0.0

        # Company size factor
        company_size = lead_data.get('company_size', '').lower()
        if 'large' in company_size or 'enterprise' in company_size:
            score += 40
        elif 'medium' in company_size:
            score += 25
        elif 'small' in company_size:
            score += 15
        else:
            score += 5

        # Industry factor (some industries typically have higher budgets)
        industry = lead_data.get('industry', '').lower()
        if industry in ['technology', 'finance', 'healthcare']:
            score += 30
        elif industry in ['ecommerce', 'marketing', 'consulting']:
            score += 20
        else:
            score += 10

        # Estimated budget (if provided)
        estimated_budget = lead_data.get('estimated_budget', '').lower()
        if 'high' in estimated_budget or '$' in estimated_budget:
            score += 30
        elif 'medium' in estimated_budget:
            score += 15

        # Normalize to 0-100 scale, then convert to 0-10 scale
        return min(score / 10.0, 10.0)

    def _calculate_engagement_potential_score(
        self, lead_data: Dict
    ) -> float:
        """
        Calculate engagement potential based on contact details and interest
        """
        score = 0.0

        # Quality of contact information
        if lead_data.get('contact_email') and lead_data.get('contact_name'):
            score += 30
        elif lead_data.get('email'):
            score += 20
        else:
            score += 5

        # Engagement indicators
        if lead_data.get('opportunity_notes'):
            score += 20

        # Interest level (based on service interest field)
        if lead_data.get('service_interest'):
            score += 30

        # Response history (would require historical data)
        # For simulation purposes
        score += 20

        # Normalize to 0-100 scale, then convert to 0-10 scale
        return min(score / 10.0, 10.0)

    def categorize_lead(self, score: float) -> str:
        """
        Categorize lead based on score
        """
        try:
            if score >= 8.0:
                return LeadScoreCategory.PRIORITY_CLIENT
            elif score >= 6.0:
                return LeadScoreCategory.GROWTH_CLIENT
            else:
                return LeadScoreCategory.LOW_PRIORITY
        except Exception as e:
            log.error(f"Error categorizing lead: {e}")
            return LeadScoreCategory.LOW_PRIORITY

    def calculate_engagement_score(self, lead_id: int) -> float:
        """
        Calculate engagement score based on interactions
        """
        # For now, return a simulated engagement score
        # In a real implementation, this would analyze email opens,
        # clicks, replies, etc.
        import random

        return round(random.uniform(0, 10), 2)

    def _determine_priority_level(self, overall_score: float) -> PriorityLevel:
        """Determine priority level based on overall score"""
        if overall_score >= 8.0:
            return PriorityLevel.HIGH
        elif overall_score >= 6.0:
            return PriorityLevel.MEDIUM
        else:
            return PriorityLevel.LOW
