"""
Discovery provider interfaces for business search - SERPAPI Integration
"""
import os
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


class SerpApiProvider(DiscoveryProvider):
    """SERPAPI provider for business discovery - PRIMARY PROVIDER"""
    
    async def search_businesses(
        self, 
        niche: str, 
        location: str, 
        count: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for businesses using SERPAPI"""
        if not self.api_key:
            raise ValueError("SERPAPI key required")
        
       import aiohttp
        # Example queries from requirements
        query = f"{niche} in {location}"
        
       url = "https://serpapi.com/search"
       params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": count
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                result = await response.json()
        
        results = []
        organic_results = result.get("organic_results", [])[:count]
        
        for item in organic_results:
            business_data = {
                "id": item.get("position", len(results)),
                "business_name": item.get("title", "Unknown Business"),
                "address": location,
                "phone": "",
                "website": item.get("link", ""),
                "city": location.split(",")[-1].strip() if "," in location else location,
                "country": "USA",
                "industry": niche,
                "source": "serpapi",
                "snippet": item.get("snippet", "")
            }
            results.append(business_data)
        
        return results
    
    async def search_competitors(
        self, 
        business_name: str, 
        location: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for competitors using SERPAPI"""
        query = f"competitors of {business_name} in {location}"
        return await self.search_businesses(query, location, **kwargs)


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
        
       import aiohttp
       url = "https://places.googleapis.com/v1/places:searchText"
       params = {
            "input": f"{niche} in {location}",
            "inputtype": "textquery",
            "fields": "displayName,addressComponents,formattedAddress,nationalPhoneNumber,websiteUri"
        }
        
        headers = {
            "X-Goog-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, headers=headers) as response:
                response.raise_for_status()
                result = await response.json()
        
        results = []
        places = result.get("places", [])[:count]
        
        for place in places:
            business_data = {
                "id": place.get("id", len(results)),
                "business_name": place.get("displayName", {}).get("text", ""),
                "address": place.get("formattedAddress", ""),
                "phone": place.get("nationalPhoneNumber", ""),
                "website": place.get("websiteUri", ""),
                "city": location,
                "country": "USA",
                "industry": niche,
                "source": "google_maps"
            }
            results.append(business_data)
        
        return results
    
    async def search_competitors(
        self, 
        business_name: str, 
        location: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for competitors using Google Maps API"""
        return await self.search_businesses(business_name, location, **kwargs)


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
        
       import aiohttp
       url = "https://api.yelp.com/v3/businesses/search"
       params = {
            "term": niche,
            "location": location,
            "limit": count
        }
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                response.raise_for_status()
                result = await response.json()
        
        results = []
        businesses = result.get("businesses", [])[:count]
        
        for business in businesses:
            business_data = {
                "id": business.get("id", len(results)),
                "business_name": business.get("name", ""),
                "address": ", ".join(business.get("location", {}).get("display_address", [])),
                "phone": business.get("phone", ""),
                "website": business.get("url", ""),
                "city": business.get("location", {}).get("city", location),
                "country": business.get("location", {}).get("country", "USA"),
                "industry": niche,
                "rating": business.get("rating"),
                "review_count": business.get("review_count"),
                "source": "yelp"
            }
            results.append(business_data)
        
        return results
    
    async def search_competitors(
        self, 
        business_name: str, 
        location: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for competitors using Yelp API"""
        return await self.search_businesses(business_name, location, **kwargs)


class MockDiscoveryProvider(MockProvider, DiscoveryProvider):
    """Mock discovery provider for testing"""
    
    async def search_businesses(
        self, 
        niche: str, 
        location: str, 
        count: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Mock business search"""
        results = []
        for i in range(count):
            results.append({
                "id": i + 1,
                "business_name": f"Mock {niche} Business {i+1}",
                "address": f"123 Mock Street, {location}",
                "phone": f"+1-555-0{i+1:02d}",
                "website": f"https://mockbusiness{i+1}.com",
                "city": location,
                "country": "USA",
                "industry": niche,
                "source": "mock"
            })
        return results
    
    async def search_competitors(
        self, 
        business_name: str, 
        location: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Mock competitor search"""
        return await self.search_businesses(business_name, location, **kwargs)

