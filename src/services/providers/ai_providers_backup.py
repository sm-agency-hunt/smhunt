"""
Base provider interface for all external API integrations
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import asyncio
import aiohttp
from src.core.logger import log


class BaseProvider(ABC):
    """Base interface for all providers"""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        self.api_key = api_key
        self.session = None
        self.rate_limit_delay = kwargs.get('rate_limit_delay', 1)
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={"User-Agent": "SMHunt/1.0"}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling and rate limiting"""
        if not self.session:
            raise RuntimeError(
                "Provider not initialized. Use 'async with' statement."
            )
        
        # Add API key to headers if provided
        if self.api_key:
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Authorization'] = f"Bearer {self.api_key}"
        
        try:
            # Rate limiting
            await asyncio.sleep(self.rate_limit_delay)
            
            async with self.session.request(method, url, **kwargs) as response:
                if response.status == 429:  # Rate limited
                    log.warning(f"Rate limited by {url}, waiting...")
                    await asyncio.sleep(60)  # Wait 1 minute before retry
                    return await self._make_request(method, url, **kwargs)
                
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            log.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            log.error(f"Unexpected error occurred: {e}")
            raise
    
    @abstractmethod
    async def search(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """Search for data"""
        pass
    
    @abstractmethod
    async def validate(self, data: Dict[str, Any], **kwargs) -> bool:
        """Validate data"""
        pass


class MockProvider(BaseProvider):
    """Mock provider for testing and development"""
    
    async def search(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """Return mock search results"""
        # Parse query to extract location and niche
        parts = query.split(" in ")
        if len(parts) >= 2:
            niche = parts[0].strip()
            location = parts[1].strip()
        else:
            niche = query
            location = "USA"
        
        count = kwargs.get('count', 10)
        results = []
        
        for i in range(count):
            result = {
                "id": f"mock_{i}",
                "business_name": f"Mock Business {i+1}",
                "website": f"https://mockbusiness{i+1}.com",
                "phone": f"+1-555-{100+i:04d}",
                "email": f"contact@mockbusiness{i+1}.com",
                "city": location,
                "country": "USA",
                "industry": niche,
                "contact_name": f"Mock Contact {i+1}",
                "contact_email": f"contact.mock{i+1}@mockbusiness{i+1}.com",
                "address": f"Mock Street {i+1}, {location}",
                "linkedin_profile": (
                    f"https://linkedin.com/company/mockbusiness{i+1}"
                ),
                "source": "mock"
            }
            results.append(result)
        
        return results
    
    async def validate(self, data: Dict[str, Any], **kwargs) -> bool:
        """Mock validation"""
        return True