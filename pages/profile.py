from nicegui import ui, app
from backend.constants import DEPARTMENTS
from backend.database import SessionLocal
from backend.models import CompletedCourse, CourseList, CourseOffering
from sqlalchemy import distinct
from components import (
    create_header, create_footer, create_page_container, create_card_container,
    create_input_field, create_select, create_primary_button, create_secondary_button
)

def profile_page():
    """User profile page"""
    ui.colors(primary='#ff6900')
    
    # Check if user is logged in
    if not app.storage.user.get('logged_in', False):
        ui.navigate.to('/signin')
        return
    
    # Get user data from session
    user_name = app.storage.user.get('full_name', 'User')
    user_email = app.storage.user.get('email', '')
    user_student_id = app.storage.user.get('student_id', 'N/A')
    user_department = app.storage.user.get('department', 'Not Set')
    user_id = app.storage.user.get('user_id', '')
    
    # Handle legacy department values (map old to new)
    department_mapping = {
        'Computer Science': 'Computer Science and Engineering',
        'Computer Science and Engineering': 'Computer Science and Engineerings',  # Old to new mapping
        'Engineering': 'Electrical and Electronic Engineering',
        'Business': 'Business Administration',
        'Mathematics': 'Mathematics',
        'Data Science': 'Data Science'
    }
    
    # Map old department name to new one if exists
    if user_department and user_department in department_mapping:
        user_department = department_mapping[user_department]
    
    # If department not in current list, set to first option or 'Not Set'
    if user_department not in DEPARTMENTS:
        user_department = DEPARTMENTS[0] if DEPARTMENTS else 'Not Set'
    
    create_header('AI Academic Scheduler', user_name)
    
    with create_page_container():
        # Welcome section
        with ui.column().classes('w-full gap-2 mb-6'):
            ui.label('My Profile').classes('text-3xl font-bold text-gray-800')
            ui.label('Manage your account information').classes('text-gray-600')
        
        # Profile info card
        with create_card_container():
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('Personal Information').classes('text-xl font-semibold text-gray-800')
                with ui.row().classes('gap-2'):
                    ui.badge(f'ID: {user_id}', color='orange').classes('text-xs')
                    if app.storage.user.get('is_admin', False):
                        ui.badge('ADMIN', color='red').classes('text-xs')
            
            with ui.column().classes('gap-4 w-full max-w-2xl'):
                # Display user information
                with ui.column().classes('w-full gap-2'):
                    ui.label('Full Name').classes('text-sm font-medium text-gray-700')
                    name_input = ui.input(value=user_name).classes('w-full')
                
                with ui.column().classes('w-full gap-2'):
                    ui.label('Email Address').classes('text-sm font-medium text-gray-700')
                    email_input = ui.input(value=user_email).classes('w-full').props('readonly')
                
                with ui.column().classes('w-full gap-2'):
                    ui.label('Student ID').classes('text-sm font-medium text-gray-700')
                    student_id_input = ui.input(value=user_student_id if user_student_id else 'Not provided').classes('w-full').props('readonly')
                
                with ui.column().classes('w-full gap-2'):
                    ui.label('Department').classes('text-sm font-medium text-gray-700')
                    department_select = create_select(
                        '',
                        DEPARTMENTS + ['Not Set'],
                        value=user_department if user_department else 'Not Set'
                    )
        
        # Account Statistics Card
        with create_card_container():
            ui.label('Account Statistics').classes('text-xl font-semibold text-gray-800 mb-4')
            
            with ui.row().classes('w-full gap-6'):
                # Stat boxes
                with ui.card().classes('flex-1 p-4 bg-orange-50'):
                    with ui.column().classes('gap-2'):
                        ui.icon('schedule', size='2rem').classes('text-[#ff6900]')
                        ui.label('0').classes('text-3xl font-bold text-gray-800')
                        ui.label('Schedules Generated').classes('text-sm text-gray-600')
                
                with ui.card().classes('flex-1 p-4 bg-green-50'):
                    with ui.column().classes('gap-2'):
                        ui.icon('school', size='2rem').classes('text-green-600')
                        ui.label('0').classes('text-3xl font-bold text-gray-800')
                        ui.label('Courses Selected').classes('text-sm text-gray-600')
                
                with ui.card().classes('flex-1 p-4 bg-purple-50'):
                    with ui.column().classes('gap-2'):
                        ui.icon('favorite', size='2rem').classes('text-purple-600')
                        ui.label('0').classes('text-3xl font-bold text-gray-800')
                        ui.label('Favorites').classes('text-sm text-gray-600')
        
        # Quick Actions Card
        with create_card_container():
            ui.label('Quick Actions').classes('text-xl font-semibold text-gray-800 mb-4')
            
            with ui.row().classes('w-full gap-4'):
                with ui.button(icon='add_circle', on_click=lambda: ui.navigate.to('/upload')).props('outline color=primary').classes('flex-1'):
                    ui.label('Generate New Schedule').classes('ml-2')
                
                with ui.button(icon='history', on_click=lambda: ui.navigate.to('/results')).props('outline color=secondary').classes('flex-1'):
                    ui.label('View Past Schedules').classes('ml-2')
        
        # Completed Courses Card
        with create_card_container():
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('Completed Courses').classes('text-xl font-semibold text-gray-800')
                ui.button(
                    'Manage Completed Courses',
                    icon='edit',
                    on_click=lambda: show_completed_courses_dialog(user_student_id, user_department)
                ).props('outline color=primary')
            
            ui.label('Mark courses you\'ve already completed to exclude them from schedule generation.').classes('text-sm text-gray-600 mb-3')
            
            # Display current completed courses
            completed_container = ui.column().classes('w-full gap-2')
            load_completed_courses_display(completed_container, user_student_id)
        
        # Action buttons
        with ui.row().classes('w-full justify-between mt-8 gap-4'):
            with ui.row().classes('gap-3'):
                create_secondary_button(
                    'Back to Dashboard',
                    on_click=lambda: ui.navigate.to('/upload'),
                    icon='arrow_back'
                )
                
                ui.button(
                    'Logout',
                    icon='logout',
                    on_click=handle_logout
                ).props('color=negative outline')
            
            create_primary_button(
                'Update Profile',
                on_click=lambda: save_profile(name_input.value, department_select.value),
                icon='save'
            )
    
    create_footer()

