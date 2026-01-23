from nicegui import ui, app
from components import (
    create_header, create_footer, create_primary_button, create_secondary_button
)
from io import BytesIO
from datetime import datetime

# Time slot mapping (in minutes from midnight) - matches database times
TIME_SLOTS = [
    {'label': '08:30 - 09:50', 'start': 510, 'end': 590},  # 8:30 AM
    {'label': '09:51 - 11:10', 'start': 591, 'end': 670},  # 9:51 AM
    {'label': '11:11 - 12:30', 'start': 671, 'end': 750},  # 11:11 AM
    {'label': '12:31 - 13:50', 'start': 751, 'end': 830},  # 12:31 PM
    {'label': '13:51 - 15:10', 'start': 831, 'end': 910},  # 1:51 PM
    {'label': '15:11 - 16:30', 'start': 911, 'end': 990},  # 3:11 PM
]

WEEKDAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

# Day name normalization mapping
DAY_MAPPING = {
    'Sat': 'Saturday',
    'Sun': 'Sunday',
    'Mon': 'Monday',
    'Tue': 'Tuesday',
    'Wed': 'Wednesday',
    'Thu': 'Thursday',
    'Fri': 'Friday'
}

def results_page():
    """Results page showing generated schedules with calendar view"""
    ui.colors(primary='#ff6900')
    
    user_name = app.storage.user.get('full_name', 'Student')
    
    create_header('AI Academic Scheduler', user_name)
    
    # Get generated schedules from session
    schedules = app.storage.user.get('generated_schedules', [])
    metadata = app.storage.user.get('generation_metadata', {})
    
    if not schedules:
        # No schedules generated
        with ui.column().classes('w-full items-center p-8'):
            with ui.card().classes('w-full max-w-2xl p-12 text-center'):
                ui.icon('error_outline', size='4rem').classes('text-gray-400 mb-4')
                ui.label('No schedules generated yet').classes('text-2xl font-bold text-gray-800 mb-2')
                ui.label('Please go back and generate schedules first').classes('text-gray-600 mb-6')
                create_primary_button(
                    'Go to Course Selection',
                    on_click=lambda: ui.navigate.to('/upload'),
                    icon='arrow_back'
                )
        return
    
    # Main container
    with ui.column().classes('w-full items-center p-8 bg-gray-50'):
        # Centered content container
        with ui.column().classes('w-full max-w-7xl gap-8'):
            # Header
            with ui.column().classes('w-full gap-2 mb-4'):
                ui.label('Your Optimal Schedules').classes('text-3xl font-bold text-gray-800')
                ui.label(f'We generated {len(schedules)} conflict-free schedule options based on your preferences').classes('text-gray-600')
            
            # Summary stats
            total_courses = metadata.get('total_courses', 0)
            with ui.row().classes('w-full gap-4 mb-4'):
                with ui.card().classes('flex-1 p-6 bg-orange-50 border-l-4 border-[#ff6900]'):
                    with ui.row().classes('items-center gap-4'):
                        ui.icon('menu_book', size='lg').classes('text-[#ff6900]')
                        with ui.column().classes('gap-1'):
                            ui.label('Total Courses').classes('text-sm text-gray-600')
                            ui.label(str(total_courses)).classes('text-2xl font-bold text-gray-800')
                
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
                            ui.label(str(len(schedules))).classes('text-2xl font-bold text-gray-800')
            
            # Schedule Options Tabs
            schedule_tabs = ui.tabs().classes('w-full')
            
            for idx, schedule in enumerate(schedules[:3], 1):  # Show best 3 options
                with schedule_tabs:
                    ui.tab(name=str(idx), label=f"Schedule {idx}")
            
            # Tab panels
            with ui.tab_panels(schedule_tabs, value='1').classes('w-full'):
                for idx, schedule in enumerate(schedules[:3], 1):
                    with ui.tab_panel(str(idx)):
                        render_calendar_view(schedule, idx)
            
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


def time_to_minutes(time_str):
    """Convert time string to minutes from midnight"""
    try:
        # Extract start time from range like "08:30 AM - 09:50 AM"
        if ' - ' in time_str:
            time_str = time_str.split(' - ')[0].strip()
        elif '-' in time_str:
            time_str = time_str.split('-')[0].strip()
        
        # Handle formats: "08:30 AM" or "08:30:AM"
        time_str = time_str.replace(':AM', ' AM').replace(':PM', ' PM')
        from datetime import datetime
        time_obj = datetime.strptime(time_str.strip(), '%I:%M %p')
        return time_obj.hour * 60 + time_obj.minute
    except Exception as e:
        print(f"Error parsing time '{time_str}': {e}")
        return 0

