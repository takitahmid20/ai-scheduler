from nicegui import ui
from components import (
    create_header, create_footer, create_page_container, create_card_container,
    create_input_field, create_primary_button, create_link_button
)

def signin_page():
    """Sign in page"""
    ui.colors(primary='#2563eb')
    
    create_header('AI Academic Scheduler')
    
    with create_page_container():
        # Center the form
        with ui.column().classes('w-full max-w-md mx-auto gap-6'):
            # Welcome card
            with create_card_container():
                ui.label('Welcome Back').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Sign in to your account to continue').classes('text-gray-600 mb-6')
                
                # Form fields
                email = create_input_field('Email', 'Enter your email')
                password = create_input_field('Password', 'Enter your password', password=True)
                
                # Sign in button
                create_primary_button(
                    'Sign In', 
                    on_click=lambda: handle_signin(email.value, password.value),
                    icon='login',
                    full_width=True
                ).classes('mt-4')
                
                # Links
                with ui.row().classes('w-full justify-between mt-4'):
                    create_link_button('Forgot password?', '/signin')
                    create_link_button("Don't have an account? Sign up", '/signup')
    
    create_footer()

def handle_signin(email: str, password: str):
    """Handle sign in - placeholder logic"""
    if email and password:
        # Mock authentication
        ui.notify(f'Welcome back, {email}!', type='positive')
        ui.navigate.to('/upload')
    else:
        ui.notify('Please fill in all fields', type='warning')
