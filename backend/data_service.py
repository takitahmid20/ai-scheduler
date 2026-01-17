"""
Data Service
Provides access to static data and reference information
Can be extended to fetch data from database if needed
"""

from .constants import (
    DEPARTMENTS, TRIMESTERS, ACADEMIC_YEARS, YEAR_LEVELS,
    WEEKDAYS, TIME_SLOTS, LAB_TIME_SLOTS, COURSE_TYPES, CREDIT_OPTIONS,
    SECTION_NAMES, ROOM_TYPES, GRADE_OPTIONS, INSTRUCTOR_TITLES,
    COURSE_PREFIXES, PRIORITY_LEVELS, CONFLICT_TYPES,
    get_department_prefix, get_time_range, validate_department, validate_trimester
)

class DataService:
    """Service to access static/reference data"""
    
    @staticmethod
    def get_departments():
        """Get list of all departments"""
        return DEPARTMENTS
    
    @staticmethod
    def get_trimesters():
        """Get list of trimesters/semesters"""
        return TRIMESTERS
    
    @staticmethod
    def get_academic_years():
        """Get list of academic years"""
        return ACADEMIC_YEARS
    
    @staticmethod
    def get_year_levels():
        """Get list of student year levels"""
        return YEAR_LEVELS
    
    @staticmethod
    def get_weekdays():
        """Get list of weekdays"""
        return WEEKDAYS
    
    @staticmethod
    def get_time_slots():
        """Get list of available time slots for theory classes"""
        return TIME_SLOTS
    
    @staticmethod
    def get_lab_time_slots():
        """Get list of available time slots for lab classes (2 hours 40 minutes)"""
        return LAB_TIME_SLOTS
    
    @staticmethod
    def get_course_types():
        """Get list of course types"""
        return COURSE_TYPES
    
    @staticmethod
    def get_credit_options():
        """Get list of credit hour options"""
        return CREDIT_OPTIONS
    
    @staticmethod
    def get_sections():
        """Get list of section names"""
        return SECTION_NAMES
    
    @staticmethod
    def get_room_types():
        """Get list of room types"""
        return ROOM_TYPES
    
    @staticmethod
    def get_grades():
        """Get list of grade options"""
        return GRADE_OPTIONS
    
    @staticmethod
    def get_instructor_titles():
        """Get list of instructor titles"""
        return INSTRUCTOR_TITLES
    
    @staticmethod
    def get_course_prefixes(department: str = None):
        """
        Get course prefixes
        If department provided, returns prefixes for that department
        Otherwise returns all prefixes
        """
        if department:
            return get_department_prefix(department)
        return COURSE_PREFIXES
    
    @staticmethod
    def get_priority_levels():
        """Get list of priority levels"""
        return PRIORITY_LEVELS
    
    @staticmethod
    def get_conflict_types():
        """Get list of conflict types"""
        return CONFLICT_TYPES
    
    @staticmethod
    def format_time_range(start_time: str, duration_minutes: int = 90):
        """
        Format time range string
        Example: "09:00" + 90 minutes -> "09:00 - 10:30"
        """
        return get_time_range(start_time, duration_minutes)
    
    @staticmethod
    def is_valid_department(department: str):
        """Validate department name"""
        return validate_department(department)
    
    @staticmethod
    def is_valid_trimester(trimester: str):
        """Validate trimester name"""
        return validate_trimester(trimester)
    
    @staticmethod
    def get_dropdown_options(data_type: str):
        """
        Generic method to get dropdown options by type
        
        Args:
            data_type: One of ['departments', 'trimesters', 'years', 
                               'year_levels', 'weekdays', 'time_slots', 
                               'course_types', 'credits', 'sections', 
                               'room_types', 'grades', 'titles', 'priorities']
        
        Returns:
            List of options for dropdown
        """
        mappings = {
            'departments': DEPARTMENTS,
            'lab_time_slots': LAB_TIME_SLOTS,
            'trimesters': TRIMESTERS,
            'years': ACADEMIC_YEARS,
            'year_levels': YEAR_LEVELS,
            'weekdays': WEEKDAYS,
            'time_slots': TIME_SLOTS,
            'course_types': COURSE_TYPES,
            'credits': CREDIT_OPTIONS,
            'sections': SECTION_NAMES,
            'room_types': ROOM_TYPES,
            'grades': GRADE_OPTIONS,
            'titles': INSTRUCTOR_TITLES,
            'priorities': PRIORITY_LEVELS
        }
        return mappings.get(data_type, [])
