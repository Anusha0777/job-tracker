from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from models import JobApplication, ApplicationStatus, get_db
from ai_helper import get_resume_tips
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


# Pydantic schemas for request/response validation
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
    by_status: dict  # e.g., {"Applied": 5, "Interview": 2, ...}


class AITipRequest(BaseModel):
    job_description: str


class AITipResponse(BaseModel):
    bullet_points: list[str]


# CRUD Endpoints

@router.get("/applications", response_model=list[JobApplicationResponse])
def get_all_applications(db: Session = Depends(get_db)):
    """Get all job applications sorted by date (newest first)"""
    applications = db.query(JobApplication).order_by(
        JobApplication.application_date.desc()
    ).all()
    return applications


@router.post("/applications", response_model=JobApplicationResponse)
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


@router.patch("/applications/{app_id}", response_model=JobApplicationResponse)
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


@router.delete("/applications/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    """Delete a job application"""
    db_app = db.query(JobApplication).filter(JobApplication.id == app_id).first()

    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(db_app)
    db.commit()
    return {"message": "Application deleted successfully"}


# Stats Endpoint

@router.get("/stats", response_model=DashboardStats)
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

    # Count by status
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

@router.post("/ai-tip", response_model=AITipResponse)
def generate_resume_tip(request: AITipRequest):
    """Generate resume tips based on job description using Gemini API"""
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    bullet_points = get_resume_tips(request.job_description)
    return AITipResponse(bullet_points=bullet_points)
