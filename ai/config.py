"""
Configuration for AI/ML Components
Settings and parameters for AI algorithms
"""

# Course Processing Settings
COURSE_PROCESSING_CONFIG = {
    'max_file_size': 10 * 1024 * 1024,  # 10 MB
    'supported_formats': ['pdf'],
    'extract_methods': ['ocr', 'text_extraction', 'table_parsing'],
}

# Schedule Generation Settings
SCHEDULE_GENERATION_CONFIG = {
    'max_schedule_options': 5,
    'max_courses_per_schedule': 10,
    'min_courses_per_schedule': 3,
    'validation_strict': True,
}

# Optimization Settings
OPTIMIZATION_CONFIG = {
    # Genetic Algorithm parameters
    'population_size': 100,
    'generations': 50,
    'mutation_rate': 0.1,
    'crossover_rate': 0.8,
    'elite_size': 10,
    
    # Scoring weights (must sum to 1.0)
    'scoring_weights': {
        'no_conflicts': 0.4,
        'workload_balance': 0.25,
        'free_time_quality': 0.2,
        'preferences_match': 0.15,
    },
    
    # Constraints
    'max_daily_hours': 8.0,
    'max_consecutive_hours': 4.0,
    'min_break_minutes': 15,
}

# Time Slot Configuration
TIME_SLOT_CONFIG = {
    'class_days': ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'theory_slot_duration': 80,  # minutes
    'lab_slot_duration': 160,  # minutes (2 theory slots)
    'min_break_between_classes': 15,  # minutes
}

# Database Configuration
DATABASE_CONFIG = {
    'cache_courses': True,
    'cache_ttl': 3600,  # 1 hour
    'batch_size': 100,
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/ai.log',
}
