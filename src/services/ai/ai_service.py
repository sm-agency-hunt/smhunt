"""
AI service module for content generation and intelligence
"""
from typing import Dict, Any
from src.core.logger import log
from src.services.providers.ai_providers import (
    OpenAIProvider,
    AnthropicProvider,
    MockAIProvider
)


class AIService:
    """Handles AI-powered content generation and intelligence"""

    def __init__(self):
        pass

    async def generate_outreach_content(
        self,
        lead_data: Dict[str, Any],
        context: str = "outreach",
        provider_type: str = "mock"
    ) -> Dict[str, str]:
        """
        Generate personalized outreach content for a lead
        """
        try:
            # Select provider based on type
            if provider_type == "openai":
                provider = OpenAIProvider(api_key=None)  # Use env var
            elif provider_type == "anthropic":
                provider = AnthropicProvider(api_key=None)  # Use env var
            else:  # default to mock
                provider = MockAIProvider()

            # Create prompt based on context and lead data
            if context == "email_subject":
                prompt = self._create_subject_prompt(lead_data)
            elif context == "email_body":
                prompt = self._create_body_prompt(lead_data)
            elif context == "linkedin_message":
                prompt = self._create_linkedin_prompt(lead_data)
            else:  # default to general outreach
                prompt = self._create_general_prompt(lead_data)

            async with provider:
                content = await provider.generate_content(prompt)

            log.info(
                f"Generated {context} content for "
                f"{lead_data.get('business_name', 'Unknown')} "
                f"using {provider_type} provider"
            )
            return {
                "content": content,
                "provider_used": provider_type,
                "success": True
            }
        except Exception as e:
            log.error(f"Error generating outreach content: {e}")
            # Fall back to mock provider if primary provider fails
            try:
                async with MockAIProvider() as provider:
                    if context == "email_subject":
                        prompt = self._create_subject_prompt(lead_data)
                    elif context == "email_body":
                        prompt = self._create_body_prompt(lead_data)
                    elif context == "linkedin_message":
                        prompt = self._create_linkedin_prompt(lead_data)
                    else:
                        prompt = self._create_general_prompt(lead_data)

                    content = await provider.generate_content(prompt)

                log.info(
                    f"Using fallback mock provider "
                    f"for {context} generation"
                )
                return {
                    "content": content,
                    "provider_used": "mock",
                    "success": True
                }
            except Exception as fallback_error:
                log.error(f"Fallback also failed: {fallback_error}")
                return {
                    "content": (
                        f"Mock {context} content for "
                        f"{lead_data.get('business_name', 'Unknown')}"
                    ),
                    "provider_used": "mock",
                    "success": False
                }

    def _create_subject_prompt(self, lead_data: Dict[str, Any]) -> str:
        """Create prompt for email subject generation"""
        return f"""
        Generate a compelling, personalized email
        subject line for a business development outreach.

        Business: {lead_data.get('business_name', 'Unknown')}
        Industry: {lead_data.get('industry', 'N/A')}
        Location: {lead_data.get('city', 'N/A')},
        {lead_data.get('country', 'N/A')}
        Contact: {lead_data.get('contact_name', 'N/A')}
        Website: {lead_data.get('website', 'N/A')}

        The subject line should be:
        - Under 50 characters
        - Attention-grabbing but professional
        - Relevant to their industry and business
        - Personalized to their specific situation

        Subject line:
        """

    def _create_body_prompt(self, lead_data: Dict[str, Any]) -> str:
        """Create prompt for email body generation"""
        return f"""
        Generate a personalized outreach email
        body for business development.

        Business: {lead_data.get('business_name', 'Unknown')}
        Industry: {lead_data.get('industry', 'N/A')}
        Location: {lead_data.get('city', 'N/A')},
        {lead_data.get('country', 'N/A')}
        Contact: {lead_data.get('contact_name', 'N/A')}
        Website: {lead_data.get('website', 'N/A')}
        Service Interest: {lead_data.get('service_interest', 'N/A')}

        The email should be:
        - 150-200 words
        - Professional but friendly tone
        - Focused on helping their business grow
        - Include a clear value proposition
        - Have a soft call-to-action
        - Reference their specific business/industry
        - Be concise and scannable

        Email body:
        """

    def _create_linkedin_prompt(self, lead_data: Dict[str, Any]) -> str:
        """Create prompt for LinkedIn message generation"""
        return f"""
        Generate a personalized LinkedIn
        connection/messaging content.

        Business: {lead_data.get('business_name', 'Unknown')}
        Industry: {lead_data.get('industry', 'N/A')}
        Contact: {lead_data.get('contact_name', 'N/A')}
        Title: {lead_data.get('contact_title', 'N/A')}
        Service Interest: {lead_data.get('service_interest', 'N/A')}

        The message should be:
        - 100-150 words
        - Professional but personable
        - Focused on mutual interests or shared connections
        - Brief introduction of who you are and why connecting
        - Soft request for brief conversation
        - No hard sell

        LinkedIn message:
        """

    def _create_general_prompt(self, lead_data: Dict[str, Any]) -> str:
        """Create general prompt for content generation"""
        return f"""
        Generate personalized
        business development content.

        Business: {lead_data.get('business_name', 'Unknown')}
        Industry: {lead_data.get('industry', 'N/A')}
        Location: {lead_data.get('city', 'N/A')},
        {lead_data.get('country', 'N/A')}
        Contact: {lead_data.get('contact_name', 'N/A')}
        Website: {lead_data.get('website', 'N/A')}
        Service Interest: {lead_data.get('service_interest', 'N/A')}

        Content:
        """

    async def classify_intent(
        self,
        text: str,
        provider_type: str = "mock"
    ) -> str:
        """
        Classify intent from text
        """
        try:
            # Select provider based on type
            if provider_type == "openai":
                provider = OpenAIProvider(api_key=None)
            elif provider_type == "anthropic":
                provider = AnthropicProvider(api_key=None)
            else:  # default to mock
                provider = MockAIProvider()

            async with provider:
                intent = await provider.classify_intent(text)

            log.info(
                f"Classified intent '{intent}' "
                f"from text using {provider_type} provider"
            )
            return intent
        except Exception as e:
            log.error(f"Error classifying intent: {e}")
            # Fall back to mock provider if primary provider fails
            try:
                async with MockAIProvider() as provider:
                    intent = await provider.classify_intent(text)
                log.info(
                    "Using fallback mock provider "
                    "for intent classification"
                )
                return intent
            except Exception as fallback_error:
                log.error(f"Fallback also failed: {fallback_error}")
                return "unknown"

    async def analyze_sentiment(
        self,
        text: str,
        provider_type: str = "mock"
    ) -> Dict[str, float]:
        """
        Analyze sentiment of text
        """
        try:
            # Select provider based on type
            if provider_type == "openai":
                provider = OpenAIProvider(api_key=None)
            elif provider_type == "anthropic":
                provider = AnthropicProvider(api_key=None)
            else:  # default to mock
                provider = MockAIProvider()

            async with provider:
                sentiment = await provider.analyze_sentiment(text)

            log.info(
                f"Analyzed sentiment "
                f"using {provider_type} provider"
            )
            return sentiment
        except Exception as e:
            log.error(f"Error analyzing sentiment: {e}")
            # Fall back to mock provider if primary provider fails
            try:
                async with MockAIProvider() as provider:
                    sentiment = await provider.analyze_sentiment(text)
                log.info(
                    "Using fallback mock provider "
                    "for sentiment analysis"
                )
                return sentiment
            except Exception as fallback_error:
                log.error(f"Fallback also failed: {fallback_error}")
                return {"positive": 0.5, "negative": 0.3, "neutral": 0.2}