def get_time_duration(time_str):
    """Get duration in minutes from time range like '08:30 AM - 10:30 AM'"""
    try:
        if ' - ' in time_str:
            parts = time_str.split(' - ')
        elif '-' in time_str:
            parts = time_str.split('-')
        else:
            return 80  # Default duration
        
        start_str = parts[0].strip().replace(':AM', ' AM').replace(':PM', ' PM')
        end_str = parts[1].strip().replace(':AM', ' AM').replace(':PM', ' PM')
        
        from datetime import datetime
        start = datetime.strptime(start_str, '%I:%M %p')
        end = datetime.strptime(end_str, '%I:%M %p')
        
        duration = (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)
        return duration
    except:
        return 80

def normalize_day(day_str):
    """Normalize day name from various formats"""
    # Remove leading parenthesis or other special characters
    day_str = day_str.lstrip(')(')
    
    # Check if it's already a full day name
    if day_str in WEEKDAYS:
        return day_str
    
    # Try to map abbreviated form
    for abbr, full in DAY_MAPPING.items():
        if day_str.startswith(abbr) or abbr in day_str:
            return full
    
    return day_str

def find_time_slot(start_time):
    """Find which time slot index a start time falls into"""
    start_minutes = time_to_minutes(start_time)
    
    if start_minutes == 0:
        return None
    
    for idx, slot in enumerate(TIME_SLOTS):
        # Check if start time falls within this slot's range
        if slot['start'] <= start_minutes <= slot['end']:
            return idx
    
    return None

def convert_schedule_to_calendar(schedule):
    """Convert schedule with sections to calendar dictionary format
    
    Args:
        schedule: Dict with 'sections' key containing list of section dicts
                  and 'courses' key containing course metadata
    """
    calendar = {}
    
    # Get sections list and courses metadata from schedule
    sections = schedule.get('sections', [])
    courses = schedule.get('courses', [])
    
    print(f"Converting schedule with {len(sections)} sections and {len(courses)} courses")
    
    # Build course code to title mapping
    course_titles = {}
    for course in courses:
        course_titles[course['code']] = course.get('title', course['code'])
    
    for section in sections:
        # Each section may have day1/time1 and day2/time2
        course_type = section.get('course_type', 'Theory')
        course_code = section.get('course_code', '')
        course_title = course_titles.get(course_code, course_code)
        
        # Process day1/time1
        day1 = section.get('day1', '').strip()
        time1 = section.get('time1', '').strip()
        room1 = section.get('room1', '').strip()
        
        # Normalize day name
        day1 = normalize_day(day1)
        
        print(f"  Section {course_code} [{section.get('section')}]: day1={day1}, time1={time1}")
        
        if day1 and time1 and time1 != '-':
            slot_idx = find_time_slot(time1)
            print(f"    Slot index for {time1}: {slot_idx}")
            if slot_idx is not None:
                # Build calendar key
                if course_type == 'Lab':
                    calendar_key = f"{day1}_{slot_idx}_lab"
                else:
                    calendar_key = f"{day1}_{slot_idx}"
                
                # Add to calendar
                calendar[calendar_key] = {
                    'course': course_title,
                    'code': course_code,
                    'section': section.get('section', ''),
                    'faculty': section.get('faculty_name', ''),
                    'room': room1 or 'TBA',
                    'type': course_type,
                    'duration': get_time_duration(time1)  # Store actual duration
                }
        
        # Process day2/time2
        day2 = section.get('day2', '').strip()
        time2 = section.get('time2', '').strip()
        room2 = section.get('room2', '').strip()
        
        # Normalize day name
        day2 = normalize_day(day2)
        
        if day2 and time2 and time2 != '-':
            slot_idx = find_time_slot(time2)
            if slot_idx is not None:
                # Build calendar key
                if course_type == 'Lab':
                    calendar_key = f"{day2}_{slot_idx}_lab"
                else:
                    calendar_key = f"{day2}_{slot_idx}"
                
                # Add to calendar
                calendar[calendar_key] = {
                    'course': course_title,
                    'code': course_code,
                    'section': section.get('section', ''),
                    'faculty': section.get('faculty_name', ''),
                    'room': room2 or room1 or 'TBA',
                    'type': course_type,
                    'duration': get_time_duration(time2)  # Store actual duration
                }
    
    return calendar

def calculate_free_days(calendar):
    """Calculate number of free days in schedule"""
    days_with_classes = set()
    for key in calendar.keys():
        day = key.split('_')[0]
        days_with_classes.add(day)
    
    return len(WEEKDAYS) - len(days_with_classes)

