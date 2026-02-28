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


class OpenAIProvider(AIProvider):
    """OpenAI provider for content generation"""
    
    async def generate_content(
        self, 
        prompt: str, 
        model_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """Generate content using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        
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
        
        response = await self._make_request("POST", url, json=payload)
        
        return response["choices"][0]["message"]["content"]
    
    async def classify_intent(
        self, 
        text: str,
        **kwargs
    ) -> str:
        """Classify intent using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        
        categories = [
            "interested", "pricing_question", "request_meeting", 
            "not_interested", "needs_followup", "unsubscribe"
        ]
        prompt = f"""
Classify the intent of the following text. 
Respond with only one of these categories:
{', '.join(categories)}

Text: {text}

Intent:
"""
        
        intent = await self.generate_content(prompt)
        return intent.strip().lower()
    
    async def analyze_sentiment(
        self, 
        text: str,
        **kwargs
    ) -> Dict[str, float]:
        """Analyze sentiment using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        
        prompt = f"""
Analyze the sentiment of the following text. 
Respond with a JSON object containing:
- positive: confidence score (0-1)
- negative: confidence score (0-1) 
- neutral: confidence score (0-1)

Text: {text}
"""
        
        result = await self.generate_content(prompt)
        
        # Parse the result as JSON
        import json
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            # Return default values if parsing fails
            return {"positive": 0.5, "negative": 0.3, "neutral": 0.2}


class AnthropicProvider(AIProvider):
    """Anthropic provider for content generation"""
    
    async def generate_content(
        self, 
        prompt: str, 
        model_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """Generate content using Anthropic API"""
        if not self.api_key:
            raise ValueError("Anthropic API key required")
        
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": (
                model_params.get("model", "claude-3-haiku-20240307") 
                if model_params else "claude-3-haiku-20240307"
            ),
            "max_tokens": (
                model_params.get("max_tokens", 1000) 
                if model_params else 1000
            ),
            "temperature": (
                model_params.get("temperature", 0.7) 
                if model_params else 0.7
            ),
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = await self._make_request("POST", url, json=payload)
        
        return response["content"][0]["text"]
    
    async def classify_intent(
        self, 
        text: str,
        **kwargs
    ) -> str:
        """Classify intent using Anthropic API"""
        if not self.api_key:
            raise ValueError("Anthropic API key required")
        
        prompt = f"""
        Human: Classify the intent of the following text. Respond with only one of these categories:
        interested, pricing_question, request_meeting, not_interested, needs_followup, unsubscribe
        
        Text: {text}
        
        Assistant: Intent:
        """
        
        intent = await self.generate_content(prompt)
        return intent.strip().lower()
    
    async def analyze_sentiment(
        self, 
        text: str,
        **kwargs
    ) -> Dict[str, float]:
        """Analyze sentiment using Anthropic API"""
        if not self.api_key:
            raise ValueError("Anthropic API key required")
        
        prompt = f"""
        Human: Analyze the sentiment of the following text. Respond with a JSON object containing:
        - positive: confidence score (0-1)
        - negative: confidence score (0-1) 
        - neutral: confidence score (0-1)
        
        Text: {text}
        
        Assistant:
        """
        
        result = await self.generate_content(prompt)
        
        # Parse the result as JSON
        import json
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            # Return default values if parsing fails
            return {"positive": 0.5, "negative": 0.3, "neutral": 0.2}


class MockAIProvider(MockProvider, AIProvider):
    """Mock AI provider for testing and development"""
    
    async def generate_content(
        self, 
        prompt: str, 
        model_params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """Mock content generation"""
        # Extract the key information from the prompt
        # to generate relevant mock content
        if (
            "outreach" in prompt.lower() or 
            "email" in prompt.lower()
        ):
            return (
                f"Mock personalized outreach email "
                f"content based on prompt: {prompt[:50]}..."
            )
        elif "subject" in prompt.lower():
            return f"Mock email subject line based on prompt: {prompt[:30]}"
        else:
            return f"Mock AI-generated content based on prompt: {prompt[:100]}"
    
    async def classify_intent(
        self, 
        text: str,
        **kwargs
    ) -> str:
        """Mock intent classification"""
        import random
        intents = [
            "interested", "pricing_question", "request_meeting", 
            "not_interested", "needs_followup"
        ]
        return random.choice(intents)
    
    async def analyze_sentiment(
        self, 
        text: str,
        **kwargs
    ) -> Dict[str, float]:
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