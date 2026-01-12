from nicegui import ui
from components import (
    create_header, create_footer, create_primary_button
)

# Track uploaded files with their actual names
uploaded_files_list = []

def upload_page():
    """Upload page for data files"""
    ui.colors(primary='#2563eb')
    
    create_header('AI Academic Scheduler', 'Student Name')
    
    # Main container with better width
    with ui.column().classes('w-full items-center p-8'):
        # Centered content container
        with ui.column().classes('w-full max-w-4xl gap-8'):
            # Page title
            with ui.column().classes('w-full gap-2 mb-4'):
                ui.label('Upload Your Data').classes('text-3xl font-bold text-gray-800')
                ui.label('Upload your course, faculty, timeslot, and exam data to get started').classes('text-gray-600')
            
            # File upload card
            with ui.card().classes('w-full p-8 shadow-lg'):
                ui.label('Upload Course Data').classes('text-xl font-semibold text-gray-800 mb-2')
                ui.label('Upload your course offerings, faculty, timeslot, or exam data').classes('text-sm text-gray-500 mb-6')
                
                # Single upload area
                with ui.column().classes('w-full gap-4 mb-6'):
                    upload = ui.upload(
                        on_upload=lambda e: handle_file_upload(e),
                        multiple=True,
                        auto_upload=True
                    ).props('accept=".csv,.pdf"').classes('w-full')
                    upload.classes('border-2 border-dashed border-blue-400 rounded-lg p-8 bg-blue-50 hover:bg-blue-100 transition-colors cursor-pointer')
                    
                    with upload:
                        with ui.column().classes('items-center gap-2'):
                            ui.icon('cloud_upload', size='3rem').classes('text-blue-600')
                            ui.label('Drop files here or click to browse').classes('text-gray-700 font-medium text-lg')
                            ui.label('Supports CSV and PDF files').classes('text-sm text-gray-500')
                
                # File status list (only show if files uploaded)
                if len(uploaded_files_list) > 0:
                    ui.separator().classes('my-4')
                    
                    with ui.row().classes('w-full items-center justify-between mb-4'):
                        ui.label('Uploaded Files').classes('text-lg font-semibold text-gray-800')
                        ui.badge(f'{len(uploaded_files_list)} file(s)', color='primary')
                    
                    file_status_container = ui.column().classes('w-full gap-3')
                    
                    with file_status_container:
                        for file_info in uploaded_files_list:
                            with ui.row().classes('w-full items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200'):
                                with ui.row().classes('items-center gap-3'):
                                    ui.icon('check_circle', size='sm').classes('text-green-600')
                                    with ui.column().classes('gap-0'):
                                        ui.label(file_info['name']).classes('font-medium text-gray-800')
                                        if file_info.get('category'):
                                            ui.label(file_info['category']).classes('text-xs text-gray-500')
                                
                                ui.badge('✓ Uploaded', color='positive')
            
            # Preferences card
            with ui.card().classes('w-full p-8 shadow-lg'):
                ui.label('Schedule Preferences (Optional)').classes('text-xl font-semibold text-gray-800 mb-6')
                
                with ui.column().classes('w-full gap-6'):
                    # Time preference
                    with ui.column().classes('w-full gap-2'):
                        ui.label('Preferred Time').classes('text-sm font-medium text-gray-700')
                        time_pref = ui.select(
                            ['No Preference', 'Morning (8 AM - 12 PM)', 'Afternoon (12 PM - 4 PM)', 'Evening (4 PM - 8 PM)'],
                            value='No Preference'
                        ).classes('w-full')
                    
                    # Checkboxes
                    with ui.column().classes('w-full gap-3'):
                        avoid_conflicts = ui.checkbox('Prioritize exam conflict avoidance').classes('text-gray-700')
                        avoid_conflicts.value = True
                        max_free = ui.checkbox('Maximize free days').classes('text-gray-700')
                    
                    # Faculty preference
                    with ui.column().classes('w-full gap-2'):
                        ui.label('Preferred Faculty (optional, comma-separated)').classes('text-sm font-medium text-gray-700')
                        faculty = ui.input(placeholder='e.g. Dr. Smith, Prof. Johnson').classes('w-full')
            
            # Generate button
            with ui.row().classes('w-full justify-end mt-6'):
                create_primary_button(
                    'Generate Schedules',
                    on_click=lambda: handle_generate(),
                    icon='auto_awesome',
                    full_width=False
                ).classes('px-12 py-3 text-lg')
    
    create_footer()

def handle_file_upload(event):
    """Handle file upload"""
    # Get the file name from the event
    if hasattr(event, 'name'):
        file_name = event.name
    elif hasattr(event, 'file') and hasattr(event.file, 'name'):
        file_name = event.file.name
    else:
        file_name = 'uploaded_file'
    
    # Determine category based on filename
    file_name_lower = file_name.lower()
    category = None
    
    if 'course' in file_name_lower:
        category = 'Course Data'
    elif 'faculty' in file_name_lower or 'teacher' in file_name_lower or 'instructor' in file_name_lower:
        category = 'Faculty Data'
    elif 'timeslot' in file_name_lower or 'time' in file_name_lower or 'slot' in file_name_lower or 'schedule' in file_name_lower:
        category = 'Time Slots'
    elif 'exam' in file_name_lower:
        category = 'Exam Data'
    else:
        category = 'Course Data'  # Default
    
    # Add to uploaded files list
    uploaded_files_list.append({
        'name': file_name,
        'category': category
    })
    
    ui.notify(f'✓ {file_name} uploaded successfully!', type='positive')
    # Refresh page to show updated status
    ui.navigate.to('/upload')

def handle_generate():
    """Handle schedule generation"""
    
    if len(uploaded_files_list) == 0:
        ui.notify('⚠️ Please upload at least one course data file', type='warning')
    else:
        ui.notify(f'Processing {len(uploaded_files_list)} file(s)...', type='info')
        ui.navigate.to('/processing')
