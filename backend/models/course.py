"""
Course Model
Database model for course information
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True, nullable=False)
    course_title = Column(String, nullable=False)
    credits = Column(Float, nullable=False)
    department = Column(String, index=True, nullable=False)
    trimester = Column(String, nullable=False)
    
    # Additional course details
    prerequisites = Column(String, nullable=True)  # Comma-separated course codes
    faculty = Column(String, nullable=True)
    sections = Column(String, nullable=True)  # JSON string with section details
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Course {self.course_code}>"
