"""
Data Models for AI/ML Components
Standardized data structures for courses, schedules, and constraints
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import time


@dataclass
class TimeSlot:
    """Represents a time slot for a class"""
    day: str
    start_time: str
    end_time: str
    slot_index: int


@dataclass
class Course:
    """Represents a single course"""
    code: str
    name: str
    credits: float
    department: str
    section: str
    instructor: str
    room: str
    course_type: str  # "Theory" or "Lab"
    time_slots: List[TimeSlot] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    max_capacity: int = 0
    enrolled_students: int = 0
    
    def has_conflict_with(self, other: 'Course') -> bool:
        """Check if this course has time conflict with another"""
        pass


@dataclass
class Schedule:
    """Represents a complete student schedule"""
    schedule_id: str
    student_id: str
    courses: List[Course] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    free_days: int = 0
    workload_balance: float = 0.0
    total_credits: float = 0.0
    score: float = 0.0
    is_favorite: bool = False
    
    def add_course(self, course: Course) -> bool:
        """Add course to schedule, return False if conflict"""
        pass
    
    def remove_course(self, course_code: str) -> bool:
        """Remove course from schedule"""
        pass
    
    def get_daily_schedule(self, day: str) -> List[Course]:
        """Get all courses for a specific day"""
        pass


@dataclass
class UserPreferences:
    """Represents user scheduling preferences"""
    student_id: str
    preferred_instructors: List[str] = field(default_factory=list)
    avoided_instructors: List[str] = field(default_factory=list)
    preferred_times: List[str] = field(default_factory=list)  # "morning", "afternoon", "evening"
    max_daily_hours: float = 8.0
    max_consecutive_hours: float = 4.0
    min_break_between_classes: int = 15  # minutes
    prefer_early_finish: bool = False
    prefer_few_days: bool = False
    allow_gaps_between_classes: bool = True


@dataclass
class ConflictReport:
    """Detailed conflict information"""
    conflict_type: str
    course1_code: str
    course2_code: str
    severity: str  # "critical", "warning", "info"
    description: str
    affected_courses: List[str] = field(default_factory=list)


@dataclass
class ScheduleAnalysis:
    """Analysis results for a schedule"""
    schedule_id: str
    total_conflicts: int = 0
    free_days: int = 0
    daily_workload: Dict[str, float] = field(default_factory=dict)  # day -> hours
    conflict_reports: List[ConflictReport] = field(default_factory=list)
    optimization_score: float = 0.0
    recommendations: List[str] = field(default_factory=list)
