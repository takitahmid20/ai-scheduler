from nicegui import ui, app

# Trimesters
trimesters = ['Spring 2026', 'Summer 2026', 'Fall 2026', 'Winter 2026']

# Departments
departments = [
    'Computer Science and Engineering',
    'Data Science',
    'Electrical and Electronic Engineering',
    'Business Administration',
    'Mathematics',
]

def handle_admin_logout():
    """Handle admin logout"""
    app.storage.user.clear()
    ui.notify('Logged out successfully', type='info')
    ui.navigate.to('/admin/login')

def admin_upload_page():
    """Admin page to upload department course data"""
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
            nav_button('upload_file', 'Upload Data', '/admin/upload', active=True)
            nav_button('table_view', 'Manage Data', '/admin/manage-data')
            nav_button('people', 'Students', '#')
            nav_button('school', 'Courses', '#')
            nav_button('schedule', 'Schedules', '#')
            
            ui.label('SETTINGS').classes('text-xs text-gray-400 font-semibold mb-2 mt-6')
            nav_button('settings', 'Settings', '#')
            nav_button('help', 'Help & Support', '#')
        
        # Main Content Area
        with ui.column().classes('flex-1 bg-gray-50 p-8 overflow-auto'):
            # Page title
            with ui.column().classes('w-full gap-2 mb-6'):
                ui.label('Upload Course Data').classes('text-3xl font-bold text-gray-800')
                ui.label('Upload department-specific PDF files for AI analysis and data extraction').classes('text-gray-600')
            
            # Upload Form Card
            with ui.card().classes('w-full max-w-4xl p-8 shadow-lg'):
                ui.label('Course Data Upload').classes('text-xl font-semibold text-gray-800 mb-2')
                ui.label('Select trimester and department, then upload the course PDF file').classes('text-sm text-gray-500 mb-6')
                
                with ui.column().classes('w-full gap-6'):
                    # Trimester Selection
                    with ui.column().classes('w-full gap-2'):
                        with ui.row().classes('items-center gap-2'):
                            ui.label('Select Trimester').classes('text-sm font-semibold text-gray-700')
                            ui.badge('Required', color='warning').classes('text-xs')
                        trimester_select = ui.select(
                            trimesters,
                            value=trimesters[0]
                        ).classes('w-full')
                    
                    # Department Selection
                    with ui.column().classes('w-full gap-2'):
                        with ui.row().classes('items-center gap-2'):
                            ui.label('Select Department').classes('text-sm font-semibold text-gray-700')
                            ui.badge('Required', color='warning').classes('text-xs')
                        department_select = ui.select(
                            departments,
                            value=departments[0]
                        ).classes('w-full')
                    
                    ui.separator()
                    
                    # File Upload Section
                    with ui.column().classes('w-full gap-2'):
                        with ui.row().classes('items-center gap-2'):
                            ui.label('Upload Course PDF').classes('text-sm font-semibold text-gray-700')
                            ui.badge('Required', color='warning').classes('text-xs')
                        ui.label('Upload the official course document in PDF format').classes('text-xs text-gray-500')
                        
                        # Upload area
                        with ui.card().classes('w-full p-8 border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 cursor-pointer'):
                            with ui.column().classes('w-full items-center gap-3'):
                                ui.icon('cloud_upload', size='4rem').classes('text-gray-400')
                                ui.label('Click to upload or drag and drop').classes('text-lg font-medium text-gray-700')
                                ui.label('PDF files only (Max 10MB)').classes('text-sm text-gray-500')
                                
                                upload = ui.upload(
                                    on_upload=lambda e: handle_file_upload(e, trimester_select.value, department_select.value),
                                    auto_upload=True
                                ).props('accept=.pdf').classes('hidden')
                                
                                ui.button('Select File', icon='attach_file', on_click=upload.run_method).props('color=primary')
                    
                    # Additional Notes
                    with ui.column().classes('w-full gap-2'):
                        ui.label('Additional Notes (Optional)').classes('text-sm font-medium text-gray-700')
                        notes = ui.textarea(
                            placeholder='Add any special notes or instructions for this upload...'
                        ).classes('w-full').props('rows=3')
                    
                    ui.separator()
                    
                    # Action Buttons
                    with ui.row().classes('w-full justify-end gap-3 mt-4'):
                        ui.button('Cancel', icon='close', on_click=lambda: ui.navigate.to('/admin/dashboard')).props('outline color=grey')
                        ui.button(
                            'Process & Upload',
                            icon='auto_awesome',
                            on_click=lambda: handle_process_upload(trimester_select.value, department_select.value, notes.value)
                        ).props('color=primary').classes('px-8')
            
            # Upload History Card
            with ui.card().classes('w-full max-w-4xl p-8 shadow-lg mt-6'):
                ui.label('Recent Uploads').classes('text-xl font-semibold text-gray-800 mb-4')
                
                # Table
                with ui.column().classes('w-full gap-3'):
                    upload_history_item('Spring 2026', 'Computer Science and Engineering', '2024-01-15', '156 courses', 'success')
                    upload_history_item('Spring 2026', 'Data Science', '2024-01-14', '89 courses', 'success')
                    upload_history_item('Spring 2026', 'Electrical and Electronic Engineering', '2024-01-13', '134 courses', 'success')
                    upload_history_item('Fall 2025', 'Business Administration', '2023-09-10', '112 courses', 'success')

def nav_button(icon, label, link, active=False):
    """Create a navigation button"""
    classes = 'w-full justify-start'
    if active:
        classes += ' bg-[#ff6900]'
    
    with ui.button(icon=icon, on_click=lambda: ui.navigate.to(link) if link != '#' else None).props('flat align=left').classes(classes):
        ui.label(label).classes('ml-3')

def upload_history_item(trimester, department, date, courses, status):
    """Create an upload history item"""
    with ui.card().classes('w-full p-4 bg-gray-50 hover:bg-gray-100'):
        with ui.row().classes('w-full items-center justify-between'):
            with ui.row().classes('items-center gap-4 flex-1'):
                ui.icon('description', size='2rem').classes('text-[#ff6900]')
                with ui.column().classes('gap-1'):
                    ui.label(department).classes('font-semibold text-gray-800')
                    with ui.row().classes('gap-4'):
                        ui.label(f'📅 {trimester}').classes('text-sm text-gray-600')
                        ui.label(f'🗓️ {date}').classes('text-sm text-gray-600')
                        ui.label(f'📚 {courses}').classes('text-sm text-gray-600')
            
            with ui.row().classes('gap-2'):
                ui.badge('Processed', color='positive')
                ui.button(icon='visibility', on_click=lambda: None).props('flat round dense')
                ui.button(icon='download', on_click=lambda: None).props('flat round dense')
                ui.button(icon='delete', on_click=lambda: None).props('flat round dense color=negative')

def handle_file_upload(event, trimester, department):
    """Handle file upload event"""
    ui.notify(f'File uploaded for {department} - {trimester}', type='positive')

def handle_process_upload(trimester, department, notes):
    """Handle process and upload button click"""
    ui.notify(f'Processing course data for {department} ({trimester})...', type='info')
    # In real implementation, this would trigger AI analysis
    ui.notify('AI analysis in progress... (Design only)', type='info')
