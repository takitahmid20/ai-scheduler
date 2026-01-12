from nicegui import ui
from components import (
    create_header, create_footer, create_page_container, create_card_container,
    create_input_field, create_primary_button, create_link_button, create_select
)

def signup_page():
    """Sign up page"""
    ui.colors(primary='#2563eb')
    
    create_header('AI Academic Scheduler')
    
    with create_page_container():
        with ui.column().classes('w-full max-w-md mx-auto gap-6'):
            with create_card_container():
                ui.label('Create Account').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Join us to optimize your schedule').classes('text-gray-600 mb-6')
                
                # Form fields
                full_name = create_input_field('Full Name', 'Enter your full name')
                email = create_input_field('Email', 'Enter your email')
                student_id = create_input_field('Student ID', 'Enter your student ID')
                department = create_select('Department', ['Computer Science', 'Engineering', 'Business', 'Mathematics'])
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
    """Handle sign up - placeholder logic"""
    if not all([name, email, student_id, dept, password, confirm]):
        ui.notify('Please fill in all fields', type='warning')
        return
    
    if password != confirm:
        ui.notify('Passwords do not match', type='negative')
        return
    
    # Mock registration
    ui.notify(f'Account created successfully! Welcome, {name}!', type='positive')
    ui.navigate.to('/upload')
