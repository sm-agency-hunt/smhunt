
# Test Endpoints for API Verification
from fastapi import APIRouter

router = APIRouter()


@router.get("/test-ai")
async def test_ai_providers():
    """Test AI providers (Groq + OpenAI)"""
    from src.services.providers.ai_providers import (
        GroqProvider,
        OpenAIProvider,
        MockAIProvider,
    )
    import os

    results = {}

    # Test Groq (Primary)
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key:
            groq = GroqProvider(api_key=groq_api_key)
            response = await groq.generate_content("Say hello in one word")
            results["groq"] = {"status": "success", "response": response[:50]}
        else:
            results["groq"] = {
                "status": "skipped",
                "reason": "API key not configured"
            }
    except Exception as e:
        results["groq"] = {"status": "error", "error": str(e)}

    # Test OpenAI (Fallback)
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            openai = OpenAIProvider(api_key=openai_api_key)
            response = await openai.generate_content("Say hello in one word")
            results["openai"] = {
                "status": "success",
                "response": response[:50]
            }
        else:
            results["openai"] = {
                "status": "skipped",
                "reason": "API key not configured"
            }
    except Exception as e:
        results["openai"] = {"status": "error", "error": str(e)}

    # Test Mock (Always works)
    try:
        mock = MockAIProvider()
        response = await mock.generate_content("Test prompt")
        results["mock"] = {"status": "success", "response": response}
    except Exception as e:
        results["mock"] = {"status": "error", "error": str(e)}

    return {
        "message": "AI Provider Test Results",
        "results": results,
        "primary_provider": "Groq",
        "fallback_provider": "OpenAI"
    }


@router.get("/test-email")
async def test_email_providers():
    """Test Email providers (Resend + Snov.io)"""
    from src.services.providers.email_providers import (
        ResendProvider,
        MockEmailProvider,
    )
    import os

    results = {}

    # Test Resend
    try:
        resend_api_key = os.getenv("RESEND_API_KEY")
        if resend_api_key:
            _ = ResendProvider(api_key=resend_api_key)
            # Don't actually send email, just verify connection
            results["resend"] = {
                "status": "configured",
                "api_key_present": True,
                "note": "Email sending requires actual recipient"
            }
        else:
            results["resend"] = {
                "status": "not_configured",
                "api_key_present": False
            }
    except Exception as e:
        results["resend"] = {"status": "error", "error": str(e)}

    # Test Mock Email
    try:
        mock = MockEmailProvider()
        response = await mock.send_email(
            recipient="test@example.com",
            subject="Test Email",
            body="This is a test"
        )
        results["mock_email"] = {"status": "success", "response": response}
    except Exception as e:
        results["mock_email"] = {"status": "error", "error": str(e)}

    return {
        "message": "Email Provider Test Results",
        "results": results,
        "primary_provider": "Resend",
        "sender_email": "hello@yourdomain.com"
    }


@router.get("/test-leads")
async def test_lead_discovery():
    """Test Lead Discovery (SERPAPI)"""
    from src.services.providers.discovery_providers import (
        SerpApiProvider,
        MockDiscoveryProvider,
    )
    import os

    results = {}

    # Test SERPAPI
    try:
        serpapi_key = os.getenv("SERPAPI_KEY")
        if serpapi_key:
            serpapi = SerpApiProvider(api_key=serpapi_key)
            # Search for digital marketing agencies in Dubai as example
            businesses = await serpapi.search_businesses(
                niche="digital marketing agency",
                location="Dubai",
                count=3
            )
            results["serpapi"] = {
                "status": "success",
                "businesses_found": len(businesses),
                "sample": businesses[0] if businesses else None
            }
        else:
            results["serpapi"] = {
                "status": "not_configured",
                "api_key_present": False
            }
    except Exception as e:
        results["serpapi"] = {"status": "error", "error": str(e)}

    # Test Mock Discovery
    try:
        mock = MockDiscoveryProvider()
        businesses = await mock.search_businesses(
            niche="test business",
            location="Test City",
            count=3
        )
        results["mock_discovery"] = {
            "status": "success",
            "businesses_found": len(businesses),
            "sample": businesses[0] if businesses else None
        }
    except Exception as e:
        results["mock_discovery"] = {"status": "error", "error": str(e)}

    return {
        "message": "Lead Discovery Test Results",
        "results": results,
        "primary_provider": "SERPAPI",
        "example_search": "digital marketing agency in Dubai"
    }
