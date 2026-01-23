"""
Course Offering Model
Database model for course offerings from uploaded PDFs
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base


class CourseOffering(Base):
    __tablename__ = "course_offerings"
    
    id = Column(Integer, primary_key=True, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    
    # Course details
    program = Column(String, nullable=False)  # BSCSE, BSDS
    course_code = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    section = Column(String, nullable=False)
    course_type = Column(String, nullable=False)  # L (Lab) or T (Theory)
    credit = Column(Integer, nullable=False)
    
    # Schedule details
    day1 = Column(String, nullable=True)  # Sat, Sun, Mon, Tue, Wed, Thu, Fri
    day2 = Column(String, nullable=True)
    time1 = Column(String, nullable=True)  # "08:30 AM - 09:50 AM"
    time2 = Column(String, nullable=True)
    
    # Room details (metadata only)
    room1 = Column(String, nullable=True)
    room2 = Column(String, nullable=True)
    
    # Faculty details
    faculty_name = Column(String, nullable=True)
    faculty_initial = Column(String, nullable=True)
    
    # Additional metadata
    notes = Column(Text, nullable=True)  # For "TBA", "If Required", etc.
    
    # Relationship to semester
    semester = relationship("Semester", back_populates="course_offerings")
    
    def __repr__(self):
        return f"<CourseOffering {self.course_code}-{self.section}>"
