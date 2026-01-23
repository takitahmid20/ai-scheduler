"""
Semester Model
Database model for academic semesters
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Semester(Base):
    __tablename__ = "semesters"
    
    id = Column(Integer, primary_key=True, index=True)
    semester_name = Column(String, nullable=False)  # Summer, Fall, Spring
    year = Column(Integer, nullable=False)
    program = Column(String, nullable=False)  # BSCSE, BSDS
    
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(Integer, nullable=True)  # admin user_id
    
    # Relationship to course offerings
    course_offerings = relationship("CourseOffering", back_populates="semester", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Semester {self.semester_name} {self.year} - {self.program}>"
