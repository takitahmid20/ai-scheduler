from nicegui import ui

def create_file_status_card(file_name: str, uploaded: bool = False):
    """Create a card showing file upload status"""
    with ui.card().classes('p-4 border border-gray-200 rounded-lg'):
        with ui.row().classes('w-full items-center justify-between'):
            with ui.row().classes('items-center gap-3'):
                icon_name = 'check_circle' if uploaded else 'radio_button_unchecked'
                icon_color = 'green' if uploaded else 'gray'
                ui.icon(icon_name, size='sm').classes(f'text-{icon_color}-600')
                ui.label(file_name).classes('font-medium text-gray-800')
            
            if uploaded:
                ui.badge('Uploaded', color='green')
            else:
                ui.badge('Pending', color='gray')

def create_schedule_card(schedule_data: dict, on_favorite=None):
    """Create a schedule result card"""
    card = ui.card().classes('p-6 border-2 rounded-lg hover:shadow-lg transition-shadow')
    
    # Border color based on favorite
    if schedule_data.get('favorite'):
        card.classes('border-[#ff6900]')
    else:
        card.classes('border-gray-200')
    
    with card:
        with ui.row().classes('w-full items-center justify-between mb-4'):
            with ui.row().classes('items-center gap-3'):
                ui.label(schedule_data.get('title', 'Schedule')).classes('text-xl font-bold text-gray-800')
                
            with ui.row().classes('items-center gap-2'):
                if on_favorite:
                    icon_name = 'star' if schedule_data.get('favorite') else 'star_border'
                    ui.button(icon=icon_name, on_click=lambda: on_favorite(schedule_data['id'])).props('flat color=yellow-600')
                
                ui.button(icon='download', on_click=lambda: download_schedule(schedule_data)).props('flat color=orange')
        
        # Stats badges
        with ui.row().classes('gap-2 mb-4'):
            ui.badge(f"{schedule_data.get('conflicts', 0)} Conflicts", 
                    color='green' if schedule_data.get('conflicts', 0) == 0 else 'red')
            ui.badge(f"{schedule_data.get('free_days', 0)} Free Days", color='orange')
            ui.badge(f"{len(schedule_data.get('courses', []))} Courses", color='purple')
        
        # Courses list
        ui.label('Courses:').classes('font-semibold text-gray-700 mb-2')
        with ui.column().classes('gap-1'):
            for course in schedule_data.get('courses', []):
                if isinstance(course, str):
                    ui.label(f"• {course}").classes('text-gray-600')
                else:
                    ui.label(f"• {course.get('name', 'Unknown')} - {course.get('time', 'TBD')}").classes('text-gray-600')

def create_analysis_step_card(step_name: str, completed: bool = False, active: bool = False):
    """Create a card for analysis progress step"""
    with ui.card().classes('p-4 border border-gray-200 rounded-lg'):
        with ui.row().classes('items-center gap-3'):
            if completed:
                ui.icon('check_circle', size='sm').classes('text-green-600')
            elif active:
                ui.spinner(size='sm', color='orange')
            else:
                ui.icon('radio_button_unchecked', size='sm').classes('text-gray-400')
            
            label_class = 'font-medium text-gray-800' if active or completed else 'text-gray-500'
            ui.label(step_name).classes(label_class)

def create_stat_card(title: str, value: str, icon: str, color: str = 'orange'):
    """Create a statistics card"""
    with ui.card().classes(f'p-6 bg-{color}-50 border-l-4 border-{color}-500 rounded-lg'):
        with ui.column().classes('gap-2'):
            with ui.row().classes('items-center gap-2'):
                ui.icon(icon, size='md').classes(f'text-{color}-600')
                ui.label(title).classes('text-sm text-gray-600')
            ui.label(value).classes('text-2xl font-bold text-gray-800')

def download_schedule(schedule_data: dict):
    """Placeholder for schedule download"""
    ui.notify(f"Downloading {schedule_data.get('title')}...", type='info')
