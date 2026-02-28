"""
Enrichment provider interfaces for contact and business data enrichment
"""
from abc import abstractmethod
from typing import Dict, Any, Optional
from .base_provider import BaseProvider, MockProvider


class EnrichmentProvider(BaseProvider):
    """Interface for data enrichment providers"""
    
    @abstractmethod
    async def enrich_contact(
        self, 
        contact_data: Dict[str, Any], 
        **kwargs
    ) -> Dict[str, Any]:
        """Enrich contact information"""
        pass
    
    @abstractmethod
    async def find_email(
        self, 
        person_name: str, 
        company_domain: str,
        **kwargs
    ) -> Optional[str]:
        """Find email address for a person at a company"""
        pass
    
    @abstractmethod
    async def enrich_company(
        self, 
        company_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Enrich company information"""
        pass


class HunterProvider(EnrichmentProvider):
    """Hunter.io provider for email finding and contact enrichment"""
    
    async def enrich_contact(
        self, 
        contact_data: Dict[str, Any], 
        **kwargs
    ) -> Dict[str, Any]:
        """Enrich contact using Hunter.io API"""
        if not self.api_key:
            raise ValueError("Hunter.io API key required")
        
        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "domain": contact_data.get("company_domain", ""),
            "first_name": contact_data.get("first_name", ""),
            "last_name": contact_data.get("last_name", "")
        }
        
        response = await self._make_request("GET", url, params=params)
        
        enriched_data = contact_data.copy()
        if "data" in response and "email" in response["data"]:
            enriched_data["email"] = response["data"]["email"]
        
        return enriched_data
    
    async def find_email(
        self, 
        person_name: str, 
        company_domain: str,
        **kwargs
    ) -> Optional[str]:
        """Find email using Hunter.io API"""
        if not self.api_key:
            raise ValueError("Hunter.io API key required")
        
        # Split person_name into first and last name
        name_parts = person_name.split(" ")
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "domain": company_domain,
            "first_name": first_name,
            "last_name": last_name
        }
        
        try:
            response = await self._make_request("GET", url, params=params)
            if "data" in response and "email" in response["data"]:
                return response["data"]["email"]
        except Exception:
            pass
        
        return None
    
    async def enrich_company(
        self, 
        company_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Enrich company using Hunter.io API"""
        if not self.api_key:
            raise ValueError("Hunter.io API key required")
        
        url = "https://api.hunter.io/v2/domain-search"
        params = {"domain": company_data.get("domain", "")}
        
        response = await self._make_request("GET", url, params=params)
        
        enriched_data = company_data.copy()
        if "data" in response:
            enriched_data.update(response["data"])
        
        return enriched_data


class ClearbitProvider(EnrichmentProvider):
    """Clearbit provider for contact and company enrichment"""
    
    async def enrich_contact(
        self, 
        contact_data: Dict[str, Any], 
        **kwargs
    ) -> Dict[str, Any]:
        """Enrich contact using Clearbit API"""
        if not self.api_key:
            raise ValueError("Clearbit API key required")
        
        email = contact_data.get("email", "")
        if not email:
            # Try to find email first
            email = await self.find_email(
                contact_data.get("name", ""), 
                contact_data.get("company_domain", "")
            )
        
        url = f"https://person.clearbit.com/v2/combined/find?email={email}"
        
        response = await self._make_request("GET", url)
        
        enriched_data = contact_data.copy()
        enriched_data.update(response)
        
        return enriched_data
    
    async def find_email(
        self, 
        person_name: str, 
        company_domain: str,
        **kwargs
    ) -> Optional[str]:
        """Find email using Clearbit API"""
        # Clearbit doesn't have direct email finding, return None
        return None
    
    async def enrich_company(
        self, 
        company_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Enrich company using Clearbit API"""
        if not self.api_key:
            raise ValueError("Clearbit API key required")
        
        domain = company_data.get("domain", "")
        if not domain:
            return company_data
        
        url = f"https://company.clearbit.com/v2/companies/find?domain={domain}"
        
        response = await self._make_request("GET", url)
        
        enriched_data = company_data.copy()
        enriched_data.update(response)
        
        return enriched_data


class LinkedInProvider(EnrichmentProvider):
    """LinkedIn provider for professional profile enrichment"""
    
    async def enrich_contact(
        self, 
        contact_data: Dict[str, Any], 
        **kwargs
    ) -> Dict[str, Any]:
        """Enrich contact using LinkedIn data"""
        # This would require LinkedIn API access in production
        # For now, return mock data
        enriched_data = contact_data.copy()
        enriched_data.update({
            "linkedin_profile": (
                f"https://linkedin.com/in/{contact_data.get('name', 'mock').lower().replace(' ', '')}"
            ),
            "linkedin_connections": 500,
            "linkedin_headline": contact_data.get("title", "Professional"),
            "linkedin_location": contact_data.get("location", "United States")
        })
        return enriched_data
    
    async def find_email(
        self, 
        person_name: str, 
        company_domain: str,
        **kwargs
    ) -> Optional[str]:
        """Find email using LinkedIn data"""
        # This would require LinkedIn API access in production
        # For now, return None
        return None
    
    async def enrich_company(
        self, 
        company_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Enrich company using LinkedIn data"""
        # This would require LinkedIn API access in production
        # For now, return mock data
        enriched_data = company_data.copy()
        enriched_data.update({
            "linkedin_company_profile": (
                f"https://linkedin.com/company/{company_data.get('name', 'mock').lower().replace(' ', '')}"
            ),
            "linkedin_employee_count": company_data.get("employee_count", 50),
            "linkedin_industry": company_data.get("industry", "Technology")
        })
        return enriched_data


class MockEnrichmentProvider(MockProvider, EnrichmentProvider):
    """Mock enrichment provider for testing and development"""
    
    async def enrich_contact(
        self, 
        contact_data: Dict[str, Any], 
        **kwargs
    ) -> Dict[str, Any]:
        """Mock contact enrichment"""
        enriched_data = contact_data.copy()
        enriched_data.update({
            "email": (
                contact_data.get("email") 
                or f"mock_{contact_data.get('name', 'user')}@mockcompany.com"
            ),
            "linkedin_profile": (
                f"https://linkedin.com/in/{contact_data.get('name', 'mock').lower().replace(' ', '')}"
            ),
            "title": contact_data.get("title", "Marketing Manager"),
            "seniority": "mid_level",
            "department": "marketing",
            "phone": "+1-555-0123",
            "verified": True
        })
        return enriched_data
    
    async def find_email(
        self, 
        person_name: str, 
        company_domain: str,
        **kwargs
    ) -> Optional[str]:
        """Mock email finding"""
        name_parts = person_name.split(" ")
        first_name = name_parts[0].lower() if name_parts else "contact"
        return f"{first_name}@{company_domain}"
    
    async def enrich_company(
        self, 
        company_data: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Mock company enrichment"""
        enriched_data = company_data.copy()
        enriched_data.update({
            "description": "Mock company description",
            "employee_count": 50,
            "annual_revenue": "$1M-$5M",
            "tech_stack": ["mock-tech-1", "mock-tech-2"],
            "tags": ["mock-tag-1", "mock-tag-2"],
            "crunchbase_url": (
                f"https://crunchbase.com/organization/{company_data.get('name', 'mock').lower().replace(' ', '-')}"
            )
        })
        return enriched_data