from nicegui import ui
from components import (
    create_header, create_footer, create_primary_button, create_secondary_button
)

# Mock schedule results
mock_results = [
    {
        'id': 1,
        'title': 'Schedule Option 1',
        'favorite': True,
        'conflicts': 0,
        'free_days': 2,
        'courses': [
            {'name': 'Database Systems', 'time': 'Mon/Wed 10:00-11:30 AM', 'faculty': 'Dr. Smith'},
            {'name': 'AI & Machine Learning', 'time': 'Tue/Thu 2:00-3:30 PM', 'faculty': 'Prof. Johnson'},
            {'name': 'Computer Networks', 'time': 'Mon/Wed 2:00-3:30 PM', 'faculty': 'Dr. Williams'},
            {'name': 'Software Engineering', 'time': 'Tue/Thu 10:00-11:30 AM', 'faculty': 'Dr. Brown'},
            {'name': 'Data Structures', 'time': 'Fri 9:00-12:00 PM', 'faculty': 'Prof. Davis'},
        ]
    },
    {
        'id': 2,
        'title': 'Schedule Option 2',
        'favorite': False,
        'conflicts': 0,
        'free_days': 1,
        'courses': [
            {'name': 'Database Systems', 'time': 'Tue/Thu 9:00-10:30 AM', 'faculty': 'Dr. Smith'},
            {'name': 'AI & Machine Learning', 'time': 'Mon/Wed 1:00-2:30 PM', 'faculty': 'Dr. Lee'},
            {'name': 'Computer Networks', 'time': 'Tue/Thu 11:00-12:30 PM', 'faculty': 'Dr. Williams'},
            {'name': 'Software Engineering', 'time': 'Mon/Wed 3:00-4:30 PM', 'faculty': 'Dr. Brown'},
            {'name': 'Data Structures', 'time': 'Fri 2:00-5:00 PM', 'faculty': 'Prof. Davis'},
        ]
    }
]

favorites = {1: True, 2: False}

def results_page():
    """Results page showing generated schedules"""
    ui.colors(primary='#2563eb')
    
    create_header('AI Academic Scheduler', 'Student Name')
    
    # Main container with better width
    with ui.column().classes('w-full items-center p-8'):
        # Centered content container
        with ui.column().classes('w-full max-w-5xl gap-8'):
            # Header
            with ui.column().classes('w-full gap-2 mb-4'):
                ui.label('Your Optimal Schedules').classes('text-3xl font-bold text-gray-800')
                ui.label('We generated 2 conflict-free schedule options based on your preferences').classes('text-gray-600')
            
            # Summary stats
            with ui.row().classes('w-full gap-4 mb-4'):
                # Stat card 1
                with ui.card().classes('flex-1 p-6 bg-blue-50 border-l-4 border-blue-500'):
                    with ui.row().classes('items-center gap-3'):
                        ui.icon('menu_book', size='lg').classes('text-blue-600')
                        with ui.column().classes('gap-1'):
                            ui.label('Total Courses').classes('text-sm text-gray-600')
                            ui.label('5').classes('text-2xl font-bold text-gray-800')
                
                # Stat card 2
                with ui.card().classes('flex-1 p-6 bg-green-50 border-l-4 border-green-500'):
                    with ui.row().classes('items-center gap-3'):
                        ui.icon('check_circle', size='lg').classes('text-green-600')
                        with ui.column().classes('gap-1'):
                            ui.label('Zero Conflicts').classes('text-sm text-gray-600')
                            ui.label('✓').classes('text-2xl font-bold text-gray-800')
                
                # Stat card 3
                with ui.card().classes('flex-1 p-6 bg-purple-50 border-l-4 border-purple-500'):
                    with ui.row().classes('items-center gap-3'):
                        ui.icon('auto_awesome', size='lg').classes('text-purple-600')
                        with ui.column().classes('gap-1'):
                            ui.label('Options Generated').classes('text-sm text-gray-600')
                            ui.label('2').classes('text-2xl font-bold text-gray-800')
            
            # Schedule cards
            schedule_container = ui.column().classes('w-full gap-6')
            
            with schedule_container:
                for schedule in mock_results:
                    schedule['favorite'] = favorites.get(schedule['id'], False)
                    
                    # Custom schedule card
                    border_class = 'border-blue-500 border-2' if schedule['favorite'] else 'border-gray-200'
                    with ui.card().classes(f'w-full p-6 {border_class} shadow-md hover:shadow-lg transition-shadow'):
                        # Card header
                        with ui.row().classes('w-full items-center justify-between mb-4'):
                            ui.label(schedule['title']).classes('text-2xl font-bold text-gray-800')
                            
                            with ui.row().classes('items-center gap-2'):
                                icon = 'star' if schedule['favorite'] else 'star_border'
                                ui.button(icon=icon, on_click=lambda s=schedule: toggle_favorite(s['id'])).props('flat color=yellow-600 size=md')
                                ui.button(icon='download', on_click=lambda s=schedule: download_schedule(s)).props('flat color=blue-600 size=md')
                        
                        # Stats badges
                        with ui.row().classes('gap-3 mb-6'):
                            conflict_color = 'positive' if schedule['conflicts'] == 0 else 'negative'
                            ui.badge(f"{schedule['conflicts']} Conflicts", color=conflict_color).classes('text-sm px-3 py-1')
                            ui.badge(f"{schedule['free_days']} Free Days", color='info').classes('text-sm px-3 py-1')
                            ui.badge(f"{len(schedule['courses'])} Courses", color='purple').classes('text-sm px-3 py-1')
                        
                        # Courses table
                        ui.label('Course Schedule:').classes('font-semibold text-gray-700 mb-3')
                        
                        with ui.column().classes('w-full gap-2'):
                            for course in schedule['courses']:
                                with ui.row().classes('w-full p-3 bg-gray-50 rounded-lg border border-gray-200'):
                                    with ui.column().classes('flex-1 gap-1'):
                                        ui.label(course['name']).classes('font-semibold text-gray-800')
                                        with ui.row().classes('gap-4 text-sm'):
                                            ui.label(f"⏰ {course['time']}").classes('text-gray-600')
                                            ui.label(f"👨‍🏫 {course['faculty']}").classes('text-gray-600')
            
            # Action buttons
            with ui.row().classes('w-full justify-between mt-6'):
                create_secondary_button(
                    'Upload New Data',
                    on_click=lambda: ui.navigate.to('/upload'),
                    icon='upload'
                )
                
                create_primary_button(
                    'Download All',
                    on_click=lambda: download_all(),
                    icon='download'
                )
    
    create_footer()

def toggle_favorite(schedule_id: int):
    """Toggle favorite status"""
    favorites[schedule_id] = not favorites.get(schedule_id, False)
    ui.notify('Favorite updated!', type='info')
    ui.navigate.to('/results')

def download_schedule(schedule_data: dict):
    """Placeholder for schedule download"""
    ui.notify(f"Downloading {schedule_data.get('title')}...", type='info')

def download_all():
    """Download all schedules - placeholder"""
    ui.notify('Downloading all schedules...', type='positive')