def save_profile(name: str, department: str):
    """Save profile changes"""
    # Update session storage
    app.storage.user['full_name'] = name
    app.storage.user['department'] = department
    
    # TODO: Update database
    ui.notify('Profile updated successfully!', type='positive')

def handle_logout():
    """Logout user"""
    app.storage.user.clear()
    ui.notify('Logged out successfully', type='info')
    ui.navigate.to('/signin')


def load_completed_courses_display(container, student_id):
    """Load and display completed courses"""
    container.clear()
    
    db = SessionLocal()
    try:
        # Get completed courses
        completed = db.query(CompletedCourse).filter(
            CompletedCourse.student_id == student_id
        ).order_by(CompletedCourse.course_code).all()
        
        if not completed:
            with container:
                ui.label('No completed courses marked yet.').classes('text-sm text-gray-500 italic')
        else:
            # Get course details from course_list
            completed_codes = [c.course_code for c in completed]
            courses_info = db.query(CourseList).filter(
                CourseList.course_code.in_(completed_codes)
            ).all()
            
            # Create a map of course_code to title
            course_titles = {c.course_code: c.title for c in courses_info}
            
            with container:
                with ui.row().classes('w-full gap-2 flex-wrap'):
                    for course in completed:
                        title = course_titles.get(course.course_code, 'Unknown Course')
                        ui.badge(f'{course.course_code} - {title}', color='green').classes('text-sm px-3 py-1')
                
                ui.label(f'Total: {len(completed)} courses').classes('text-xs text-gray-500 mt-2')
    finally:
        db.close()


