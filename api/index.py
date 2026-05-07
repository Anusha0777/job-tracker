from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Job Application Tracker",
    description="Track job applications and get AI-powered resume tips",
    version="1.0.0",
    root_path="/api"
)

# Enable CORS to allow requests from React frontend
cors_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002",
    "http://127.0.0.1:5173",
]

# Allow all localhost variants during development
if os.getenv("ENVIRONMENT", "development") == "development":
    cors_origins.extend([
        "http://localhost",
        "http://127.0.0.1",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
def read_root():
    """Root endpoint - API is running"""
    logger.info("Root endpoint called")
    return {
        "message": "AI Job Application Tracker API",
        "status": "running",
        "docs_url": "/docs",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    logger.info("Health check called")
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("=" * 50)
    logger.info("🚀 AI Job Application Tracker Backend Starting")
    logger.info(f"⏰ Started at: {datetime.now().isoformat()}")
    logger.info(f"📍 Database: SQLite (job_tracker.db)")
    logger.info(f"🌐 CORS Origins: localhost:3000, localhost:5173")
    logger.info(f"📖 API Docs: http://localhost:8000/docs")
    logger.info("=" * 50)


# Mangum handler for Vercel
from mangum import Mangum

handler = Mangum(app)


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn server...")
    uvicorn.run(
        "index:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
