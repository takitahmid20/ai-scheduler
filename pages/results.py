from nicegui import ui, app
from components import (
    create_header, create_footer, create_primary_button, create_secondary_button
)
from backend.constants import WEEKDAYS, TIME_SLOTS

# Mock schedule results with calendar-based data
mock_results = [
    {
        'id': 1,
        'title': 'Schedule Option 1',
        'favorite': True,
        'conflicts': 0,
        'free_days': 2,
        'calendar': {
            # Format: 'day_timeslot': {'course': 'name', 'code': 'CSE1234', 'section': 'A', 'faculty': 'name', 'room': 'room', 'type': 'Theory/Lab'}
            # Sat-Tue aligned (same classes same time)
            'Saturday_0': {'course': 'Database Systems', 'code': 'CSE 3101', 'section': 'A', 'faculty': 'Dr. Smith', 'room': 'NAC 501', 'type': 'Theory'},
            'Tuesday_0': {'course': 'Database Systems', 'code': 'CSE 3101', 'section': 'A', 'faculty': 'Dr. Smith', 'room': 'NAC 501', 'type': 'Theory'},
            
            'Saturday_2': {'course': 'Computer Networks', 'code': 'CSE 3201', 'section': 'B', 'faculty': 'Dr. Williams', 'room': 'NAC 502', 'type': 'Theory'},
            'Tuesday_2': {'course': 'Computer Networks', 'code': 'CSE 3201', 'section': 'B', 'faculty': 'Dr. Williams', 'room': 'NAC 502', 'type': 'Theory'},
            
            # Sun-Wed aligned (same classes same time)
            'Sunday_1': {'course': 'AI & Machine Learning', 'code': 'CSE 4101', 'section': 'A', 'faculty': 'Prof. Johnson', 'room': 'NAC 601', 'type': 'Theory'},
            'Wednesday_1': {'course': 'AI & Machine Learning', 'code': 'CSE 4101', 'section': 'A', 'faculty': 'Prof. Johnson', 'room': 'NAC 601', 'type': 'Theory'},
            
            'Sunday_3': {'course': 'Software Engineering', 'code': 'CSE 3301', 'section': 'C', 'faculty': 'Dr. Brown', 'room': 'NAC 503', 'type': 'Theory'},
            'Wednesday_3': {'course': 'Software Engineering', 'code': 'CSE 3301', 'section': 'C', 'faculty': 'Dr. Brown', 'room': 'NAC 503', 'type': 'Theory'},
            
            # Lab on Saturday (spans 2 slots: slot 4 and 5)
            'Saturday_4_lab': {'course': 'Data Structures Lab', 'code': 'CSE 2216', 'section': 'A', 'faculty': 'Prof. Davis', 'room': 'Lab 301', 'type': 'Lab', 'span': 2},
        }
    },
    {
        'id': 2,
        'title': 'Schedule Option 2',
        'favorite': False,
        'conflicts': 0,
        'free_days': 1,
        'calendar': {
            # Sat-Tue aligned (same classes same time)
            'Saturday_1': {'course': 'Software Engineering', 'code': 'CSE 3301', 'section': 'C', 'faculty': 'Dr. Brown', 'room': 'NAC 503', 'type': 'Theory'},
            'Tuesday_1': {'course': 'Software Engineering', 'code': 'CSE 3301', 'section': 'C', 'faculty': 'Dr. Brown', 'room': 'NAC 503', 'type': 'Theory'},
            
            'Saturday_4': {'course': 'Computer Networks', 'code': 'CSE 3201', 'section': 'B', 'faculty': 'Dr. Williams', 'room': 'NAC 502', 'type': 'Theory'},
            'Tuesday_4': {'course': 'Computer Networks', 'code': 'CSE 3201', 'section': 'B', 'faculty': 'Dr. Williams', 'room': 'NAC 502', 'type': 'Theory'},
            
            # Sun-Wed aligned (same classes same time)
            'Sunday_0': {'course': 'Database Systems', 'code': 'CSE 3101', 'section': 'A', 'faculty': 'Dr. Smith', 'room': 'NAC 501', 'type': 'Theory'},
            'Wednesday_0': {'course': 'Database Systems', 'code': 'CSE 3101', 'section': 'A', 'faculty': 'Dr. Smith', 'room': 'NAC 501', 'type': 'Theory'},
            
            'Sunday_3': {'course': 'AI & Machine Learning', 'code': 'CSE 4101', 'section': 'A', 'faculty': 'Dr. Lee', 'room': 'NAC 602', 'type': 'Theory'},
            'Wednesday_3': {'course': 'AI & Machine Learning', 'code': 'CSE 4101', 'section': 'A', 'faculty': 'Dr. Lee', 'room': 'NAC 602', 'type': 'Theory'},
            
            # Lab on Sunday (spans 2 slots)
            'Sunday_2_lab': {'course': 'Data Structures Lab', 'code': 'CSE 2216', 'section': 'A', 'faculty': 'Prof. Davis', 'room': 'Lab 301', 'type': 'Lab', 'span': 2},
        }
    }
]