def show_completed_courses_dialog(student_id, department):
    """Show dialog to manage completed courses"""
    db = SessionLocal()
    
    try:
        # Sync course_list from course_offering if empty
        course_list_count = db.query(CourseList).count()
        if course_list_count == 0:
            # Get all unique courses from course_offering
            unique_courses = db.query(
                CourseOffering.course_code,
                CourseOffering.title,
                CourseOffering.credit
            ).distinct(CourseOffering.course_code).all()
            
            # Populate course_list
            for code, title, credit in unique_courses:
                if code:  # Skip empty course codes
                    new_course = CourseList(
                        course_code=code,
                        title=title,
                        credit=credit
                    )
                    db.add(new_course)
            
            db.commit()
            print(f"✅ Synced {len(unique_courses)} courses to course_list")
        
        # Get ALL courses from the master course_list table
        all_courses = db.query(CourseList).order_by(CourseList.course_code).all()
        
        # Get student's completed courses
        completed = db.query(CompletedCourse).filter(
            CompletedCourse.student_id == student_id
        ).all()
        completed_codes = {c.course_code for c in completed}
        
        # Create course dictionary
        course_dict = {}
        for course in all_courses:
            course_dict[course.course_code] = {
                'title': course.title,
                'credit': course.credit
            }
        
        with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl p-6'):
            ui.label('Manage Completed Courses').classes('text-2xl font-bold text-gray-800 mb-4')
            ui.label('Select the courses you have already completed. These will be excluded from schedule generation.').classes('text-sm text-gray-600 mb-4')
            
            # Search box with button
            with ui.row().classes('w-full gap-2 mb-4'):
                search_input = ui.input('Search courses...').classes('flex-1').props('outlined dense')
                ui.button('Search', icon='search', on_click=lambda: filter_courses()).props('color=primary')
                ui.button('Clear', icon='clear', on_click=lambda: clear_search()).props('outline')
            
            # Stats display
            stats_label = ui.label('').classes('text-sm text-gray-600 mb-2')
            
            # Scrollable course list
            course_container = ui.column().classes('w-full gap-1 max-h-96 overflow-auto p-2 bg-gray-50 rounded')
            
            # Store checkbox references and their current states
            checkboxes = {}
            checkbox_states = {}  # Track current state of all checkboxes
            
            # Initialize states from completed courses
            for code in course_dict.keys():
                checkbox_states[code] = code in completed_codes
            
            def update_stats():
                """Update the statistics display"""
                checked_count = sum(1 for state in checkbox_states.values() if state)
                stats_label.text = f'Showing {len(checkboxes)} courses | {checked_count} marked as completed'
            
            def on_checkbox_change(code):
                """Handle checkbox state change"""
                def handler(e):
                    checkbox_states[code] = e.value
                    update_stats()
                return handler
            
            def clear_search():
                """Clear search and show all courses"""
                search_input.value = ''
                filter_courses()
            
            def filter_courses():
                """Filter courses based on search"""
                course_container.clear()
                checkboxes.clear()
                search_term = search_input.value.lower() if search_input.value else ''
                
                count = 0
                with course_container:
                    for code, info in sorted(course_dict.items()):
                        title = info['title']
                        credit = info.get('credit', 0)
                        
                        # Filter by search term (search in code or title)
                        if search_term:
                            if (search_term not in code.lower() and 
                                search_term not in title.lower()):
                                continue
                        
                        count += 1
                        with ui.row().classes('w-full items-center gap-2 p-2 hover:bg-white rounded border border-transparent hover:border-orange-200'):
                            # Use the stored state
                            cb = ui.checkbox(
                                value=checkbox_states.get(code, False),
                                on_change=on_checkbox_change(code)
                            ).classes('flex-shrink-0')
                            
                            with ui.column().classes('flex-1 gap-0'):
                                ui.label(f'{code} - {title}').classes('font-medium text-gray-800')
                                if credit:
                                    ui.label(f'Credits: {credit}').classes('text-xs text-gray-500')
                            
                            checkboxes[code] = cb
                
                # Show message if no results
                if count == 0:
                    with course_container:
                        ui.label('No courses found matching your search.').classes('text-gray-500 italic p-4 text-center')
                
            filter_courses()
            
            # Update on search
            search_input.on('input', filter_courses)
            
            ui.separator().classes('my-4')
            
            # Action buttons
            with ui.row().classes('w-full justify-end gap-3'):
                ui.button('Cancel', on_click=dialog.close).props('outline')
                ui.button(
                    'Save Changes',
                    icon='save',
                    on_click=lambda: save_completed_courses(
                        dialog,
                        student_id,
                        department,
                        checkbox_states
                    )
                ).props('color=primary')
        
        dialog.open()
    finally:
        db.close()


def save_completed_courses(dialog, student_id, program, selections):
    """Save completed courses to database"""
    db = SessionLocal()
    
    try:
        # Delete existing completed courses for this student
        db.query(CompletedCourse).filter(
            CompletedCourse.student_id == student_id
        ).delete()
        
        # Add new selections
        count = 0
        for code, is_selected in selections.items():
            if is_selected:
                new_completed = CompletedCourse(
                    student_id=student_id,
                    course_code=code,
                    program=program
                )
                db.add(new_completed)
                count += 1
        
        db.commit()
        ui.notify(f'Successfully saved {count} completed courses!', type='positive')
        
        # Refresh the display
        dialog.close()
        ui.navigate.reload()
        
    except Exception as e:
        db.rollback()
        ui.notify(f'Error saving completed courses: {str(e)}', type='negative')
    finally:
        db.close()