def render_calendar_view(schedule, schedule_number):
    """Render weekly calendar timetable view"""
    # Convert sections list to calendar format
    calendar = convert_schedule_to_calendar(schedule)
    free_days = calculate_free_days(calendar)
    total_courses = len(set(c['code'] for c in calendar.values()))
    
    with ui.column().classes('w-full gap-4'):
        # Schedule header with actions
        with ui.row().classes('w-full items-center justify-between p-4 bg-white rounded-lg shadow-sm'):
            with ui.column().classes('gap-2'):
                ui.label(f'Schedule Option {schedule_number}').classes('text-2xl font-bold text-gray-800')
                with ui.row().classes('gap-3'):
                    ui.badge(f"✓ 0 Conflicts", color='positive').classes('text-sm')
                    ui.badge(f"📅 {free_days} Free Days", color='info').classes('text-sm')
                    ui.badge(f"📚 {total_courses} Courses", color='purple').classes('text-sm')
            
            with ui.row().classes('gap-2'):
                ui.button('Download PDF', icon='download', on_click=lambda s=schedule: download_schedule(s, schedule_number)).props('color=primary')
        
        # Calendar Timetable
        with ui.card().classes('w-full p-6 shadow-lg overflow-auto'):
            with ui.element('div').classes('min-w-[900px]'):
                # Calendar grid using CSS Grid
                with ui.element('div').style('display: grid; grid-template-columns: 120px repeat(6, 1fr); gap: 2px; background: #e5e7eb;'):
                    
                    # Header row - Time column + Days
                    ui.label('Time').classes('bg-[#ff6900] text-white p-3 font-bold text-center text-sm')
                    for day in WEEKDAYS:
                        ui.label(day).classes('bg-[#ff6900] text-white p-3 font-bold text-center text-sm')
                    
                    # Track which slots are occupied by labs
                    occupied_slots = set()
                    
                    # Time slot rows
                    for slot_idx, time_slot in enumerate(TIME_SLOTS):
                        # Time column
                        ui.label(time_slot['label']).classes('bg-gray-100 p-2 font-semibold text-xs text-gray-700 flex items-center justify-center text-center')
                        
                        # Day columns
                        for day in WEEKDAYS:
                            slot_key = f"{day}_{slot_idx}"
                            
                            # Skip if this slot is occupied by a lab from previous slot
                            if slot_key in occupied_slots:
                                continue
                            
                            course_key = f"{day}_{slot_idx}"
                            lab_key = f"{day}_{slot_idx}_lab"
                            
                            # Check if this slot has a course or lab
                            if course_key in calendar:
                                render_course_cell(calendar[course_key])
                            elif lab_key in calendar:
                                # Lab session - spans multiple time slots based on duration
                                lab_course = calendar[lab_key]
                                duration = lab_course.get('duration', 120)
                                # Each slot is ~80 minutes, calculate how many slots needed
                                slots_to_span = max(2, int(duration / 79))  # Labs typically span 2 slots
                                
                                render_course_cell(lab_course, is_lab=True, span_slots=slots_to_span)
                                # Mark next slots as occupied
                                for span_offset in range(1, slots_to_span):
                                    if slot_idx + span_offset < len(TIME_SLOTS):
                                        occupied_slots.add(f"{day}_{slot_idx + span_offset}")
                            else:
                                # Empty slot
                                ui.element('div').classes('bg-white p-2 min-h-[60px]')
        
        # Course List Section - Deduplicated
        with ui.card().classes('w-full p-6 mt-4 shadow-lg'):
            ui.label('Course Details').classes('text-xl font-bold text-gray-800 mb-4')
            
            # Deduplicate courses by code + section
            unique_courses = {}
            for course_key in calendar.keys():
                course = calendar[course_key]
                unique_key = f"{course['code']}_{course['section']}"
                if unique_key not in unique_courses:
                    unique_courses[unique_key] = course
            
            with ui.column().classes('w-full gap-3'):
                for unique_key in sorted(unique_courses.keys()):
                    course = unique_courses[unique_key]
                    
                    with ui.card().classes('p-4 bg-gray-50 border-l-4 border-[#ff6900]'):
                        with ui.row().classes('w-full items-center gap-4'):
                            # Section badge (prominent)
                            ui.badge(f"Section {course['section']}", color='orange').classes('text-lg font-bold px-4 py-2')
                            
                            # Course details
                            with ui.column().classes('gap-1 flex-1'):
                                with ui.row().classes('gap-2 items-center'):
                                    ui.label(course['code']).classes('text-lg font-bold text-gray-800')
                                    ui.label('•').classes('text-gray-400')
                                    ui.label(course['course']).classes('text-lg text-gray-700')
                                
                                with ui.row().classes('gap-2 items-center'):
                                    ui.icon('person', size='sm').classes('text-gray-600')
                                    ui.label(course['faculty']).classes('text-sm text-gray-600')
                                    ui.label('|').classes('text-gray-400 mx-1')
                                    ui.icon('meeting_room', size='sm').classes('text-gray-600')
                                    ui.label(course['room']).classes('text-sm text-gray-600')
                                    ui.badge(course['type'], color='primary').classes('text-xs ml-2')