favorites = {1: True, 2: False}

def results_page():
    """Results page showing generated schedules with calendar view"""
    ui.colors(primary='#ff6900')
    
    user_name = app.storage.user.get('full_name', 'Student')
    
    create_header('AI Academic Scheduler', user_name)
    
    # Main container
    with ui.column().classes('w-full items-center p-8 bg-gray-50'):
        # Centered content container
        with ui.column().classes('w-full max-w-7xl gap-8'):
            # Header
            with ui.column().classes('w-full gap-2 mb-4'):
                ui.label('Your Optimal Schedules').classes('text-3xl font-bold text-gray-800')
                ui.label('We generated 2 conflict-free schedule options based on your preferences').classes('text-gray-600')
            
            # Summary stats
            with ui.row().classes('w-full gap-4 mb-4'):
                with ui.card().classes('flex-1 p-6 bg-orange-50 border-l-4 border-[#ff6900]'):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('menu_book', size='lg').classes('text-[#ff6900]')
                        with ui.column().classes('gap-1'):
                            ui.label('Total Courses').classes('text-sm text-gray-600')
                            ui.label('5').classes('text-2xl font-bold text-gray-800')
                
                with ui.card().classes('flex-1 p-6 bg-green-50 border-l-4 border-green-500'):
                    with ui.row().classes('items-center gap-3'):
                        ui.icon('check_circle', size='lg').classes('text-green-600')
                        with ui.column().classes('gap-1'):
                            ui.label('Zero Conflicts').classes('text-sm text-gray-600')
                            ui.label('✓').classes('text-2xl font-bold text-gray-800')
                
                with ui.card().classes('flex-1 p-6 bg-purple-50 border-l-4 border-purple-500'):
                    with ui.row().classes('items-center gap-3'):
                        ui.icon('auto_awesome', size='lg').classes('text-purple-600')
                        with ui.column().classes('gap-1'):
                            ui.label('Options Generated').classes('text-sm text-gray-600')
                            ui.label('2').classes('text-2xl font-bold text-gray-800')
            
            # Schedule Options Tabs
            schedule_tabs = ui.tabs().classes('w-full')
            
            for schedule in mock_results:
                schedule['favorite'] = favorites.get(schedule['id'], False)
                star_icon = '⭐' if schedule['favorite'] else '☆'
                with schedule_tabs:
                    ui.tab(name=str(schedule['id']), label=f"{star_icon} {schedule['title']}")
            
            # Tab panels
            with ui.tab_panels(schedule_tabs, value='1').classes('w-full'):
                for schedule in mock_results:
                    with ui.tab_panel(str(schedule['id'])):
                        render_calendar_view(schedule)
            
            # Action buttons
            with ui.row().classes('w-full justify-between mt-6'):
                create_secondary_button(
                    'Upload New Data',
                    on_click=lambda: ui.navigate.to('/upload'),
                    icon='upload'
                )
                
                create_primary_button(
                    'Download All Schedules',
                    on_click=lambda: download_all(),
                    icon='download'
                )
    
    create_footer()


