"""
Contact enrichment service module
"""
from typing import Dict, Optional
from src.core.logger import log
from src.services.providers.enrichment_providers import (
    HunterProvider, ClearbitProvider, LinkedInProvider, MockEnrichmentProvider
)


class EnrichmentService:
    """Handles contact information enrichment"""

    async def enrich_contact(
        self, 
        business_data: Dict, 
        provider_type: str = "mock"
    ) -> Dict:
        """
        Enrich business contact information
        Supports different providers: hunter, clearbit, 
        linkedin, mock
        """
        try:
            # Select provider based on type
            if provider_type == "hunter":
                provider = HunterProvider(api_key=None)  # Will use env var
            elif provider_type == "clearbit":
                provider = ClearbitProvider(api_key=None)  # Will use env var
            elif provider_type == "linkedin":
                provider = LinkedInProvider(api_key=None)  # Will use env var
            else:  # default to mock
                provider = MockEnrichmentProvider()

            async with provider:
                enriched_data = await provider.enrich_contact(business_data)

            log.info(
                f"Enriched contact {business_data.get('name', 'Unknown')} "
                f"using {provider_type} provider"
            )
            return enriched_data
        except Exception as e:
            log.error(f"Error enriching contact: {e}")
            # Fall back to mock provider if primary provider fails
            try:
                async with MockEnrichmentProvider() as provider:
                    enriched_data = await provider.enrich_contact(business_data)
                log.info("Using fallback mock provider for contact enrichment")
                return enriched_data
            except Exception as fallback_error:
                log.error(f"Fallback also failed: {fallback_error}")
                return business_data

    async def find_email(
        self, business_name: str, domain: str, provider_type: str = "mock"
    ) -> Optional[str]:
        """
        Find email for a business
        """
        try:
            # Select provider based on type
            if provider_type == "hunter":
                provider = HunterProvider(api_key=None)
            elif provider_type == "clearbit":
                provider = ClearbitProvider(api_key=None)
            elif provider_type == "linkedin":
                provider = LinkedInProvider(api_key=None)
            else:  # default to mock
                provider = MockEnrichmentProvider()

            async with provider:
                email = await provider.find_email(business_name, domain)

            log.info(
                f"Found email for {business_name} at {domain} "
                f"using {provider_type} provider"
            )
            return email
        except Exception as e:
            log.error(f"Error finding email: {e}")
            # Fall back to mock provider if primary provider fails
            try:
                async with MockEnrichmentProvider() as provider:
                    email = await provider.find_email(business_name, domain)
                log.info("Using fallback mock provider for email finding")
                return email
            except Exception as fallback_error:
                log.error(f"Fallback also failed: {fallback_error}")
                # Generate a mock email as final fallback
                name_parts = business_name.split(" ")
                first_name = name_parts[0].lower() if name_parts else "contact"
                return f"{first_name}@{domain}"

    async def find_social_profiles(self, business_data: Dict, provider_type: str = "mock") -> Dict:
        """
        Find social media profiles for a business
        """
        try:
            # Select provider based on type
            if provider_type == "hunter":
                provider = HunterProvider(api_key=None)
            elif provider_type == "clearbit":
                provider = ClearbitProvider(api_key=None)
            elif provider_type == "linkedin":
                provider = LinkedInProvider(api_key=None)
            else:  # default to mock
                provider = MockEnrichmentProvider()

            async with provider:
                enriched_data = await provider.enrich_company(business_data)

            log.info(
                f"Found social profiles for "
                f"{business_data.get('name', 'Unknown')} "
                f"using {provider_type} provider"
            )
            return enriched_data
        except Exception as e:
            log.error(f"Error finding social profiles: {e}")
            # Fall back to mock provider if primary provider fails
            try:
                async with MockEnrichmentProvider() as provider:
                    enriched_data = await provider.enrich_company(business_data)
                log.info(
                    "Using fallback mock provider "
                    "for social profile "
                    "finding"
                )
                return enriched_data
            except Exception as fallback_error:
                log.error(f"Fallback also failed: {fallback_error}")
                return business_data


# Create a singleton instance for import
enrichment_service = EnrichmentService()
