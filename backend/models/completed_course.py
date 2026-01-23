"""
Completed Course Model
Stores courses that a student has already completed
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class CompletedCourse(Base):
    __tablename__ = "completed_courses"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True, nullable=False)  # Student's ID
    course_code = Column(String, nullable=False)  # e.g., "CSE101", "MAT201"
    program = Column(String, nullable=False)  # e.g., "BSCSE", "BSDS"
    
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<CompletedCourse {self.student_id} - {self.course_code}>"
