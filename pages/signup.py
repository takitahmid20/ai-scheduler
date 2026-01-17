from nicegui import ui, app
from backend.services.auth_service import AuthService
from backend.constants import DEPARTMENTS, YEAR_LEVELS
from components import (
    create_header, create_footer, create_page_container, create_card_container,
    create_input_field, create_primary_button, create_link_button, create_select
)

def signup_page():
    """Sign up page"""
    ui.colors(primary='#ff6900')
    
    create_header('AI Academic Scheduler')
    
    with create_page_container():
        with ui.column().classes('w-full max-w-md mx-auto gap-6'):
            with create_card_container():
                ui.label('Create Account').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Join us to optimize your schedule').classes('text-gray-600 mb-6')
                
                # Form fields
                full_name = create_input_field('Full Name', 'Enter your full name')
                email = create_input_field('Email', 'Enter your email')
                student_id = create_input_field('Student ID', 'Enter your student ID (optional)')
                department = create_select('Department', DEPARTMENTS)
                password = create_input_field('Password', 'Create a password', password=True)
                confirm_password = create_input_field('Confirm Password', 'Re-enter password', password=True)
                
                # Sign up button
                create_primary_button(
                    'Create Account',
                    on_click=lambda: handle_signup(
                        full_name.value, email.value, student_id.value, 
                        department.value, password.value, confirm_password.value
                    ),
                    icon='person_add',
                    full_width=True
                ).classes('mt-4')
                
                # Link to sign in
                with ui.row().classes('w-full justify-center mt-4'):
                    create_link_button('Already have an account? Sign in', '/signin')
    
    create_footer()

def handle_signup(name: str, email: str, student_id: str, dept: str, password: str, confirm: str):
    """Handle sign up - direct backend call"""
    if not all([name, email, password, confirm]):
        ui.notify('Please fill in required fields', type='warning')
        return
    
    if password != confirm:
        ui.notify('Passwords do not match', type='negative')
        return
    
    # Skip department if "Not Set"
    department_value = None if dept == 'Not Set' else dept
    
    # Call backend service directly
    result = AuthService.signup(
        email=email,
        password=password,
        full_name=name,
        student_id=student_id if student_id else None,
        department=department_value
    )
    
    if result['success']:
        # Auto sign in after signup
        signin_result = AuthService.signin(email, password)
        if signin_result['success']:
            user_data = signin_result['user']
            app.storage.user['logged_in'] = True
            app.storage.user['user_id'] = user_data['id']
            app.storage.user['email'] = user_data['email']
            app.storage.user['full_name'] = user_data['full_name']
            app.storage.user['student_id'] = user_data.get('student_id')
            app.storage.user['department'] = user_data.get('department')
        
        ui.notify(f'Account created successfully! Welcome, {name}!', type='positive')
        ui.timer(0.5, lambda: ui.navigate.to('/profile'), once=True)
    else:
        ui.notify(f'Signup failed: {result["error"]}', type='negative')
