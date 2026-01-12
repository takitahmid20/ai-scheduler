from nicegui import ui

def create_input_field(label: str, placeholder: str = '', password: bool = False):
    """Create a styled input field"""
    with ui.column().classes('w-full gap-1'):
        ui.label(label).classes('text-sm font-medium text-gray-700')
        input_field = ui.input(placeholder=placeholder).classes('w-full')
        if password:
            input_field.props('type=password')
        return input_field

def create_file_upload(label: str, on_upload, accepted_types: list = None):
    """Create a file upload component"""
    with ui.column().classes('w-full gap-2'):
        ui.label(label).classes('text-sm font-medium text-gray-700')
        
        upload = ui.upload(
            on_upload=on_upload,
            auto_upload=True
        ).classes('w-full border-2 border-dashed border-gray-300 rounded-lg p-4')
        
        if accepted_types:
            upload.props(f'accept="{",".join(accepted_types)}"')
        
        return upload

def create_checkbox(label: str, value: bool = False):
    """Create a styled checkbox"""
    checkbox = ui.checkbox(label).classes('text-gray-700')
    checkbox.value = value
    return checkbox

def create_select(label: str, options: list, value=None):
    """Create a styled select dropdown"""
    with ui.column().classes('w-full gap-1'):
        ui.label(label).classes('text-sm font-medium text-gray-700')
        select = ui.select(options, value=value).classes('w-full')
        return select

def create_preference_form():
    """Create preference form for schedule generation"""
    preferences = {}
    
    with ui.column().classes('w-full gap-4'):
        ui.label('Schedule Preferences (Optional)').classes('text-lg font-semibold text-gray-800')
        
        preferences['time_preference'] = create_select(
            'Preferred Time',
            ['No Preference', 'Morning (8 AM - 12 PM)', 'Afternoon (12 PM - 4 PM)', 'Evening (4 PM - 8 PM)'],
            value='No Preference'
        )
        
        preferences['avoid_conflicts'] = create_checkbox('Prioritize exam conflict avoidance', True)
        preferences['max_free_days'] = create_checkbox('Maximize free days', False)
        
        with ui.column().classes('w-full gap-1'):
            ui.label('Preferred Faculty (optional, comma-separated)').classes('text-sm font-medium text-gray-700')
            preferences['faculty'] = ui.input(placeholder='e.g. Dr. Smith, Prof. Johnson').classes('w-full')
    
    return preferences
