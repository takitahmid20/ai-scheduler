"""
AI Module - Core AI/ML functionality for Academic Scheduler
Handles course processing, schedule generation, and optimization
"""

# Optional imports - only needed for PDF parsing (admin feature)
try:
    from .course_processor.pdf_parser import PDFParser, CourseExtractor
except ImportError:
    # pdfplumber not installed - PDF upload will be disabled
    PDFParser = None
    CourseExtractor = None

__all__ = ['PDFParser', 'CourseExtractor']