def render_calendar_view(schedule):
    """Render weekly calendar timetable view"""
    with ui.column().classes('w-full gap-4'):
        # Schedule header with actions
        with ui.row().classes('w-full items-center justify-between p-4 bg-white rounded-lg shadow-sm'):
            with ui.column().classes('gap-2'):
                ui.label(schedule['title']).classes('text-2xl font-bold text-gray-800')
                with ui.row().classes('gap-3'):
                    conflict_color = 'positive' if schedule['conflicts'] == 0 else 'negative'
                    ui.badge(f"✓ {schedule['conflicts']} Conflicts", color=conflict_color).classes('text-sm')
                    ui.badge(f"📅 {schedule['free_days']} Free Days", color='info').classes('text-sm')
                    total_courses = len([k for k in schedule['calendar'].keys() if not k.endswith('_lab')])
                    ui.badge(f"📚 {total_courses} Courses", color='purple').classes('text-sm')
            
            with ui.row().classes('gap-2'):
                icon = 'star' if schedule['favorite'] else 'star_border'
                color = 'yellow' if schedule['favorite'] else 'grey'
                ui.button(icon=icon, on_click=lambda s=schedule: toggle_favorite(s['id'])).props(f'flat color={color} size=md').classes('text-lg')
                ui.button('Download PDF', icon='download', on_click=lambda s=schedule: download_schedule(s)).props('color=primary')
        
        # Calendar Timetable
        with ui.card().classes('w-full p-6 shadow-lg overflow-auto'):
            with ui.element('div').classes('min-w-[900px]'):
                # Calendar grid using CSS Grid
                with ui.element('div').style('display: grid; grid-template-columns: 120px repeat(7, 1fr); gap: 2px; background: #e5e7eb;'):
                    
                    # Header row - Time column + Days
                    ui.label('Time').classes('bg-[#ff6900] text-white p-3 font-bold text-center text-sm')
                    for day in WEEKDAYS:
                        ui.label(day).classes('bg-[#ff6900] text-white p-3 font-bold text-center text-sm')
                    
                    # Track which slots are occupied by labs
                    occupied_slots = set()
                    
                    # Time slot rows
                    for slot_idx, time_slot in enumerate(TIME_SLOTS):
                        # Time column
                        ui.label(time_slot).classes('bg-gray-100 p-2 font-semibold text-xs text-gray-700 flex items-center justify-center text-center')
                        
                        # Day columns
                        for day in WEEKDAYS:
                            slot_key = f"{day}_{slot_idx}"
                            
                            # Skip if this slot is occupied by a lab from previous slot
                            if slot_key in occupied_slots:
                                continue
                            
                            course_key = f"{day}_{slot_idx}"
                            lab_key = f"{day}_{slot_idx}_lab"
                            
                            # Check if this slot has a course or lab
                            if course_key in schedule['calendar']:
                                render_course_cell(schedule['calendar'][course_key])
                            elif lab_key in schedule['calendar']:
                                # Lab session - spans 2 time slots
                                render_course_cell(schedule['calendar'][lab_key], is_lab=True)
                                # Mark next slot as occupied
                                if slot_idx + 1 < len(TIME_SLOTS):
                                    occupied_slots.add(f"{day}_{slot_idx + 1}")
                            else:
                                # Empty slot
                                ui.element('div').classes('bg-white p-2 min-h-[60px]')


def render_course_cell(course, is_lab=False):
    """Render a single course cell in the calendar"""
    bg_color = 'bg-orange-100' if course['type'] == 'Lab' else 'bg-blue-50'
    border_color = 'border-l-4 border-orange-500' if course['type'] == 'Lab' else 'border-l-4 border-blue-500'
    
    # Lab spans 2 rows
    grid_row_span = 'grid-row: span 2;' if is_lab else ''
    min_height = 'min-height: 130px;' if is_lab else 'min-height: 60px;'
    
    with ui.card().classes(f'p-2 {bg_color} {border_color} shadow-sm hover:shadow-md transition-shadow cursor-pointer').style(f'margin: 0; {grid_row_span} {min_height}'):
        with ui.column().classes('gap-1 w-full'):
            # Course code and section
            ui.label(f"{course['code']} [{course['section']}]").classes('font-bold text-xs text-gray-800')
            # Course name
            ui.label(course['course']).classes('text-xs text-gray-700 font-medium line-clamp-2')
            # Faculty
            ui.label(f"👨‍🏫 {course['faculty']}").classes('text-xs text-gray-600')
            # Room
            ui.label(f"📍 {course['room']}").classes('text-xs text-gray-600')
            # Type badge
            badge_color = 'orange' if course['type'] == 'Lab' else 'primary'
            ui.badge(course['type'], color=badge_color).classes('text-xs')

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
