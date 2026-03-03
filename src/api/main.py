import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.core.logger import log
from src.database.connection import init_database, create_admin_user
from src.api.v1.routers import (
    auth, leads, outreach, analytics, business, discovery,
    enrichment, ai, email, scheduling, crm, website_intelligence, tasks
)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SMHunt Autonomous Client Acquisition Agent API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(leads.router, prefix="/api/v1", tags=["Leads"])
app.include_router(outreach.router, prefix="/api/v1", tags=["Outreach"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(business.router, prefix="/api/v1", tags=["Business"])
app.include_router(discovery.router, prefix="/api/v1", tags=["Discovery"])
app.include_router(enrichment.router, prefix="/api/v1", tags=["Enrichment"])
app.include_router(ai.router, prefix="/api/v1", tags=["AI"])
app.include_router(email.router, prefix="/api/v1", tags=["Email"])
app.include_router(scheduling.router, prefix="/api/v1", tags=["Scheduling"])
app.include_router(crm.router, prefix="/api/v1", tags=["CRM"])
app.include_router(
    website_intelligence.router,
    prefix="/api/v1",
    tags=["Website Intelligence"]
)
app.include_router(tasks.router, prefix="/api/v1", tags=["Tasks"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        log.info("Starting SMHunt application...")

        # Only initialize database if not in Vercel serverless environment
        if not os.getenv("VERCEL"):
            try:
                # Initialize database
                init_database()

                # Create admin user
                create_admin_user()
            except Exception as db_error:
                # Handle duplicate table/index errors gracefully
                if "already exists" in str(db_error):
                    log.warning("Database tables already exist")
                else:
                    raise

        log.info("SMHunt application started successfully")

    except Exception as e:
        log.error(f"Failed to start application: {e}")
        # Don't raise in Vercel environment to prevent deployment failures
        if not os.getenv("VERCEL"):
            raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    log.info("Shutting down SMHunt application...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SMHunt Lead Intelligence & Client Acquisition System",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # In Vercel serverless environment, skip database check
    if os.getenv("VERCEL"):
        return {
            "status": "healthy",
            "database": "skipped_in_serverless",
            "timestamp": "2024-01-01T00:00:00Z",
            "environment": "vercel_serverless"
        }

    from src.database.connection import health_check

    db_healthy = health_check()

    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    log.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
