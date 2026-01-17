from nicegui import ui, app

def handle_admin_logout():
    """Handle admin logout"""
    app.storage.user.clear()
    ui.notify('Logged out successfully', type='info')
    ui.navigate.to('/admin/login')

def admin_dashboard_page():
    """Admin dashboard main page"""
    ui.colors(primary='#ff6900')
    
    # Admin Header
    with ui.header().classes('bg-[#ff6900] text-white shadow-lg'):
        with ui.row().classes('w-full items-center justify-between px-6 py-3'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('admin_panel_settings', size='2rem')
                ui.label('Admin Dashboard').classes('text-2xl font-bold')
            
            with ui.row().classes('items-center gap-4'):
                ui.button(icon='notifications', on_click=lambda: None).props('flat round')
                ui.button(icon='settings', on_click=lambda: None).props('flat round')
                with ui.button(icon='account_circle', on_click=lambda: None).props('flat'):
                    admin_name = app.storage.user.get('full_name', 'Admin')
                    ui.label(admin_name).classes('ml-2')
                ui.button('Logout', icon='logout', on_click=handle_admin_logout).props('flat')
    
    with ui.row().classes('w-full h-screen'):
        # Sidebar Navigation
        with ui.column().classes('w-64 bg-gray-800 text-white p-4 gap-2'):
            ui.label('NAVIGATION').classes('text-xs text-gray-400 font-semibold mb-2 mt-4')
            
            nav_button('dashboard', 'Dashboard', '/admin/dashboard', active=True)
            nav_button('upload_file', 'Upload Data', '/admin/upload')
            nav_button('table_view', 'Manage Data', '/admin/manage-data')
            nav_button('people', 'Students', '#')
            nav_button('school', 'Courses', '#')
            nav_button('schedule', 'Schedules', '#')
            
            ui.label('SETTINGS').classes('text-xs text-gray-400 font-semibold mb-2 mt-6')
            nav_button('settings', 'Settings', '#')
            nav_button('help', 'Help & Support', '#')
        
        # Main Content Area
        with ui.column().classes('flex-1 bg-gray-50 p-8 overflow-auto'):
            # Welcome section
            with ui.card().classes('w-full p-6 shadow-lg mb-6 bg-gradient-to-r from-orange-500 to-[#ff6900] text-white'):
                ui.label('Welcome back, Admin!').classes('text-2xl font-bold mb-2')
                ui.label('Manage course data and student schedules efficiently').classes('text-orange-100')
            
            # Statistics Cards
            with ui.row().classes('w-full gap-6 mb-6'):
                stat_card('folder', 'Total Uploads', '12', 'Files uploaded this semester', 'bg-orange-500')
                stat_card('school', 'Total Courses', '156', 'Across all departments', 'bg-green-500')
                stat_card('people', 'Active Students', '2,340', 'Currently enrolled', 'bg-purple-500')
                stat_card('schedule', 'Schedules Generated', '1,890', 'This semester', 'bg-orange-500')
            
            # Quick Actions
            with ui.card().classes('w-full p-6 shadow-lg mb-6'):
                ui.label('Quick Actions').classes('text-xl font-bold text-gray-800 mb-4')
                
                with ui.row().classes('w-full gap-4'):
                    action_card('upload_file', 'Upload Course Data', 'Upload department PDF files', '/admin/upload', 'blue')
                    action_card('table_view', 'Manage Data', 'View and edit course data', '/admin/manage-data', 'green')
                    action_card('analytics', 'View Analytics', 'Check system statistics', '#', 'purple')
                    action_card('download', 'Export Data', 'Download reports', '#', 'orange')
            
            # Recent Activity
            with ui.card().classes('w-full p-6 shadow-lg'):
                ui.label('Recent Activity').classes('text-xl font-bold text-gray-800 mb-4')
                
                with ui.column().classes('w-full gap-3'):
                    activity_item('upload_file', 'CSE Department data uploaded', '2 hours ago', 'success')
                    activity_item('edit', 'Course data updated - EEE', '5 hours ago', 'info')
                    activity_item('people', 'New student registration', '1 day ago', 'success')
                    activity_item('schedule', 'Schedule generated for BBA', '2 days ago', 'info')
                    activity_item('warning', 'System backup completed', '3 days ago', 'warning')

def nav_button(icon, label, link, active=False):
    """Create a navigation button"""
    classes = 'w-full justify-start'
    if active:
        classes += ' bg-[#ff6900]'
    
    with ui.button(icon=icon, on_click=lambda: ui.navigate.to(link) if link != '#' else None).props('flat align=left').classes(classes):
        ui.label(label).classes('ml-3')

def stat_card(icon, title, value, subtitle, color):
    """Create a statistics card"""
    with ui.card().classes(f'flex-1 p-6 shadow-lg {color} text-white'):
        with ui.row().classes('w-full items-center justify-between mb-3'):
            ui.icon(icon, size='2.5rem').classes('opacity-80')
            ui.label(value).classes('text-4xl font-bold')
        ui.label(title).classes('text-lg font-semibold mb-1')
        ui.label(subtitle).classes('text-sm opacity-90')

def action_card(icon, title, description, link, color):
    """Create a quick action card"""
    color_classes = {
        'blue': 'bg-orange-50 hover:bg-orange-100 border-orange-200 text-[#ff6900]',
        'green': 'bg-green-50 hover:bg-green-100 border-green-200 text-green-700',
        'purple': 'bg-purple-50 hover:bg-purple-100 border-purple-200 text-purple-700',
        'orange': 'bg-orange-50 hover:bg-orange-100 border-orange-200 text-orange-700',
    }
    
    with ui.card().classes(f'flex-1 p-6 cursor-pointer border-2 {color_classes[color]} transition-all').on('click', lambda: ui.navigate.to(link) if link != '#' else None):
        ui.icon(icon, size='2.5rem').classes('mb-3')
        ui.label(title).classes('text-lg font-bold mb-1')
        ui.label(description).classes('text-sm opacity-80')

def activity_item(icon, text, time, type):
    """Create an activity item"""
    color_map = {
        'success': 'text-green-600 bg-green-50',
        'info': 'text-[#ff6900] bg-orange-50',
        'warning': 'text-orange-600 bg-orange-50',
    }
    
    with ui.row().classes('w-full items-center gap-4 p-3 rounded-lg hover:bg-gray-50'):
        with ui.avatar().classes(color_map[type]):
            ui.icon(icon)
        with ui.column().classes('flex-1'):
            ui.label(text).classes('text-gray-800 font-medium')
            ui.label(time).classes('text-xs text-gray-500')
