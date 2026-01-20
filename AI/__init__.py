"""
AI Module - Core AI/ML functionality for Academic Scheduler
Handles course processing, schedule generation, and optimization
"""

from ai.course_processor import CourseProcessor
from ai.schedule_generator import ScheduleGenerator
from ai.optimization import ScheduleOptimizer

__all__ = [
    'CourseProcessor',
    'ScheduleGenerator',
    'ScheduleOptimizer',
]
