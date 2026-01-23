"""
Schedule Generator Module
Generates optimal schedules based on courses and constraints
"""

from .conflict_detector import ConflictDetector
from itertools import product
from typing import List, Dict, Any


class ScheduleGenerator:
    """Generate course schedules with conflict detection"""
    
    def __init__(self, courses_with_sections: List[Dict], user_preferences: dict = None):
        """
        Args:
            courses_with_sections: List of courses, each containing multiple sections
                                  Format: [{'code': 'CSE1111', 'sections': [...]}]
            user_preferences: Dict with preferences like max_free_days, avoid_early, etc.
        """
        self.courses = courses_with_sections
        self.user_preferences = user_preferences or {}
        self.detector = ConflictDetector()
    
    def generate_schedules(self, num_options: int = 5) -> List[Dict]:
        """
        Generate multiple valid schedule options
        Returns list of schedules, each with selected sections and stats
        """
        if not self.courses:
            return []
        
        # Get all section combinations
        all_sections = [course['sections'] for course in self.courses]
        
        # Generate all possible combinations (cartesian product)
        all_combinations = list(product(*all_sections))
        
        print(f"Total combinations to check: {len(all_combinations)}")
        
        # Filter out conflicting schedules
        valid_schedules = []
        for combination in all_combinations:
            if not self.has_conflict(list(combination)):
                schedule = {
                    'sections': list(combination),
                    'courses': self.courses,
                    'stats': self.calculate_stats(list(combination))
                }
                valid_schedules.append(schedule)
                
                # Stop if we have enough options
                if len(valid_schedules) >= num_options * 3:  # Get extra for scoring
                    break
        
        print(f"Found {len(valid_schedules)} valid schedules")
        
        if not valid_schedules:
            return []
        
        # Score and rank schedules
        scored_schedules = self.score_schedules(valid_schedules)
        
        # Return top N
        return scored_schedules[:num_options]
    
    def has_conflict(self, sections: List[Dict]) -> bool:
        """Check if a combination of sections has time conflicts"""
        # Check each pair of sections
        for i in range(len(sections)):
            for j in range(i + 1, len(sections)):
                if self.detector.detect_time_overlap(sections[i], sections[j]):
                    return True
        return False
    
    def get_free_days(self, sections: List[Dict]) -> int:
        """Count number of free days in schedule"""
        all_days = {'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}
        used_days = set()
        
        for section in sections:
            days = self.detector.get_days_list(section)
            used_days.update(days)
        
        free_days = len(all_days - used_days)
        return free_days
    
    def calculate_stats(self, sections: List[Dict]) -> Dict:
        """Calculate statistics for a schedule"""
        free_days = self.get_free_days(sections)
        
        # Count total credits
        total_credits = sum(section.get('credit', 0) for section in sections)
        
        # Count days with classes
        all_days = set()
        for section in sections:
            days = self.detector.get_days_list(section)
            all_days.update(days)
        
        days_with_classes = len(all_days)
        
        return {
            'free_days': free_days,
            'total_credits': total_credits,
            'days_with_classes': days_with_classes,
            'total_courses': len(sections)
        }
    
    def score_schedules(self, schedules: List[Dict]) -> List[Dict]:
        """Score and rank schedules based on preferences"""
        for schedule in schedules:
            score = 0
            stats = schedule['stats']
            
            # Reward free days if preference is set
            if self.user_preferences.get('max_free_days', False):
                score += stats['free_days'] * 10
            
            # Penalty for early classes if preference is set
            if self.user_preferences.get('avoid_early', False):
                early_count = self.count_early_classes(schedule['sections'])
                score -= early_count * 5
            
            # Penalty for late classes if preference is set
            if self.user_preferences.get('avoid_late', False):
                late_count = self.count_late_classes(schedule['sections'])
                score -= late_count * 5
            
            # Bonus for balanced schedule (not too many classes per day)
            score += (7 - stats['days_with_classes']) * 3
            
            schedule['score'] = score
        
        # Sort by score (highest first)
        schedules.sort(key=lambda x: x['score'], reverse=True)
        
        return schedules
    
    def count_early_classes(self, sections: List[Dict]) -> int:
        """Count classes starting before 9 AM"""
        count = 0
        for section in sections:
            time_str = section.get('time1', '')
            start, _ = self.detector.parse_time(time_str)
            if start > 0 and start < 9 * 60:  # Before 9 AM
                count += 1
        return count
    
    def count_late_classes(self, sections: List[Dict]) -> int:
        """Count classes ending after 5 PM"""
        count = 0
        for section in sections:
            time_str = section.get('time1', '')
            _, end = self.detector.parse_time(time_str)
            if end > 17 * 60:  # After 5 PM
                count += 1
        return count
    
    def apply_constraints(self, schedules: List[Dict]) -> List[Dict]:
        """Apply additional constraints to filter schedules"""
        # Already handled in generate_schedules
        return schedules
