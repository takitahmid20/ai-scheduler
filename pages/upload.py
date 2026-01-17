from nicegui import ui, app
from backend.constants import DEPARTMENTS
from components import (
    create_header, create_footer, create_primary_button
)

# Available departments (using constants)
departments = DEPARTMENTS

# Available courses per department (dummy data - will be from database)
courses_by_department = {
    'Computer Science and Engineering': [
        'CSE 1111 - Structured Programming Language',
        'CSE 1112 - Structured Programming Language Lab',
        'CSE 2213 - Discrete Mathematics',
        'CSE 2215 - Data Structure and Algorithms I',
        'CSE 2216 - Data Structure and Algorithms I Lab',
        'CSE 1325 - Digital Logic Design',
        'CSE 1326 - Digital Logic Design Lab',
        'CSE 1115 - Object Oriented Programming',
        'CSE 1116 - Object Oriented Programming Lab',
        'CSE 2217 - Data Structure and Algorithms II',
        'CSE 2218 - Data Structure and Algorithms II Lab',
        'MATH 2183 - Calculus and Linear Algebra',
        'MATH 2201 - Coordinate Geometry and Vector Analysis',
        'MATH 2205 - Probability and Statistics',
        'PHY 2105 - Physics',
        'PHY 2106 - Physics Lab',
        'EEE 2113 - Electrical Circuits',
    ],
    'Data Science': [
        'CSE 1110 - Introduction to Computer Systems',
        'MATH 1151 - Fundamental Calculus',
        'CSE 1111 - Structured Programming Language',
        'CSE 2213 - Discrete Mathematics',
    ],
}

