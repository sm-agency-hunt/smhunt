"""
SMHunt Autonomous Client Acquisition Agent
Main application entry point for Vercel deployment
"""
import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the FastAPI app from src.api.main
# flake8: noqa: E402
from src.api.main import app as fastapi_app

# Export app for Vercel deployment
app = fastapi_app

def handler(event, context):
    """Vercel serverless function handler"""
    from mangum import Mangum
    asgi_handler = Mangum(fastapi_app)
    return asgi_handler(event, context)

if __name__ == "__main__":
    import uvicorn

    # Check if we're in development mode
    debug = os.getenv("DEBUG", "True").lower() == "true"

    uvicorn.run(
        "src.api.main:app",  # Use string reference for proper reloading
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=debug,
        log_level="info"
    )