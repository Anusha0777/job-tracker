from sqlalchemy import Column, Integer, String, DateTime, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from enum import Enum as PyEnum
import os

DATABASE_URL = "sqlite:///./job_tracker.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