def render_course_cell(course, is_lab=False, span_slots=1):
    """Render a single course cell in the calendar"""
    bg_color = 'bg-orange-100' if course['type'] == 'Lab' else 'bg-blue-50'
    border_color = 'border-l-4 border-orange-500' if course['type'] == 'Lab' else 'border-l-4 border-blue-500'
    
    # Lab spans multiple rows based on calculated span
    grid_row_span = f'grid-row: span {span_slots};' if span_slots > 1 else ''
    min_height = f'min-height: {60 * span_slots}px;'
    
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

def download_schedule(schedule_data, schedule_number: int):
    """Download schedule as PDF"""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        # Convert schedule to calendar format
        calendar = convert_schedule_to_calendar(schedule_data)
        
        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#ff6900'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(f"Schedule Option {schedule_number}", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Stats
        free_days = calculate_free_days(calendar)
        total_courses = len(set(c['code'] for c in calendar.values()))
        stats_text = f"<b>Courses:</b> {total_courses} | <b>Free Days:</b> {free_days} | <b>Conflicts:</b> 0"
        elements.append(Paragraph(stats_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Build calendar table
        data = [['Time', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']]
        
        for slot_idx, time_slot in enumerate(TIME_SLOTS):
            row = [Paragraph(f"<b>{time_slot['label']}</b>", styles['Normal'])]
            for day in WEEKDAYS:
                course_key = f"{day}_{slot_idx}"
                lab_key = f"{day}_{slot_idx}_lab"
                
                if course_key in calendar:
                    course = calendar[course_key]
                    cell_style = ParagraphStyle('CellStyle', fontSize=7, leading=9, alignment=TA_CENTER)
                    cell_text = f"<b>{course['code']} [{course['section']}]</b><br/>{course['course'][:25]}<br/><font size=6>{course['faculty']}</font>"
                    row.append(Paragraph(cell_text, cell_style))
                elif lab_key in calendar:
                    course = calendar[lab_key]
                    cell_style = ParagraphStyle('CellStyle', fontSize=7, leading=9, alignment=TA_CENTER)
                    cell_text = f"<b>{course['code']} [{course['section']}]</b><br/>{course['course'][:25]}<br/><font size=6>{course['faculty']}</font><br/><font color='orange'><b>(Lab)</b></font>"
                    row.append(Paragraph(cell_text, cell_style))
                else:
                    row.append('')
            data.append(row)
        
        # Create table with proper column widths
        table = Table(data, colWidths=[0.9*inch, 1.6*inch, 1.6*inch, 1.6*inch, 1.6*inch, 1.6*inch, 1.6*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6900')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Course Details Section
        course_header_style = ParagraphStyle(
            'CourseHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#ff6900'),
            spaceAfter=15,
            alignment=TA_LEFT
        )
        elements.append(Paragraph("Course Details", course_header_style))
        
        # Deduplicate courses
        unique_courses = {}
        for course_key in calendar.keys():
            course = calendar[course_key]
            unique_key = f"{course['code']}_{course['section']}"
            if unique_key not in unique_courses:
                unique_courses[unique_key] = course
        
        # Create course list
        for unique_key in sorted(unique_courses.keys()):
            course = unique_courses[unique_key]
            
            course_style = ParagraphStyle('CourseDetail', fontSize=10, leading=14, leftIndent=20)
            type_badge = 'L' if course['type'] == 'Lab' else 'T'
            
            course_text = f"""
            <b><font color='#ff6900' size=12>Section {course['section']}</font></b><br/>
            <b>{course['code']}</b> • {course['course']}<br/>
            <font size=9>{course['faculty']} | {course['room']} | <font color='#ff6900'><b>{type_badge}</b></font></font>
            """
            elements.append(Paragraph(course_text, course_style))
            elements.append(Spacer(1, 0.15*inch))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Download
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'schedule_{schedule_number}_{timestamp}.pdf'
        ui.download(buffer.getvalue(), filename)
        ui.notify(f'✓ Schedule {schedule_number} downloaded!', type='positive')
        
    except ImportError:
        ui.notify('⚠️ ReportLab not installed. Run: pip install reportlab', type='warning')
    except Exception as e:
        ui.notify(f'Error generating PDF: {str(e)}', type='negative')
        print(f"PDF generation error: {e}")

def download_all():
    """Download all schedules"""
    schedules = app.storage.user.get('generated_schedules', [])
    
    if not schedules:
        ui.notify('No schedules to download', type='warning')
        return
    
    ui.notify(f'Downloading {min(3, len(schedules))} schedules...', type='info')
    
    # Download first 3 schedules
    for idx, schedule in enumerate(schedules[:3], 1):
        download_schedule(schedule, idx)
