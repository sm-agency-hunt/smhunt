"""
AI provider interfaces for content generation and intelligence
"""
from abc import abstractmethod
from typing import Dict, Any, Optional
from .base_provider import BaseProvider, MockProvider


class AIProvider(BaseProvider):
    """Interface for AI model providers"""

    @abstractmethod
    async def generate_content(
        self,
        prompt: str,
        model_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """Generate content using AI model"""
        pass

    @abstractmethod
    async def classify_intent(
        self,
        text: str,
        **kwargs
    ) -> str:
        """Classify intent from text"""
        pass

    @abstractmethod
    async def analyze_sentiment(
        self,
        text: str,
        **kwargs
    ) -> Dict[str, float]:
        """Analyze sentiment of text"""
        pass


class GroqProvider(AIProvider):
    """Groq provider for fast LLM inference - PRIMARY PROVIDER"""

    async def generate_content(
        self,
        prompt: str,
        model_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """Generate content using Groq API"""
        if not self.api_key:
            raise ValueError("Groq API key required")

        import aiohttp
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": (
                model_params.get("model", "llama-3.1-70b-versatile")
                if model_params else "llama-3.1-70b-versatile"
            ),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": (
                model_params.get("temperature", 0.7)
                if model_params else 0.7
            ),
            "max_tokens": (
                model_params.get("max_tokens", 1000)
                if model_params else 1000
            ),
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=payload, headers=headers
            ) as response:
                response.raise_for_status()
                result = await response.json()

        return result["choices"][0]["message"]["content"]

    async def classify_intent(self, text: str, **kwargs) -> str:
        """Classify intent using Groq API"""
        categories = [
            "interested", "pricing_question",
            "request_meeting", "not_interested",
            "needs_followup", "unsubscribe"
        ]
        prompt = (
            f"Classify the intent. Categories: {', '.join(categories)}. "
            f"Text: {text}. Intent:"
        )
        intent = await self.generate_content(prompt)
        return intent.strip().lower()

    async def analyze_sentiment(self, text: str, **kwargs) -> Dict[str, float]:
        """Analyze sentiment using Groq API"""
        prompt = (
            f"Analyze sentiment of: {text}. "
            "Return JSON: {positive: score, "
            "negative: score, neutral: score}"
        )
        result = await self.generate_content(prompt)
        import json
        try:
            return json.loads(result)
        except Exception:
            return {"positive": 0.5, "negative": 0.3, "neutral": 0.2}


class OpenAIProvider(AIProvider):
    """OpenAI provider - FALLBACK PROVIDER"""

    async def generate_content(
        self,
        prompt: str,
        model_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """Generate content using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key required")

        import aiohttp
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": (
                model_params.get("model", "gpt-3.5-turbo")
                if model_params else "gpt-3.5-turbo"
            ),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": (
                model_params.get("temperature", 0.7)
                if model_params else 0.7
            ),
            "max_tokens": (
                model_params.get("max_tokens", 1000)
                if model_params else 1000
            ),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as response:
                response.raise_for_status()
                result = await response.json()

        return result["choices"][0]["message"]["content"]

    async def classify_intent(self, text: str, **kwargs) -> str:
        """Classify intent using OpenAI API"""
        return "interested"

    async def analyze_sentiment(self, text: str, **kwargs) -> Dict[str, float]:
        """Analyze sentiment using OpenAI API"""
        return {"positive": 0.5, "negative": 0.3, "neutral": 0.2}


class AnthropicProvider(AIProvider):
    """Anthropic provider for content generation"""
    pass


class MockAIProvider(MockProvider, AIProvider):
    """Mock AI provider for testing and development"""

    async def generate_content(
        self,
        prompt: str,
        model_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """Mock content generation"""
        if "outreach" in prompt.lower() or "email" in prompt.lower():
            return (
                f"Mock personalized outreach email content "
                f"based on prompt: {prompt[:50]}..."
            )
        elif "subject" in prompt.lower():
            return (
                f"Mock email subject line based on prompt: {prompt[:30]}"
            )
        else:
            return (
                f"Mock AI-generated content based on prompt: {prompt[:100]}"
            )

    async def classify_intent(self, text: str, **kwargs) -> str:
        """Mock intent classification"""
        import random
        intents = [
            "interested", "pricing_question",
            "request_meeting", "not_interested",
            "needs_followup"
        ]
        return random.choice(intents)

    async def analyze_sentiment(self, text: str, **kwargs) -> Dict[str, float]:
        """Mock sentiment analysis"""
        import random
        total = 1.0
        positive = random.uniform(0.1, 0.9)
        negative = random.uniform(0.0, 1.0 - positive)
        neutral = max(0.0, total - positive - negative)

        return {
            "positive": round(positive, 2),
            "negative": round(negative, 2),
            "neutral": round(neutral, 2)
        }
