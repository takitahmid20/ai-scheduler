"""
AI Module - Core AI/ML functionality for Academic Scheduler
Handles course processing, schedule generation, and optimization
"""

from .course_processor.pdf_parser import PDFParser, CourseExtractor

__all__ = ['PDFParser', 'CourseExtractor']
