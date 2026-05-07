from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, DateTime, Enum, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from enum import Enum as PyEnum
import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# LOGGING
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DATABASE SETUP
# ============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////tmp/job_tracker.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================================================
# DATABASE MODELS
# ============================================================================
class ApplicationStatus(str, PyEnum):
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    REJECTED = "Rejected"
    OFFER = "Offer"


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(255), index=True)
    role = Column(String(255), index=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    application_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


Base.metadata.create_all(bind=engine)

# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================
class JobApplicationCreate(BaseModel):
    company: str
    role: str
    application_date: datetime = None
    status: str = "Applied"


class JobApplicationUpdate(BaseModel):
    status: ApplicationStatus


class JobApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    status: ApplicationStatus
    application_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_applications: int
    interviews: int
    offers: int
    rejected: int
    by_status: dict


class AITipRequest(BaseModel):
    job_description: str


class AITipResponse(BaseModel):
    bullet_points: list[str]

# ============================================================================
# AI HELPER (Gemini Integration)
# ============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def get_resume_tips(job_description: str) -> list[str]:
    """Generate resume tips using Gemini API"""
    if not GEMINI_API_KEY:
        return [
            "Error: GEMINI_API_KEY not configured. Please set it in your environment variables.",
            "",
            ""
        ]

    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""Based on this job description, provide exactly 3 specific, actionable resume bullet points that would help a candidate stand out for this role. Format as a numbered list.

Job Description:
{job_description}

Return only the 3 bullet points, nothing else."""

        response = model.generate_content(prompt)

        if response.text:
            lines = response.text.strip().split('\n')
            bullet_points = []

            for line in lines:
                line = line.strip()
                if line and any(char.isalpha() for char in line):
                    cleaned = line.lstrip('0123456789.-) ')
                    if cleaned:
                        bullet_points.append(cleaned)

            while len(bullet_points) < 3:
                bullet_points.append("")

            return bullet_points[:3]
        else:
            return ["No response from API", "", ""]

    except Exception as e:
        return [f"Error calling Gemini API: {str(e)}", "", ""]

# ============================================================================
# FASTAPI APP
# ============================================================================
app = FastAPI(
    title="AI Job Application Tracker",
    description="Track job applications and get AI-powered resume tips",
    version="1.0.0"
)

# Enable CORS
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

# ============================================================================
# DEPENDENCY
# ============================================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# ROUTES
# ============================================================================

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


# Applications CRUD Endpoints

@app.get("/applications", response_model=list[JobApplicationResponse])
def get_all_applications(db: Session = Depends(get_db)):
    """Get all job applications sorted by date (newest first)"""
    applications = db.query(JobApplication).order_by(
        JobApplication.application_date.desc()
    ).all()
    return applications


@app.post("/applications", response_model=JobApplicationResponse)
def create_application(
    app: JobApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create a new job application"""
    if not app.application_date:
        app.application_date = datetime.utcnow()

    db_app = JobApplication(
        company=app.company,
        role=app.role,
        application_date=app.application_date,
        status=ApplicationStatus(app.status)
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


@app.patch("/applications/{app_id}", response_model=JobApplicationResponse)
def update_application_status(
    app_id: int,
    update: JobApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Update the status of a job application"""
    db_app = db.query(JobApplication).filter(JobApplication.id == app_id).first()

    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")

    db_app.status = update.status
    db.commit()
    db.refresh(db_app)
    return db_app


@app.delete("/applications/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    """Delete a job application"""
    db_app = db.query(JobApplication).filter(JobApplication.id == app_id).first()

    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(db_app)
    db.commit()
    return {"message": "Application deleted successfully"}


# Stats Endpoint

@app.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    total = db.query(func.count(JobApplication.id)).scalar() or 0
    interviews = db.query(func.count(JobApplication.id)).filter(
        JobApplication.status == ApplicationStatus.INTERVIEW
    ).scalar() or 0
    offers = db.query(func.count(JobApplication.id)).filter(
        JobApplication.status == ApplicationStatus.OFFER
    ).scalar() or 0
    rejected = db.query(func.count(JobApplication.id)).filter(
        JobApplication.status == ApplicationStatus.REJECTED
    ).scalar() or 0

    by_status_raw = db.query(
        JobApplication.status,
        func.count(JobApplication.id)
    ).group_by(JobApplication.status).all()

    by_status = {status.value: count for status, count in by_status_raw}

    return DashboardStats(
        total_applications=total,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        by_status=by_status
    )


# AI Tip Endpoint

@app.post("/ai-tip", response_model=AITipResponse)
def generate_resume_tip(request: AITipRequest):
    """Generate resume tips based on job description using Gemini API"""
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    bullet_points = get_resume_tips(request.job_description)
    return AITipResponse(bullet_points=bullet_points)

# ============================================================================
# MANGUM HANDLER FOR VERCEL
# ============================================================================
from mangum import Mangum

handler = Mangum(app)


# ============================================================================
# LOCAL DEVELOPMENT
# ============================================================================
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn server for local development...")
    uvicorn.run(
        "index:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
