from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
import os

app = FastAPI(
    title="AI Job Application Tracker",
    description="Track job applications and get AI-powered resume tips",
    version="1.0.0"
)

# Enable CORS to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
def read_root():
    """Root endpoint - API is running"""
    return {
        "message": "AI Job Application Tracker API",
        "status": "running",
        "docs_url": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    # Auto-reload on code changes during development
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
