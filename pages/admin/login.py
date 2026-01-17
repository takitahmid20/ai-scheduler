from nicegui import ui, app
from backend.services.auth_service import AuthService

def admin_login_page():
    """Admin login page"""
    ui.colors(primary='#ff6900')
    
    with ui.column().classes('w-full h-screen items-center justify-center bg-gradient-to-br from-orange-50 to-orange-100'):
        with ui.card().classes('w-full max-w-md p-10 shadow-2xl'):
            # Logo/Icon
            with ui.row().classes('w-full justify-center mb-6'):
                ui.icon('admin_panel_settings', size='4rem').classes('text-[#ff6900]')
            
            # Title
            ui.label('Admin Portal').classes('text-3xl font-bold text-gray-800 text-center w-full mb-2')
            ui.label('Course Management System').classes('text-sm text-gray-500 text-center w-full mb-8')
            
            # Login form
            with ui.column().classes('w-full gap-6'):
                # Email field
                with ui.column().classes('w-full gap-2'):
                    ui.label('Email Address').classes('text-sm font-medium text-gray-700')
                    email = ui.input(
                        placeholder='admin@gmail.com'
                    ).classes('w-full').props('type=email outlined')
                
                # Password field
                with ui.column().classes('w-full gap-2'):
                    ui.label('Password').classes('text-sm font-medium text-gray-700')
                    password = ui.input(
                        placeholder='Enter your password'
                    ).classes('w-full').props('type=password outlined')
                
                # Remember me checkbox
                with ui.row().classes('w-full justify-between items-center'):
                    ui.checkbox('Remember me').classes('text-gray-700')
                
                # Login button
                ui.button(
                    'Login to Dashboard',
                    on_click=lambda: handle_admin_login(email.value, password.value)
                ).classes('w-full py-3 text-white font-semibold').props('icon=login color=primary size=lg')
                
                # Divider
                ui.separator()
                
                # Back to student portal
                with ui.row().classes('w-full justify-center'):
                    ui.link('Back to Student Portal', '/').classes('text-sm text-[#ff6900] hover:text-[#e65f00]')

def handle_admin_login(email, password):
    """Handle admin login - direct backend call"""
    result = AuthService.admin_signin(email, password)
    
    if result['success']:
        user_data = result['user']
        ui.notify('Welcome Admin!', type='positive')
        # Store admin session
        app.storage.user['logged_in'] = True
        app.storage.user['email'] = user_data['email']
        app.storage.user['full_name'] = user_data['full_name']
        app.storage.user['is_admin'] = True
        ui.navigate.to('/admin/dashboard')
    else:
        ui.notify('Invalid credentials. Please try again.', type='negative')
