"""
Core modules for AI Academic Scheduler
Contains authentication, data processing, and scheduling logic
"""

from .auth import register_user, authenticate_user, get_user_by_email, update_user_profile
from .data_processor import (
    parse_csv_file, parse_pdf_file, 
    normalize_course_data, normalize_faculty_data, 
    normalize_timeslot_data, normalize_exam_data,
    save_processed_data, load_processed_data, validate_uploaded_data
)
from .scheduler import ScheduleGenerator, optimize_schedule

__all__ = [
    'register_user', 'authenticate_user', 'get_user_by_email', 'update_user_profile',
    'parse_csv_file', 'parse_pdf_file',
    'normalize_course_data', 'normalize_faculty_data',
    'normalize_timeslot_data', 'normalize_exam_data',
    'save_processed_data', 'load_processed_data', 'validate_uploaded_data',
    'ScheduleGenerator', 'optimize_schedule'
]
