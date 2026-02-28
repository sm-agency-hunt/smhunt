"""
Business discovery service module
"""
from typing import List, Dict
from src.core.logger import log
from src.services.providers.discovery_providers import (
    GoogleMapsProvider, YelpProvider, YellowPagesProvider,
    IndustryDirectoryProvider, MockProvider
)


class DiscoveryService:
    """Handles business discovery and identification"""

    def __init__(self):
        self.session = None

    async def discover_businesses(
        self, 
        niche: str, 
        location: str, 
        count: int = 10, 
        provider_type: str = "mock"
    ) -> List[Dict]:
        """
        Discover businesses based on niche and location
        Supports different providers: google_maps, yelp, 
        yellow_pages, industry_directory, mock
        """
        try:
            # Select provider based on type
            if provider_type == "google_maps":
                provider = GoogleMapsProvider(api_key=None)  # Will use env var
            elif provider_type == "yelp":
                provider = YelpProvider(api_key=None)  # Will use env var
            elif provider_type == "yellow_pages":
                provider = YellowPagesProvider()
            elif provider_type == "industry_directory":
                provider = IndustryDirectoryProvider()
            else:  # default to mock
                provider = MockProvider()

            async with provider:
                businesses = await provider.search_businesses(
                    niche=niche, location=location, count=count
                )

            log.info(
                f"Discovered {len(businesses)} businesses in {location} for "
                f"{niche} niche using {provider_type} provider"
            )
            return businesses
        except Exception as e:
            log.error(f"Error discovering businesses: {e}")
            # Fall back to mock provider if primary provider fails
            try:
                async with MockProvider() as provider:
                    businesses = await provider.search_businesses(
                        niche=niche, location=location, count=count
                    )
                log.info(
                    f"Using fallback mock provider, "
                    f"discovered {len(businesses)} businesses"
                )
                return businesses
            except Exception as fallback_error:
                log.error(f"Fallback also failed: {fallback_error}")
                return []

    async def validate_business(self, business_data: Dict) -> bool:
        """
        Validate business information
        """
        try:
            # Basic validation checks
            required_fields = ['business_name', 'city', 'country', 'industry']
            for field in required_fields:
                if not business_data.get(field):
                    return False

            # Validate email format if present
            email = business_data.get('email')
            if email:
                import re
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(pattern, email):
                    return False

            log.info(
                f"Validated business: {business_data.get('business_name')}"
            )
            return True
        except Exception as e:
            log.error(f"Error validating business: {e}")
            return False

    async def search_competitors(
        self, 
        business_name: str, 
        location: str, 
        count: int = 10, 
        provider_type: str = "mock"
    ) -> List[Dict]:
        """
        Search for competitor businesses
        """
        try:
            # Select provider based on type
            if provider_type == "google_maps":
                provider = GoogleMapsProvider(api_key=None)
            elif provider_type == "yelp":
                provider = YelpProvider(api_key=None)
            elif provider_type == "yellow_pages":
                provider = YellowPagesProvider()
            elif provider_type == "industry_directory":
                provider = IndustryDirectoryProvider()
            else:  # default to mock
                provider = MockProvider()

            async with provider:
                competitors = await provider.search_competitors(
                    business_name=business_name, location=location
                )

            log.info(
                f"Found {len(competitors)} competitors for {business_name} "
                f"in {location} using {provider_type} provider"
            )
            return competitors[:count]
        except Exception as e:
            log.error(f"Error searching competitors: {e}")
            # Fall back to mock provider if primary provider fails
            try:
                async with MockProvider() as provider:
                    competitors = await provider.search(
                        f"{business_name} competitors in {location}", count=count
                    )
                log.info(
                    f"Using fallback mock provider, "
                    f"found {len(competitors)} competitors"
                )
                return competitors
            except Exception as fallback_error:
                log.error(f"Fallback also failed: {fallback_error}")
                return []
