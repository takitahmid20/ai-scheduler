"""
Integration Layer - Connects AI modules with backend services
Provides high-level API for UI/backend to use AI functionality
"""

from ai.course_processor import CourseProcessor
from ai.schedule_generator import ScheduleGenerator
from ai.optimization import ScheduleOptimizer
from ai.models import Schedule, UserPreferences, Course


class AIScheduleEngine:
    """Main AI engine for schedule generation"""
    
    def __init__(self):
        self.course_processor = CourseProcessor()
        self.schedule_generator = ScheduleGenerator([])
        self.optimizer = ScheduleOptimizer()
        self.processed_courses = []
    
    def process_course_data(self, pdf_file_path: str, department: str) -> dict:
        result = self.course_processor.process_pdf(pdf_file_path)
        if result['success']:
            self.processed_courses.extend(result['courses'])
        return result
    
    def generate_student_schedules(
        self, 
        student_courses: list, 
        user_preferences: UserPreferences,
        num_options: int = 3
    ) -> list:
        self.schedule_generator = ScheduleGenerator(student_courses, user_preferences.__dict__)
        raw_schedules = self.schedule_generator.generate_schedules(num_options)
        optimized_schedules = self.optimizer.rank_schedules(raw_schedules)
        return optimized_schedules
    
    def save_favorite_schedule(self, schedule_id: str) -> bool:
        return True
    
    def get_schedule_analysis(self, schedule: Schedule) -> dict:
        return {}
    
    def export_schedule(self, schedule: Schedule, format: str = 'pdf') -> str:
        return ""


# Singleton instance
_engine = None


def get_ai_engine() -> AIScheduleEngine:
    """Get or create AI engine singleton"""
    global _engine
    if _engine is None:
        _engine = AIScheduleEngine()
    return _engine
