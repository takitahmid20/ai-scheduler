"""
Conflict Detection Engine
Identifies and analyzes scheduling conflicts
"""

from enum import Enum
from datetime import datetime
from typing import List, Tuple


class ConflictType(Enum):
    """Types of scheduling conflicts"""
    TIME_OVERLAP = "time_overlap"
    SAME_TIMESLOT = "same_timeslot"
    PREREQUISITE = "prerequisite"
    INVALID_SCHEDULE = "invalid_schedule"


class ConflictDetector:
    """Detect scheduling conflicts"""
    
    @staticmethod
    def parse_time(time_str: str) -> Tuple[int, int]:
        """
        Parse time string like '08:30 AM - 09:50 AM' or '08:30:AM - 09:50:AM' and return start/end minutes from midnight
        Returns: (start_minutes, end_minutes)
        """
        if not time_str or time_str.strip() == '' or time_str.strip() == '-':
            return (0, 0)
        
        try:
            parts = time_str.split('-')
            if len(parts) != 2:
                return (0, 0)
            
            start_str = parts[0].strip()
            end_str = parts[1].strip()
            
            # Handle both formats: "08:30 AM" and "08:30:AM"
            # Add space before AM/PM if missing
            if ':AM' in start_str:
                start_str = start_str.replace(':AM', ' AM')
            if ':PM' in start_str:
                start_str = start_str.replace(':PM', ' PM')
            if ':AM' in end_str:
                end_str = end_str.replace(':AM', ' AM')
            if ':PM' in end_str:
                end_str = end_str.replace(':PM', ' PM')
            
            # Parse start time
            start_time = datetime.strptime(start_str, '%I:%M %p')
            start_minutes = start_time.hour * 60 + start_time.minute
            
            # Parse end time
            end_time = datetime.strptime(end_str, '%I:%M %p')
            end_minutes = end_time.hour * 60 + end_time.minute
            
            return (start_minutes, end_minutes)
        except Exception as e:
            # Silently return (0, 0) for invalid times
            return (0, 0)
    
    @staticmethod
    def times_overlap(time1_str: str, time2_str: str) -> bool:
        """Check if two time ranges overlap"""
        start1, end1 = ConflictDetector.parse_time(time1_str)
        start2, end2 = ConflictDetector.parse_time(time2_str)
        
        # If either time is invalid, no overlap
        if start1 == 0 and end1 == 0:
            return False
        if start2 == 0 and end2 == 0:
            return False
        
        # Check overlap: times overlap if one starts before the other ends
        return start1 < end2 and start2 < end1
    
    @staticmethod
    def get_days_list(offering: dict) -> List[str]:
        """Get list of days a course meets"""
        days = []
        if offering.get('day1'):
            days.append(offering['day1'].strip())
        if offering.get('day2'):
            days.append(offering['day2'].strip())
        return days
    
    @staticmethod
    def detect_time_overlap(offering1: dict, offering2: dict) -> bool:
        """
        Check if two course offerings have time overlap
        Returns True if they conflict
        """
        # Get days for both courses
        days1 = ConflictDetector.get_days_list(offering1)
        days2 = ConflictDetector.get_days_list(offering2)
        
        # Check if they share any common day
        common_days = set(days1) & set(days2)
        if not common_days:
            return False  # No common days, no conflict
        
        # They share at least one day, check time overlap
        time1 = offering1.get('time1', '')
        time2 = offering2.get('time2', '')
        
        # Check if times overlap
        if ConflictDetector.times_overlap(time1, time2):
            return True
        
        # Also check time2 fields if present
        time1_alt = offering1.get('time2', '')
        time2_alt = offering2.get('time1', '')
        
        if time1_alt and time2_alt:
            if ConflictDetector.times_overlap(time1_alt, time2_alt):
                return True
        
        return False
    
    @staticmethod
    def validate_timeslot(day: str, time_str: str) -> bool:
        """Validate that a timeslot is reasonable"""
        if not day or not time_str:
            return False
        
        # Valid days
        valid_days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
                      'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        
        if day not in valid_days:
            return False
        
        # Try to parse time
        start, end = ConflictDetector.parse_time(time_str)
        
        # Check if time is valid (between 7 AM and 10 PM)
        if start < 7 * 60 or end > 22 * 60:
            return False
        
        # Check if duration is reasonable (30 min to 4 hours)
        duration = end - start
        if duration < 30 or duration > 240:
            return False
        
        return True
    
    @staticmethod
    def check_prerequisites(course: dict, taken_courses: List[str]) -> bool:
        """
        Check if prerequisites are met
        For now, just returns True (no prerequisite data in database yet)
        """
        # TODO: Implement when prerequisite data is available
        return True
    
    @staticmethod
    def get_conflict_details(conflict_type: ConflictType, details: dict) -> str:
        """Generate human-readable conflict description"""
        if conflict_type == ConflictType.TIME_OVERLAP:
            return f"Time conflict: {details.get('course1', 'Course 1')} and {details.get('course2', 'Course 2')} overlap on {details.get('day', 'same day')}"
        elif conflict_type == ConflictType.SAME_TIMESLOT:
            return f"Same timeslot conflict: Both courses scheduled at {details.get('time', 'same time')}"
        elif conflict_type == ConflictType.PREREQUISITE:
            return f"Prerequisite not met: {details.get('course', 'Course')} requires {details.get('prerequisite', 'prerequisite')}"
        else:
            return "Invalid schedule configuration"

