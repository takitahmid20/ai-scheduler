from nicegui import ui, app
from backend.constants import DEPARTMENTS
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
