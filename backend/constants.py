"""
Static Data & Constants
Reference data that rarely changes, used across the application
"""

# Academic Departments
DEPARTMENTS = [
"Computer Science and Engineering",
"Electrical and Electronic Engineering",
"Civil Engineering",
"Data Science",
"Business Administration",
"Accounting and Information Systems",
"Economics",
"English",
"Environment and Development Studies",
"Media Studies and Journalism",
"Pharmacy",
"Biotechnology and Genetic Engineering",
"Natural Sciences",
]

# Trimesters/Semesters
TRIMESTERS = [
    "Spring",
    "Summer", 
    "Fall"
]

# Academic Years
ACADEMIC_YEARS = [
    "2024-2025",
    "2025-2026",
    "2026-2027",
    "2027-2028"
]

# Student Year Levels
YEAR_LEVELS = [
    "1st Year",
    "2nd Year",
    "3rd Year",
    "4th Year",
    "Masters",
    "PhD"
]

# Days of Week
WEEKDAYS = [
    "Saturday",
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

# Time Slots (Theory Classes - 80 minutes each)
TIME_SLOTS = [
    "08:30 AM - 09:50 AM",
    "09:51 AM - 11:10 AM",
    "11:11 AM - 12:30 PM",
    "12:31 PM - 01:50 PM",
    "01:51 PM - 03:10 PM",
    "03:11 PM - 04:30 PM"
]

# Lab Time Slots (Combining 2 theory slots - 160 minutes each)
LAB_TIME_SLOTS = [
    "08:30 AM - 11:10 AM",  # Slot 1 + 2
    "09:51 AM - 12:30 PM",  # Slot 2 + 3
    "11:11 AM - 01:50 PM",  # Slot 3 + 4
    "12:31 PM - 03:10 PM",  # Slot 4 + 5
    "01:51 PM - 04:30 PM"   # Slot 5 + 6
]

# Course Types
COURSE_TYPES = [
    "Theory",
    "Lab"
]

# Credit Hours
CREDIT_OPTIONS = [
    1.0, 2.0, 3.0
]

# Section Names
SECTION_NAMES = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"
]









# Priority Levels for Scheduling
PRIORITY_LEVELS = [
    "High",
    "Medium", 
    "Low"
]

# Conflict Types
CONFLICT_TYPES = [
    "Time Overlap",
    "Prerequisite Not Met",
    "Instructor Unavailable",
    "Maximum Credit Exceeded"
]

# Helper Functions
def get_department_prefix(department: str) -> list:
    """Get common course prefixes for a department"""
    return COURSE_PREFIXES.get(department, [])

def get_time_range(start_time: str, duration_minutes: int = 90) -> str:
    """
    Get formatted time range
    Example: get_time_range("09:00", 90) -> "09:00 - 10:30"
    """
    from datetime import datetime, timedelta
    start = datetime.strptime(start_time, "%H:%M")
    end = start + timedelta(minutes=duration_minutes)
    return f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"

def validate_department(department: str) -> bool:
    """Check if department exists"""
    return department in DEPARTMENTS

def validate_trimester(trimester: str) -> bool:
    """Check if trimester is valid"""
    return trimester in TRIMESTERS
