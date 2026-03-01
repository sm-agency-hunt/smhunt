"""
Simple FastAPI test application
This demonstrates the correct structure for a FastAPI app
"""
from fastapi import FastAPI


# Create the FastAPI app instance
app = FastAPI(
    title="SMHunt Test API",
    version="1.0.0",
    description="Simple test to verify FastAPI setup"
)


# Add a sample route
@app.get("/")
async def root():
    return {
        "message": "SMHunt FastAPI is working!",
        "status": "success",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "SMHunt API"
    }


@app.get("/test")
async def test_endpoint():
    return {
        "message": "Test endpoint working",
        "timestamp": "2024-01-01T00:00:00Z"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "simple_main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )