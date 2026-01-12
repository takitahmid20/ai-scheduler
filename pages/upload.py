from nicegui import ui
from components import (
    create_header, create_footer, create_primary_button
)

# Mock uploaded file state
uploaded_files = {
    'courses.csv': False,
    'faculty.csv': False,
    'timeslots.csv': False,
    'exams.csv': False,
}

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
                ui.label('Required Files').classes('text-xl font-semibold text-gray-800 mb-6')
                
                # Single upload area
                with ui.column().classes('w-full gap-4 mb-6'):
                    ui.label('Upload Files (CSV/PDF)').classes('text-sm font-medium text-gray-700')
                    upload = ui.upload(
                        on_upload=lambda e: handle_file_upload(e),
                        multiple=True,
                        auto_upload=True
                    ).props('accept=".csv,.pdf"').classes('w-full')
                    upload.classes('border-2 border-dashed border-blue-400 rounded-lg p-8 bg-blue-50')
                    
                    with upload:
                        with ui.column().classes('items-center gap-2'):
                            ui.icon('cloud_upload', size='3rem').classes('text-blue-600')
                            ui.label('Drop files here or click to browse').classes('text-gray-700 font-medium')
                            ui.label('Supports CSV and PDF files').classes('text-sm text-gray-500')
                
                ui.separator()
                
                # File status list
                ui.label('Uploaded Files').classes('text-lg font-semibold text-gray-800 mt-6 mb-4')
                file_status_container = ui.column().classes('w-full gap-3')
                
                with file_status_container:
                    for file_name, status in uploaded_files.items():
                        with ui.row().classes('w-full items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200'):
                            with ui.row().classes('items-center gap-3'):
                                icon = 'check_circle' if status else 'radio_button_unchecked'
                                color = 'text-green-600' if status else 'text-gray-400'
                                ui.icon(icon, size='sm').classes(color)
                                ui.label(file_name).classes('font-medium text-gray-800')
                            
                            badge_color = 'positive' if status else 'grey'
                            badge_text = '✓ Uploaded' if status else 'Pending'
                            ui.badge(badge_text, color=badge_color)
            
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
    file_name = event.name.lower()
    
    # Match uploaded file to required files
    if 'course' in file_name:
        uploaded_files['courses.csv'] = True
    elif 'faculty' in file_name or 'teacher' in file_name:
        uploaded_files['faculty.csv'] = True
    elif 'timeslot' in file_name or 'time' in file_name or 'slot' in file_name:
        uploaded_files['timeslots.csv'] = True
    elif 'exam' in file_name:
        uploaded_files['exams.csv'] = True
    
    ui.notify(f'✓ {event.name} uploaded successfully!', type='positive')
    # Refresh page to show updated status
    ui.navigate.to('/upload')

def handle_generate():
    """Handle schedule generation"""
    uploaded_count = sum(uploaded_files.values())
    
    if uploaded_count < 4:
        ui.notify(f'Please upload all required files ({uploaded_count}/4 uploaded)', type='warning')
    else:
        ui.notify('Processing your data...', type='info')
        ui.navigate.to('/processing')
