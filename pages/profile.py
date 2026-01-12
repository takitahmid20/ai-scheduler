from nicegui import ui
from components import (
    create_header, create_footer, create_page_container, create_card_container,
    create_input_field, create_select, create_primary_button, create_secondary_button
)

# Mock user data
user_data = {
    'name': 'John Doe',
    'email': 'john.doe@university.edu',
    'student_id': 'CS2024001',
    'department': 'Computer Science',
    'semester': 'Spring 2026'
}

def profile_page():
    """User profile page"""
    ui.colors(primary='#2563eb')
    
    create_header('AI Academic Scheduler', user_data['name'])
    
    with create_page_container():
        ui.label('My Profile').classes('text-3xl font-bold text-gray-800 mb-2')
        ui.label('Manage your account information').classes('text-gray-600 mb-8')
        
        # Profile info card
        with create_card_container():
            ui.label('Personal Information').classes('text-xl font-semibold text-gray-800 mb-4')
            
            with ui.column().classes('gap-4 w-full max-w-2xl'):
                name = create_input_field('Full Name', user_data['name'])
                name.value = user_data['name']
                
                email = create_input_field('Email', user_data['email'])
                email.value = user_data['email']
                
                student_id = create_input_field('Student ID', user_data['student_id'])
                student_id.value = user_data['student_id']
                student_id.props('readonly')
                
                department = create_select(
                    'Department',
                    ['Computer Science', 'Engineering', 'Business', 'Mathematics'],
                    value=user_data['department']
                )
                
                semester = create_select(
                    'Current Semester',
                    ['Spring 2026', 'Fall 2025', 'Summer 2026'],
                    value=user_data['semester']
                )
        
        # Change password card
        with create_card_container():
            ui.label('Change Password').classes('text-xl font-semibold text-gray-800 mb-4')
            
            with ui.column().classes('gap-4 w-full max-w-2xl'):
                current_password = create_input_field('Current Password', '', password=True)
                new_password = create_input_field('New Password', '', password=True)
                confirm_password = create_input_field('Confirm New Password', '', password=True)
        
        # Action buttons
        with ui.row().classes('w-full justify-between mt-8'):
            create_secondary_button(
                'Cancel',
                on_click=lambda: ui.navigate.to('/upload'),
                icon='close'
            )
            
            create_primary_button(
                'Save Changes',
                on_click=lambda: save_profile(name.value, email.value, department.value, semester.value),
                icon='save'
            )
    
    create_footer()

def save_profile(name: str, email: str, dept: str, semester: str):
    """Save profile changes - placeholder"""
    user_data['name'] = name
    user_data['email'] = email
    user_data['department'] = dept
    user_data['semester'] = semester
    
    ui.notify('✓ Profile updated successfully!', type='positive')
