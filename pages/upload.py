from nicegui import ui, app
from backend.constants import DEPARTMENTS
from backend.database import SessionLocal
from backend.models import Semester, CourseOffering, CompletedCourse
from sqlalchemy import distinct
from components import (
    create_header, create_footer, create_primary_button
)


def get_available_semesters():
    """Get list of semesters that have course offerings"""
    db = SessionLocal()
    try:
        semesters = db.query(Semester).order_by(Semester.year.desc(), Semester.semester_name).all()
        return [(f"{s.semester_name} {s.year}", s.id, s.program) for s in semesters]
    finally:
        db.close()


def get_available_programs():
    """Get distinct programs from course offerings"""
    db = SessionLocal()
    try:
        programs = db.query(distinct(CourseOffering.program)).all()
        return [p[0] for p in programs if p[0]]
    finally:
        db.close()


def get_courses_by_semester_program(semester_id, program, exclude_completed=None):
    """
    Get all courses for a specific semester and program
    
    Args:
        semester_id: Semester ID to filter by
        program: Program name to filter by
        exclude_completed: Set of course codes to exclude (completed courses)
    """
    db = SessionLocal()
    try:
        offerings = db.query(CourseOffering).filter(
            CourseOffering.semester_id == semester_id,
            CourseOffering.program == program
        ).order_by(CourseOffering.course_code).all()
        
        # Group by course_code (same course, multiple sections)
        courses_dict = {}
        for offering in offerings:
            code = offering.course_code
            
            # Skip if this course is in the exclude list (completed courses)
            if exclude_completed and code in exclude_completed:
                continue
            
            if code not in courses_dict:
                courses_dict[code] = {
                    'code': code,
                    'title': offering.title,
                    'credit': offering.credit,
                    'sections': []
                }
            courses_dict[code]['sections'].append({
                'id': offering.id,
                'section': offering.section,
                'type': offering.course_type,
                'day1': offering.day1,
                'day2': offering.day2,
                'time1': offering.time1,
                'faculty': offering.faculty_name
            })
        
        return list(courses_dict.values())
    finally:
        db.close()


def get_completed_courses(student_id):
    """Get set of completed course codes for a student"""
    db = SessionLocal()
    try:
        completed = db.query(CompletedCourse.course_code).filter(
            CompletedCourse.student_id == student_id
        ).all()
        return {c[0] for c in completed}
    finally:
        db.close()

