"""
Schedule Model
Database model for generated schedules
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from ..database import Base

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Schedule details
    trimester = Column(String, nullable=False)
    selected_courses = Column(Text, nullable=False)  # JSON string
    completed_courses = Column(Text, nullable=True)  # JSON string
    
    # Generated schedule data
    schedule_data = Column(Text, nullable=False)  # JSON string with full schedule
    conflicts = Column(Text, nullable=True)  # JSON string with detected conflicts
    
    is_favorite = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Schedule user={self.user_id} trimester={self.trimester}>"
