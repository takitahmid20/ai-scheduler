from nicegui import ui, app
from backend.services.auth_service import AuthService
from components import (
    create_header, create_footer, create_page_container, create_card_container,
    create_input_field, create_primary_button, create_link_button
)

def signin_page():
    """Sign in page"""
    ui.colors(primary='#ff6900')
    
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
                
                # Admin portal link
                ui.separator().classes('my-4')
                with ui.row().classes('w-full justify-center'):
                    ui.icon('admin_panel_settings', size='sm').classes('text-[#ff6900]')
                    ui.link('Admin Portal', '/admin/login').classes('text-sm text-[#ff6900] hover:text-[#e65f00] ml-2 font-medium')
    
    create_footer()

def handle_signin(email: str, password: str):
    """Handle sign in - direct backend call"""
    if not email or not password:
        ui.notify('Please fill in all fields', type='warning')
        return
    
    # Call backend service directly
    result = AuthService.signin(email, password)
    
    if result['success']:
        user_data = result['user']
        # Store user data in session storage first
        app.storage.user['logged_in'] = True
        app.storage.user['user_id'] = user_data['id']
        app.storage.user['email'] = user_data['email']
        app.storage.user['full_name'] = user_data['full_name']
        app.storage.user['student_id'] = user_data.get('student_id')
        app.storage.user['department'] = user_data.get('department')
        app.storage.user['is_admin'] = user_data.get('is_admin', False)
        
        # Show notification and navigate
        ui.notify(f'Welcome back, {user_data["full_name"]}!', type='positive')
        ui.timer(0.5, lambda: ui.navigate.to('/profile'), once=True)
    else:
        ui.notify(f'Login failed: {result["error"]}', type='negative')
