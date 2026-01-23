"""
Course List Model
Master list of all unique courses
"""

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from ..database import Base

class CourseList(Base):
    __tablename__ = "course_list"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True, nullable=False)  # e.g., "CSE101"
    title = Column(String, nullable=False)  # Course title
    credit = Column(Float, nullable=True)  # Credit hours
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<CourseList {self.course_code} - {self.title}>"