def upload_page():
    """Course selection page for students"""
    ui.colors(primary='#ff6900')
    
    # Check if user is logged in
    if not app.storage.user.get('logged_in', False):
        ui.notify('Please sign in to continue', type='warning')
        ui.navigate.to('/signin')
        return
    
    user_name = app.storage.user.get('full_name', 'Student')
    
    create_header('AI Academic Scheduler', user_name)
    
    # State variables
    selected_data = {
        'semester_id': None,
        'program': None,
        'courses': [],
        'selected_course_codes': []
    }
    
    courses_container_ref = {'container': None}
    
    # Main container with better width
    with ui.column().classes('w-full items-center p-8'):
        # Centered content container
        with ui.column().classes('w-full max-w-4xl gap-8'):
            # Page title
            with ui.column().classes('w-full gap-2 mb-4'):
                ui.label('Select Your Courses').classes('text-3xl font-bold text-gray-800')
                ui.label('Choose semester, program, and courses you want to register').classes('text-gray-600')
            
            # Semester & Program Selection Card
            with ui.card().classes('w-full p-8 shadow-lg'):
                ui.label('Semester & Program Selection').classes('text-xl font-semibold text-gray-800 mb-2')
                ui.label('Select the semester and your program to see available courses').classes('text-sm text-gray-500 mb-6')
                
                with ui.row().classes('w-full gap-4'):
                    # Semester dropdown
                    with ui.column().classes('flex-1 gap-2'):
                        ui.label('Select Semester').classes('text-sm font-medium text-gray-700')
                        
                        semester_options = get_available_semesters()
                        if not semester_options:
                            ui.label('No semesters available. Admin needs to upload course data first.').classes('text-sm text-orange-600')
                            semester_select = None
                        else:
                            semester_select = ui.select(
                                options=[s[0] for s in semester_options],
                                value=semester_options[0][0] if semester_options else None
                            ).classes('w-full')
                            
                            # Store semester_id mapping
                            semester_map = {s[0]: (s[1], s[2]) for s in semester_options}
                    
                    # Program dropdown
                    with ui.column().classes('flex-1 gap-2'):
                        ui.label('Select Program').classes('text-sm font-medium text-gray-700')
                        
                        programs = get_available_programs()
                        if not programs:
                            ui.label('No programs available').classes('text-sm text-orange-600')
                            program_select = None
                        else:
                            program_select = ui.select(
                                options=programs,
                                value=programs[0] if programs else None
                            ).classes('w-full')
                
                # Load courses button
                def load_courses_action():
                    if not semester_select or not program_select:
                        ui.notify('Please select semester and program', type='warning')
                        return
                    
                    semester_id, _ = semester_map[semester_select.value]
                    program = program_select.value
                    
                    # Store selection
                    selected_data['semester_id'] = semester_id
                    selected_data['program'] = program
                    
                    # Get student's completed courses
                    student_id = app.storage.user.get('student_id', '')
                    excluded_courses = get_completed_courses(student_id) if student_id else set()
                    
                    # Load courses (excluding completed ones)
                    courses = get_courses_by_semester_program(semester_id, program, excluded_courses)
                    selected_data['courses'] = courses
                    
                    if not courses:
                        ui.notify('No courses available for this semester/program', type='warning')
                        return
                    
                    # Get total courses for this semester (before exclusion)
                    all_semester_courses = get_courses_by_semester_program(semester_id, program, None)
                    
                    # Show info message if courses were excluded
                    if excluded_courses:
                        ui.notify(
                            f'Loaded {len(courses)} courses (excluding {len(excluded_courses)} completed). '
                            f'Total in semester: {len(all_semester_courses)}',
                            type='positive'
                        )
                    else:
                        ui.notify(f'Loaded {len(courses)} courses', type='positive')
                    
                    # Update courses display
                    display_courses(courses)
                
                ui.button('Load Available Courses', icon='refresh', on_click=load_courses_action).classes('mt-4').props('color=primary')

            # Course Selection Card
            with ui.card().classes('w-full p-8 shadow-lg'):
                ui.label('Course Selection').classes('text-xl font-semibold text-gray-800 mb-2')
                ui.label('Select courses you want to take this semester').classes('text-sm text-gray-500 mb-4')
                
                # Search box
                search_container = ui.row().classes('w-full gap-2 mb-4').style('display: none')
                with search_container:
                    search_input = ui.input('Search by course code or title...').classes('flex-1').props('outlined dense')
                    ui.button('Search', icon='search', on_click=lambda: filter_displayed_courses()).props('color=primary')
                    ui.button('Clear', icon='clear', on_click=lambda: clear_course_search()).props('outline')
                
                courses_container_ref['container'] = ui.column().classes('w-full gap-3')
                courses_container_ref['search_container'] = search_container
                courses_container_ref['search_input'] = search_input
                courses_container_ref['all_courses'] = []  # Store all courses for filtering
                
                with courses_container_ref['container']:
                    ui.label('Click "Load Available Courses" above to see courses').classes('text-sm text-gray-500 italic')
            
            def clear_course_search():
                """Clear search and show all courses"""
                courses_container_ref['search_input'].value = ''
                display_courses(courses_container_ref['all_courses'])
            
            def filter_displayed_courses():
                """Filter courses based on search"""
                search_term = courses_container_ref['search_input'].value.lower()
                all_courses = courses_container_ref['all_courses']
                
                if not search_term:
                    display_courses(all_courses)
                    return
                
                # Filter courses
                filtered = [
                    course for course in all_courses
                    if search_term in course['code'].lower() or search_term in course['title'].lower()
                ]
                
                display_courses(filtered, is_filtered=True)
            
            def display_courses(courses, is_filtered=False):
                """Display courses with checkboxes and faculty selection"""
                container = courses_container_ref['container']
                container.clear()
                
                # Store all courses for filtering
                if not is_filtered:
                    courses_container_ref['all_courses'] = courses
                    # Show search box when courses are loaded
                    if courses:
                        courses_container_ref['search_container'].style('display: flex')
                
                with container:
                    if not courses:
                        ui.label('No courses found').classes('text-sm text-gray-500 italic')
                        return
                    
                    status_text = f'{len(courses)} courses available'
                    if is_filtered:
                        status_text += f' (filtered from {len(courses_container_ref["all_courses"])})'
                    ui.label(f'{status_text} - Select courses and preferred faculty:').classes('text-sm font-semibold text-gray-700 mb-2')
                    
                    for course in courses:
                        # Get unique faculty for this course
                        faculty_map = {}  # {faculty_name: [section_ids]}
                        for section in course['sections']:
                            faculty = section['faculty']
                            if faculty not in faculty_map:
                                faculty_map[faculty] = []
                            faculty_map[faculty].append(section['id'])
                        
                        with ui.card().classes('w-full p-4 bg-gray-50'):
                            with ui.row().classes('w-full items-start gap-4'):
                                # Course checkbox
                                course_checkbox = ui.checkbox('').classes('mt-1')
                                course_checkbox.on('update:model-value', lambda e, code=course['code']: toggle_course(code, e.args))
                                
                                # Course info
                                with ui.column().classes('flex-1 gap-2'):
                                    with ui.row().classes('items-center gap-2'):
                                        ui.label(course['code']).classes('text-lg font-bold text-gray-800')
                                        ui.badge(f"{course['credit']} credits", color='orange').classes('text-xs')
                                        ui.badge(f"{len(course['sections'])} sections", color='blue').classes('text-xs')
                                    ui.label(course['title']).classes('text-sm text-gray-600')
                                    
                                    # Faculty preference selection
                                    with ui.column().classes('gap-1 mt-2'):
                                        ui.label('Select preferred faculty (optional):').classes('text-xs font-semibold text-gray-500')
                                        for faculty, section_ids in faculty_map.items():
                                            with ui.row().classes('items-center gap-2 ml-4'):
                                                faculty_checkbox = ui.checkbox('').classes('flex-shrink-0')
                                                faculty_checkbox.on('update:model-value', 
                                                    lambda e, code=course['code'], fac=faculty, secs=section_ids: toggle_faculty_preference(code, fac, secs, e.args))
                                                
                                                section_count = len([s for s in course['sections'] if s['faculty'] == faculty])
                                                ui.label(f"{faculty} ({section_count} section{'s' if section_count > 1 else ''})").classes('text-xs text-gray-600')
            
            def toggle_course(course_code, checked):
                """Toggle course selection"""
                if checked:
                    if course_code not in selected_data['selected_course_codes']:
                        selected_data['selected_course_codes'].append(course_code)
                else:
                    if course_code in selected_data['selected_course_codes']:
                        selected_data['selected_course_codes'].remove(course_code)
            
            def toggle_faculty_preference(course_code, faculty_name, section_ids, checked):
                """Toggle faculty preference for a course"""
                # Initialize faculty preferences if not exists
                if 'faculty_preferences' not in selected_data:
                    selected_data['faculty_preferences'] = {}
                
                if course_code not in selected_data['faculty_preferences']:
                    selected_data['faculty_preferences'][course_code] = []
                
                if checked:
                    # Add faculty preference (store section IDs taught by this faculty)
                    for section_id in section_ids:
                        if section_id not in selected_data['faculty_preferences'][course_code]:
                            selected_data['faculty_preferences'][course_code].append(section_id)
                else:
                    # Remove faculty preference
                    for section_id in section_ids:
                        if section_id in selected_data['faculty_preferences'][course_code]:
                            selected_data['faculty_preferences'][course_code].remove(section_id)

            
            # Preferences card
            with ui.card().classes('w-full p-8 shadow-lg'):
                ui.label('Schedule Preferences (Optional)').classes('text-xl font-semibold text-gray-800 mb-2')
                ui.label('These preferences will help generate better schedules for you').classes('text-sm text-gray-500 mb-6')
                
                with ui.column().classes('w-full gap-4'):
                    max_free = ui.checkbox('Maximize free days (get continuous days off)').classes('text-gray-700')
                    avoid_early = ui.checkbox('Avoid early morning classes (before 9 AM)').classes('text-gray-700')
                    avoid_late = ui.checkbox('Avoid evening classes (after 5 PM)').classes('text-gray-700')
            
            # Generate button
            with ui.row().classes('w-full justify-end mt-6'):
                def on_generate_click():
                    handle_generate(selected_data, max_free.value, avoid_early.value, avoid_late.value)
                
                create_primary_button(
                    'Generate Schedules',
                    on_click=on_generate_click,
                    icon='auto_awesome',
                    full_width=False
                ).classes('px-12 py-3 text-lg')
    
    create_footer()


def handle_generate(selected_data, max_free, avoid_early, avoid_late):
    """Navigate to processing page with validation"""
    # Validate selections
    if not selected_data['semester_id'] or not selected_data['program']:
        ui.notify('Please select semester and program, then load courses', type='warning')
        return
    
    if not selected_data['selected_course_codes'] or len(selected_data['selected_course_codes']) == 0:
        ui.notify('Please select at least one course', type='warning')
        return
    
    # Store in session for processing page
    app.storage.user['schedule_request'] = {
        'semester_id': selected_data['semester_id'],
        'program': selected_data['program'],
        'selected_course_codes': selected_data['selected_course_codes'],
        'faculty_preferences': selected_data.get('faculty_preferences', {}),
        'preferences': {
            'max_free_days': max_free,
            'avoid_early': avoid_early,
            'avoid_late': avoid_late
        }
    }
    
    ui.notify(f'Generating schedules for {len(selected_data["selected_course_codes"])} courses...', type='positive')
    ui.navigate.to('/processing')