# Store selected values
selected_department = None
selected_courses_list = []

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
    
    # Main container with better width
    with ui.column().classes('w-full items-center p-8'):
        # Centered content container
        with ui.column().classes('w-full max-w-4xl gap-8'):
            # Page title
            with ui.column().classes('w-full gap-2 mb-4'):
                ui.label('Select Your Courses').classes('text-3xl font-bold text-gray-800')
                ui.label('Choose your department and courses for this semester').classes('text-gray-600')
            
            # Variable to store courses select widget
            courses_select = None
            
            # Department Selection Card
            with ui.card().classes('w-full p-8 shadow-lg'):
                ui.label('Department Selection').classes('text-xl font-semibold text-gray-800 mb-2')
                ui.label('Choose your department to see relevant courses').classes('text-sm text-gray-500 mb-6')
                
                ui.label('Select Your Department').classes('text-sm font-medium text-gray-700 mb-2')
                
                # Department dropdown
                department_select = ui.select(
                    departments,
                    value=departments[0]
                ).classes('w-full')
                
                ui.label('Available courses will be shown based on your department').classes('text-xs text-gray-500 mt-2')

            # Student Information Card
            with ui.card().classes('w-full p-8 shadow-lg'):
                ui.label('Student Information').classes('text-xl font-semibold text-gray-800 mb-2')
                ui.label('Help us understand your academic progress').classes('text-sm text-gray-500 mb-6')
                
                with ui.column().classes('w-full gap-6'):
                    # Completed courses - IMPORTANT
                    with ui.column().classes('w-full gap-2'):
                        with ui.row().classes('items-center gap-2'):
                            ui.label('Completed Courses').classes('text-sm font-semibold text-gray-700')
                            ui.badge('Required', color='warning').classes('text-xs')
                        ui.label('Enter course codes you have already completed (one per line or comma-separated)').classes('text-xs text-gray-500')
                        completed_courses = ui.textarea(
                            placeholder='Example:\nCSE 1110, ENG 1011, MATH 1151\nBDS 1201'
                        ).classes('w-full').props('rows=4')
                    
                    ui.separator()
                    
                    # Course selection - Main feature
                    with ui.column().classes('w-full gap-2'):
                        with ui.row().classes('items-center gap-2'):
                            ui.label('Select Courses for This Semester').classes('text-sm font-semibold text-gray-700')
                            ui.badge('Required', color='warning').classes('text-xs')
                        ui.label('Choose courses you want to take (AI will check prerequisites and conflicts)').classes('text-xs text-gray-500')
                        
                        # Container for course selection that updates based on department
                        courses_container = ui.column().classes('w-full')
                        
                        # Function to update courses when department changes
                        def update_courses(dept):
                            """Update course list when department changes"""
                            global selected_department, courses_select
                            selected_department = dept
                            courses_container.clear()
                            
                            with courses_container:
                                dept_courses = courses_by_department.get(dept, [])
                                if len(dept_courses) == 0:
                                    ui.label('No courses available for this department yet').classes('text-sm text-gray-500 italic')
                                else:
                                    courses_select = ui.select(
                                        dept_courses,
                                        multiple=True,
                                        with_input=True,
                                        clearable=True,
                                        value=[]
                                    ).classes('w-full').props('use-chips')
                        
                        # Connect department dropdown to update function
                        department_select.on('update:model-value', lambda e: update_courses(e.args))
                        
                        # Initialize with first department's courses
                        initial_courses = courses_by_department.get(departments[0], [])
                        courses_select = ui.select(
                            initial_courses,
                            multiple=True,
                            with_input=True,
                            clearable=True,
                            value=[]
                        ).classes('w-full').props('use-chips')

            
            # Preferences card
            with ui.card().classes('w-full p-8 shadow-lg'):
                ui.label('Schedule Preferences').classes('text-xl font-semibold text-gray-800 mb-2')
                ui.label('Optional preferences to help generate better schedules').classes('text-sm text-gray-500 mb-6')
                
                with ui.column().classes('w-full gap-6'):
                    # Time preference
                    with ui.column().classes('w-full gap-2'):
                        with ui.row().classes('items-center gap-2'):
                            ui.label('Preferred Time').classes('text-sm font-medium text-gray-700')
                            ui.badge('Optional', color='grey').classes('text-xs')
                        time_pref = ui.select(
                            ['No Preference', 'Morning (8 AM - 12 PM)', 'Afternoon (12 PM - 4 PM)', 'Evening (4 PM - 8 PM)'],
                            value='No Preference'
                        ).classes('w-full')
                    
                    # Checkboxes
                    with ui.column().classes('w-full gap-3'):
                        avoid_conflicts = ui.checkbox('Prioritize exam conflict avoidance').classes('text-gray-700')
                        avoid_conflicts.value = True
                        max_free = ui.checkbox('Maximize free days').classes('text-gray-700')
                    
                    # Faculty preference
                    with ui.column().classes('w-full gap-2'):
                        with ui.row().classes('items-center gap-2'):
                            ui.label('Preferred Faculty').classes('text-sm font-medium text-gray-700')
                            ui.badge('Optional', color='grey').classes('text-xs')
                        ui.label('Enter faculty names you prefer (comma-separated)').classes('text-xs text-gray-500')
                        faculty = ui.input(placeholder='e.g. Dr. Smith, Prof. Johnson').classes('w-full')
            
            # Generate button
            with ui.row().classes('w-full justify-end mt-6'):
                def on_generate_click():
                    if courses_select is None:
                        ui.notify('Please select your department first', type='warning')
                        return
                    handle_generate(completed_courses.value, courses_select.value)
                
                create_primary_button(
                    'Generate Schedules',
                    on_click=on_generate_click,
                    icon='auto_awesome',
                    full_width=False
                ).classes('px-12 py-3 text-lg')
    
    create_footer()

def handle_department_change(dept):
    """Update course list when department changes"""
    global selected_department, selected_courses_list
    selected_department = dept
    selected_courses_list = []  # Reset selected courses
    # Course dropdown will be updated via the on_change event


def handle_generate(completed_courses_text, selected_courses):
    """Navigate to processing page with validation"""
    # Validate completed courses input
    if not completed_courses_text or completed_courses_text.strip() == '':
        ui.notify('Please enter your completed courses', type='warning')
        return
    
    # Validate course selection
    if not selected_courses or len(selected_courses) == 0:
        ui.notify('Please select at least one course for this semester', type='warning')
        return
    
    # Store data for processing (in real app, would save to database/session)
    global selected_courses_list
    selected_courses_list = selected_courses
    
    ui.notify(f'Generating schedules for {len(selected_courses)} courses...', type='positive')
    ui.navigate.to('/processing')
