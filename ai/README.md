# AI Academic Scheduler - AI Module

Organized AI/ML components for course processing, schedule generation, and optimization.

## Directory Structure

```
ai/
├── __init__.py                 # Module exports
├── config.py                   # Configuration and parameters
├── engine.py                   # Main AI orchestration engine
│
├── course_processor/           # PDF parsing & course extraction
│   ├── __init__.py            # CourseProcessor class
│   └── pdf_parser.py          # PDF utilities
│
├── schedule_generator/         # Schedule generation & conflict detection
│   ├── __init__.py            # ScheduleGenerator class
│   └── conflict_detector.py   # Conflict detection engine
│
├── optimization/              # Schedule optimization & ranking
│   ├── __init__.py            # ScheduleOptimizer class
│   └── genetic_algorithm.py   # GA-based optimization
│
└── models/                    # Data structures & models
    └── __init__.py            # Dataclasses for courses, schedules, etc.
```

## Module Descriptions

### 1. **course_processor/**
Handles PDF file processing and course data extraction.

**Key Classes:**
- `CourseProcessor`: Main processor for extracting courses from PDFs
- `PDFParser`: Utilities for PDF text/table extraction
- `CourseExtractor`: Extracts structured course info from text

**Responsibilities:**
- Parse PDF course documents
- Extract course details (code, name, credits, faculty, schedule)
- Validate extracted data
- Store courses in database

### 2. **schedule_generator/**
Generates valid course schedules with conflict detection.

**Key Classes:**
- `ScheduleGenerator`: Creates schedule combinations
- `ConflictDetector`: Identifies scheduling conflicts

**Responsibilities:**
- Generate multiple schedule options
- Detect time conflicts
- Apply constraints
- Calculate free days/workload

### 3. **optimization/**
Optimizes schedules based on various criteria.

**Key Classes:**
- `ScheduleOptimizer`: Main optimizer
- `GeneticScheduleOptimizer`: Evolutionary algorithm for optimization

**Responsibilities:**
- Score schedules
- Rank schedules by preference
- Balance workload
- Apply genetic algorithms

### 4. **models/**
Data structures for AI components.

**Key Classes:**
- `Course`: Represents a single course
- `Schedule`: Represents complete student schedule
- `UserPreferences`: Student scheduling preferences
- `ConflictReport`: Conflict information
- `ScheduleAnalysis`: Schedule analysis results

## Usage Example

```python
from ai import AIScheduleEngine
from ai.models import UserPreferences

# Get AI engine
engine = AIScheduleEngine()

# Step 1: Process course PDF
result = engine.process_course_data('courses.pdf', 'Computer Science')

# Step 2: Generate schedules
preferences = UserPreferences(
    student_id='STU001',
    preferred_times=['morning', 'afternoon'],
    max_daily_hours=6.0
)

courses = [...]  # Student selected courses
schedules = engine.generate_student_schedules(courses, preferences, num_options=3)

# Step 3: Export schedule
for schedule in schedules:
    engine.export_schedule(schedule, format='pdf')
```

## Configuration

Edit `config.py` to adjust:
- GA parameters (population size, generations)
- Scoring weights
- Time slot constraints
- Database caching

## Integration with Backend

The AI module integrates with backend services:
- `backend/database.py`: Stores/retrieves courses and schedules
- `backend/services/`: May use AI engine for API endpoints
- `pages/upload.py`: Triggers course processing via AI engine
- `pages/results.py`: Displays AI-generated schedules

## TODO - Implementation Priority

1. **Phase 1: Core Data Models**
   - Implement dataclasses in `models/__init__.py`
   - Create database schemas for courses/schedules

2. **Phase 2: Course Processing**
   - Implement PDF parsing utilities
   - Build course extraction logic
   - Add validation

3. **Phase 3: Schedule Generation**
   - Implement basic schedule generation
   - Add conflict detection
   - Generate multiple options

4. **Phase 4: Optimization**
   - Implement scoring system
   - Add genetic algorithm
   - Rank schedules

5. **Phase 5: Integration**
   - Connect with backend services
   - Add API endpoints
   - Test end-to-end flow

## Dependencies

Will need:
- `PyPDF2` or `pdfplumber` - PDF parsing
- `numpy` - Numerical operations
- `scikit-learn` - ML utilities (optional)
- `sqlalchemy` - Database ORM (already in project)

## Testing

Create `tests/test_ai/` with:
- `test_course_processor.py`
- `test_schedule_generator.py`
- `test_optimization.py`
- `test_models.py`
