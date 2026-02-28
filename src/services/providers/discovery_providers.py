"""
Discovery provider interfaces for business search
"""
from abc import abstractmethod
from typing import List, Dict, Any
from .base_provider import BaseProvider, MockProvider


class DiscoveryProvider(BaseProvider):
    """Interface for business discovery providers"""
    
    @abstractmethod
    async def search_businesses(
        self, 
        niche: str, 
        location: str, 
        count: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for businesses in a specific niche and location"""
        pass
    
    @abstractmethod
    async def search_competitors(
        self, 
        business_name: str, 
        location: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for competitor businesses"""
        pass


class GoogleMapsProvider(DiscoveryProvider):
    """Google Maps API provider for business discovery"""
    
    async def search_businesses(
        self, 
        niche: str, 
        location: str, 
        count: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for businesses using Google Maps API"""
        if not self.api_key:
            raise ValueError("Google Maps API key required")
        
        url = "https://places.googleapis.com/v1/places:searchText"
        params = {
            "input": f"{niche} in {location}",
            "inputtype": "textquery",
            "fields": (
                "displayName,addressComponents,formattedAddress,"
                "nationalPhoneNumber,websiteUri"
            )
        }
        
        response = await self._make_request("POST", url, json=params)
        
        results = []
        for place in response.get("places", [])[:count]:
            result = {
                "id": place.get("id"),
                "business_name": place.get("displayName", {}).get("text", ""),
                "address": place.get("formattedAddress", ""),
                "phone": place.get("nationalPhoneNumber", ""),
                "website": place.get("websiteUri", ""),
                "city": location,  # Simplified for demo
                "country": "USA",  # Simplified for demo
                "industry": niche,
                "source": "google_maps"
            }
            results.append(result)
        
        return results
    
    async def search_competitors(
        self, 
        business_name: str, 
        location: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for competitors using Google Maps API"""
        if not self.api_key:
            raise ValueError("Google Maps API key required")
        
        url = "https://places.googleapis.com/v1/places:searchText"
        params = {
            "input": f"competitors of {business_name} in {location}",
            "inputtype": "textquery",
            "fields": (
                "displayName,addressComponents,formattedAddress,"
                "nationalPhoneNumber,websiteUri"
            )
        }
        
        response = await self._make_request("POST", url, json=params)
        
        results = []
        for place in response.get("places", []):
            result = {
                "id": place.get("id"),
                "business_name": place.get("displayName", {}).get("text", ""),
                "address": place.get("formattedAddress", ""),
                "phone": place.get("nationalPhoneNumber", ""),
                "website": place.get("websiteUri", ""),
                "city": location,
                "country": "USA",
                "industry": business_name,
                "source": "google_maps"
            }
            results.append(result)
        
        return results


class YelpProvider(DiscoveryProvider):
    """Yelp API provider for business discovery"""
    
    async def search_businesses(
        self, 
        niche: str, 
        location: str, 
        count: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for businesses using Yelp API"""
        if not self.api_key:
            raise ValueError("Yelp API key required")
        
        url = "https://api.yelp.com/v3/businesses/search"
        params = {
            "term": niche,
            "location": location,
            "limit": count
        }
        
        response = await self._make_request("GET", url, params=params)
        
        results = []
        for business in response.get("businesses", []):
            result = {
                "id": business.get("id"),
                "business_name": business.get("name", ""),
                "address": ", ".join(
                    business.get("location", {}).get("display_address", [])
                ),
                "phone": business.get("phone", ""),
                "website": business.get("url", ""),
                "city": business.get("location", {}).get("city", location),
                "country": business.get("location", {}).get("country", "USA"),
                "industry": niche,
                "rating": business.get("rating"),
                "review_count": business.get("review_count"),
                "source": "yelp"
            }
            results.append(result)
        
        return results
    
    async def search_competitors(
        self, 
        business_name: str, 
        location: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for competitors using Yelp API"""
        return await self.search_businesses(business_name, location)


class YellowPagesProvider(DiscoveryProvider):
    """Yellow Pages provider for business discovery"""
    
    async def search_businesses(
        self, 
        niche: str, 
        location: str, 
        count: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for businesses using Yellow Pages"""
        # This would be a web scraping implementation in real scenario
        # For now, return mock data
        query = f"{niche} in {location}"
        return await MockProvider().search(query, count=count)
    
    async def search_competitors(
        self, 
        business_name: str, 
        location: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for competitors using Yellow Pages"""
        return await self.search_businesses(business_name, location)


class IndustryDirectoryProvider(DiscoveryProvider):
    """Industry directory provider for business discovery"""
    
    async def search_businesses(
        self, 
        niche: str, 
        location: str, 
        count: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for businesses using industry directories"""
        # This would be a web scraping implementation in real scenario
        # For now, return mock data
        query = f"{niche} in {location}"
        return await MockProvider().search(query, count=count)
    
    async def search_competitors(
        self, 
        business_name: str, 
        location: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for competitors using industry directories"""
        return await self.search_businesses(business_name, location)