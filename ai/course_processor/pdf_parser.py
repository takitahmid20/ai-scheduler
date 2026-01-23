"""
PDF Parser Utility
Extracts structured data from PDF course documents using pdfplumber
"""

import pdfplumber
import re
from typing import List, Dict, Any
from datetime import datetime


class PDFParser:
    """Parse PDF and extract tables using pdfplumber"""
    
    @staticmethod
    def parse_pdf(file_path: str) -> List[Dict[str, Any]]:
        """
        Extract course data from PDF file
        Returns list of course dictionaries with all fields
        """
        courses = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Extract table from page
                    tables = page.extract_tables()
                    
                    for table in tables:
                        if not table or len(table) < 2:
                            continue
                        
                        # First row is header
                        headers = table[0]
                        
                        # Process data rows
                        for row in table[1:]:
                            if not row or len(row) < 13:  # Should have at least 13 columns
                                continue
                            
                            # Skip empty rows
                            if not any(cell for cell in row if cell and str(cell).strip()):
                                continue
                            
                            # Map row to course dictionary
                            course = PDFParser._map_row_to_course(headers, row)
                            if course:
                                courses.append(course)
        
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            raise
        
        return courses
    
    @staticmethod
    def _map_row_to_course(headers: List, row: List) -> Dict[str, Any]:
        """Map table row to course dictionary"""
        try:
            # Create dictionary from headers and row
            course_data = {}
            
            # Handle the case where we know the column order
            # SL, Program, Course Code, Title, Section, Room1, Room2, Day1, Day2, Time1, Time2, Faculty Name, Faculty Initial, Credit
            
            if len(row) >= 13:
                course_data = {
                    'sl': str(row[0]).strip() if row[0] else '',
                    'program': str(row[1]).strip() if row[1] else '',
                    'course_code': str(row[2]).strip() if row[2] else '',
                    'title': str(row[3]).strip() if row[3] else '',
                    'section': str(row[4]).strip() if row[4] else '',
                    'room1': str(row[5]).strip() if row[5] else '',
                    'room2': str(row[6]).strip() if row[6] else '',
                    'day1': str(row[7]).strip() if row[7] else '',
                    'day2': str(row[8]).strip() if row[8] else '',
                    'time1': str(row[9]).strip() if row[9] else '',
                    'time2': str(row[10]).strip() if row[10] else '',
                    'faculty_name': str(row[11]).strip() if row[11] else '',
                    'faculty_initial': str(row[12]).strip() if row[12] else '',
                    'credit': str(row[13]).strip() if len(row) > 13 and row[13] else '0'
                }
                
                # Skip if course_code is empty
                if not course_data['course_code']:
                    return None
                
                return course_data
            
            return None
            
        except Exception as e:
            print(f"Error mapping row: {e}")
            return None


class CourseExtractor:
    """Extract and process course details"""
    
    @staticmethod
    def detect_course_type(course_data: Dict[str, Any]) -> str:
        """
        Detect if course is Lab (L) or Theory (T)
        Based on: duration, course code, title, room
        """
        # Check time duration
        time1 = course_data.get('time1', '')
        if time1:
            duration = CourseExtractor._calculate_duration(time1)
            # Lab courses are typically 160 minutes (2 hours 40 min)
            # Theory courses are typically 80 minutes (1 hour 20 min)
            if duration >= 150:  # Allow some tolerance
                return 'L'
        
        # Check course code for "LAB" keyword
        course_code = course_data.get('course_code', '').upper()
        if 'LAB' in course_code:
            return 'L'
        
        # Check title for lab keywords
        title = course_data.get('title', '').upper()
        if 'LAB' in title or 'LABORATORY' in title:
            return 'L'
        
        # Check room for lab indication
        room1 = course_data.get('room1', '').upper()
        room2 = course_data.get('room2', '').upper()
        if 'LAB' in room1 or 'LAB' in room2:
            return 'L'
        
        # Default to Theory
        return 'T'
    
    @staticmethod
    def _calculate_duration(time_str: str) -> int:
        """Calculate duration in minutes from time string like '08:30 AM - 09:50 AM'"""
        try:
            # Parse time string
            parts = time_str.split('-')
            if len(parts) != 2:
                return 0
            
            # Normalize time format: "08:30:AM" or "02:00:PM" -> "08:30 AM" or "02:00 PM"
            start_str = parts[0].strip().replace(':AM', ' AM').replace(':PM', ' PM')
            end_str = parts[1].strip().replace(':AM', ' AM').replace(':PM', ' PM')
            
            # Convert to datetime
            start = datetime.strptime(start_str, '%I:%M %p')
            end = datetime.strptime(end_str, '%I:%M %p')
            
            # Calculate difference in minutes
            duration = (end - start).total_seconds() / 60
            return int(duration)
            
        except Exception as e:
            # Silently return default duration to avoid log spam
            return 80
    
    @staticmethod
    def validate_course_data(course_data: Dict[str, Any]) -> bool:
        """Validate that required fields exist"""
        required_fields = ['course_code', 'title', 'section']
        return all(course_data.get(field) for field in required_fields)
    
    @staticmethod
    def clean_course_data(course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and normalize course data"""
        # Remove None values
        cleaned = {k: v for k, v in course_data.items() if v is not None}
        
        # Convert credit to integer
        try:
            cleaned['credit'] = int(cleaned.get('credit', 0))
        except (ValueError, TypeError):
            cleaned['credit'] = 0
        
        # Detect course type
        cleaned['course_type'] = CourseExtractor.detect_course_type(course_data)
        
        return cleaned
