from nicegui import ui, app

# Mock data for demonstration
mock_courses = [
    {'code': 'CSE 1111', 'title': 'Structured Programming Language', 'credits': '3.0', 'dept': 'CSE', 'trimester': 'Spring 2026'},
    {'code': 'CSE 1112', 'title': 'Structured Programming Language Lab', 'credits': '1.0', 'dept': 'CSE', 'trimester': 'Spring 2026'},
    {'code': 'CSE 2213', 'title': 'Discrete Mathematics', 'credits': '3.0', 'dept': 'CSE', 'trimester': 'Spring 2026'},
    {'code': 'CSE 2215', 'title': 'Data Structure and Algorithms I', 'credits': '3.0', 'dept': 'CSE', 'trimester': 'Spring 2026'},
    {'code': 'CSE 2216', 'title': 'Data Structure and Algorithms I Lab', 'credits': '1.0', 'dept': 'CSE', 'trimester': 'Spring 2026'},
    {'code': 'BDS 1201', 'title': 'Introduction to Data Science', 'credits': '3.0', 'dept': 'Data Science', 'trimester': 'Spring 2026'},
    {'code': 'MATH 1151', 'title': 'Fundamental Calculus', 'credits': '3.0', 'dept': 'Math', 'trimester': 'Spring 2026'},
]

def handle_admin_logout():
    """Handle admin logout"""
    app.storage.user.clear()
    ui.notify('Logged out successfully', type='info')
    ui.navigate.to('/admin/login')

def admin_manage_data_page():
    """Admin page to manage course data"""
    ui.colors(primary='#ff6900')
    
    # Admin Header
    with ui.header().classes('bg-[#ff6900] text-white shadow-lg'):
        with ui.row().classes('w-full items-center justify-between px-6 py-3'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('admin_panel_settings', size='2rem')
                ui.label('Admin Dashboard').classes('text-2xl font-bold')
            
            with ui.row().classes('items-center gap-4'):
                ui.button('Back to Dashboard', icon='arrow_back', on_click=lambda: ui.navigate.to('/admin/dashboard')).props('flat')
                ui.button('Logout', icon='logout', on_click=handle_admin_logout).props('flat')
    
    with ui.row().classes('w-full h-screen'):
        # Sidebar Navigation
        with ui.column().classes('w-64 bg-gray-800 text-white p-4 gap-2'):
            ui.label('NAVIGATION').classes('text-xs text-gray-400 font-semibold mb-2 mt-4')
            
            nav_button('dashboard', 'Dashboard', '/admin/dashboard')
            nav_button('upload_file', 'Upload Data', '/admin/upload')
            nav_button('table_view', 'Manage Data', '/admin/manage-data', active=True)
            nav_button('people', 'Students', '#')
            nav_button('school', 'Courses', '#')
            nav_button('schedule', 'Schedules', '#')
            
            ui.label('SETTINGS').classes('text-xs text-gray-400 font-semibold mb-2 mt-6')
            nav_button('settings', 'Settings', '#')
            nav_button('help', 'Help & Support', '#')
        
        # Main Content Area
        with ui.column().classes('flex-1 bg-gray-50 p-8 overflow-auto'):
            # Page title
            with ui.row().classes('w-full items-center justify-between mb-6'):
                with ui.column().classes('gap-2'):
                    ui.label('Manage Course Data').classes('text-3xl font-bold text-gray-800')
                    ui.label('View, edit, and manage all course information').classes('text-gray-600')
                
                ui.button('Add New Course', icon='add', on_click=lambda: ui.notify('Add course dialog (Design only)')).props('color=primary')
            
            # Filters Card
            with ui.card().classes('w-full p-6 shadow-lg mb-6'):
                ui.label('Filters').classes('text-lg font-semibold text-gray-800 mb-4')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1 gap-2'):
                        ui.label('Trimester').classes('text-sm font-medium text-gray-700')
                        ui.select(['All', 'Spring 2026', 'Summer 2026', 'Fall 2026'], value='All').classes('w-full')
                    
                    with ui.column().classes('flex-1 gap-2'):
                        ui.label('Department').classes('text-sm font-medium text-gray-700')
                        ui.select(['All', 'CSE', 'Data Science', 'EEE', 'Business', 'Math'], value='All').classes('w-full')
                    
                    with ui.column().classes('flex-1 gap-2'):
                        ui.label('Search').classes('text-sm font-medium text-gray-700')
                        ui.input(placeholder='Search by code or title...').classes('w-full').props('outlined')
                    
                    with ui.column().classes('gap-2 justify-end'):
                        ui.label(' ').classes('text-sm')
                        ui.button('Apply Filters', icon='filter_alt').props('color=primary')
            
            # Data Table Card
            with ui.card().classes('w-full p-6 shadow-lg'):
                with ui.row().classes('w-full items-center justify-between mb-4'):
                    ui.label('Course List').classes('text-lg font-semibold text-gray-800')
                    with ui.row().classes('gap-2'):
                        ui.button(icon='download', on_click=lambda: ui.notify('Export (Design only)')).props('flat')
                        ui.button(icon='refresh', on_click=lambda: ui.notify('Refresh (Design only)')).props('flat')
                
                # Table
                columns = [
                    {'name': 'code', 'label': 'Course Code', 'field': 'code', 'align': 'left'},
                    {'name': 'title', 'label': 'Course Title', 'field': 'title', 'align': 'left'},
                    {'name': 'credits', 'label': 'Credits', 'field': 'credits', 'align': 'center'},
                    {'name': 'dept', 'label': 'Department', 'field': 'dept', 'align': 'left'},
                    {'name': 'trimester', 'label': 'Trimester', 'field': 'trimester', 'align': 'left'},
                    {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'},
                ]
                
                table = ui.table(
                    columns=columns,
                    rows=mock_courses,
                    row_key='code'
                ).classes('w-full')
                
                # Add custom action buttons for each row
                table.add_slot('body-cell-actions', '''
                    <q-td :props="props">
                        <q-btn flat round dense icon="edit" color="primary" size="sm" />
                        <q-btn flat round dense icon="delete" color="negative" size="sm" />
                    </q-td>
                ''')
                
                # Pagination
                with ui.row().classes('w-full justify-between items-center mt-4'):
                    ui.label('Showing 7 of 7 courses').classes('text-sm text-gray-600')
                    with ui.row().classes('gap-2'):
                        ui.button(icon='chevron_left').props('flat dense disable')
                        ui.label('1').classes('px-3 py-1 bg-[#ff6900] text-white rounded')
                        ui.button(icon='chevron_right').props('flat dense disable')

def nav_button(icon, label, link, active=False):
    """Create a navigation button"""
    classes = 'w-full justify-start'
    if active:
        classes += ' bg-[#ff6900]'
    
    with ui.button(icon=icon, on_click=lambda: ui.navigate.to(link) if link != '#' else None).props('flat align=left').classes(classes):
        ui.label(label).classes('ml-3')
