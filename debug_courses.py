from backend.database import SessionLocal
from backend.models import CourseOffering, CompletedCourse, Semester
from sqlalchemy import distinct

db = SessionLocal()

# Check total unique courses in database
total_courses = db.query(distinct(CourseOffering.course_code)).count()
print(f'\n=== TOTAL UNIQUE COURSES IN DATABASE: {total_courses} ===\n')

# Check courses per semester/program
semesters = db.query(Semester).all()
print('=== COURSES PER SEMESTER/PROGRAM ===')
for sem in semesters:
    offerings = db.query(CourseOffering).filter(
        CourseOffering.semester_id == sem.id,
        CourseOffering.program == sem.program
    ).all()
    
    unique_codes = set(o.course_code for o in offerings)
    print(f'{sem.semester_name} {sem.year} - {sem.program}:')
    print(f'  Total offerings: {len(offerings)}')
    print(f'  Unique courses: {len(unique_codes)}')
    print()

# Check completed courses (assuming there's a student)
completed_all = db.query(CompletedCourse).all()
print(f'=== COMPLETED COURSES (ALL STUDENTS): {len(completed_all)} ===')
for comp in completed_all[:10]:  # Show first 10
    print(f'  Student {comp.student_id}: {comp.course_code}')

db.close()
