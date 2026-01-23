from nicegui import ui, app
from components import create_header, create_footer
from backend.database import SessionLocal
from backend.models import CourseOffering
from ai.schedule_generator import ScheduleGenerator
import asyncio

# Analysis steps
analysis_steps = [
    'Loading selected courses',
    'Fetching course sections',
    'Applying faculty preferences',
    'Detecting time conflicts',
    'Generating schedule combinations',
    'Scoring and ranking schedules',
]

def processing_page():
    """Processing page showing analysis progress"""
    ui.colors(primary='#ff6900')
    
    user_name = app.storage.user.get('full_name', 'Student')
    
    create_header('AI Academic Scheduler', user_name)
    
    # Main container with better width
    with ui.column().classes('w-full items-center p-8'):
        # Centered content container
        with ui.column().classes('w-full max-w-3xl gap-6'):
            # Page title
            with ui.column().classes('w-full gap-2 mb-4 text-center'):
                ui.label('Processing Your Data').classes('text-3xl font-bold text-gray-800')
                ui.label('Our AI is analyzing your data and generating optimal schedules...').classes('text-gray-600')
            
            # Processing card
            with ui.card().classes('w-full p-8 shadow-lg'):
                # Animated spinner
                with ui.column().classes('w-full items-center gap-4 mb-8'):
                    ui.spinner(size='xl', color='orange')
                
                # Progress steps
                step_cards = ui.column().classes('gap-4 w-full mb-8')
                
                with step_cards:
                    for step in analysis_steps:
                        with ui.row().classes('w-full items-center gap-4 p-4 bg-gray-50 rounded-lg'):
                            ui.icon('radio_button_unchecked', size='sm').classes('text-gray-400')
                            ui.label(step).classes('text-gray-500')
                
                # Progress bar
                ui.separator().classes('my-6')
                
                progress_container = ui.column().classes('w-full gap-3')
                with progress_container:
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('Overall Progress').classes('text-sm font-medium text-gray-700')
                        progress_label = ui.label('0%').classes('text-sm font-bold text-[#ff6900]')
                    progress_bar = ui.linear_progress(value=0).classes('w-full').props('size=8px color=primary')
        
        # Start processing simulation
        ui.timer(0.1, lambda: start_processing(step_cards, progress_bar, progress_label), once=True)
    
    create_footer()

async def start_processing(step_cards, progress_bar, progress_label):
    """Process schedule generation with visual updates"""
    
    try:
        # Step 1: Load selected courses
        await update_step(step_cards, progress_bar, progress_label, 0, "Loading selected courses...")
        
        schedule_request = app.storage.user.get('schedule_request', {})
        selected_course_codes = schedule_request.get('selected_course_codes', [])
        semester_id = schedule_request.get('semester_id')
        faculty_preferences = schedule_request.get('faculty_preferences', {})
        user_preferences = schedule_request.get('preferences', {})
        
        if not selected_course_codes:
            ui.notify('No courses selected. Please go back and select courses.', type='negative')
            await asyncio.sleep(2)
            ui.navigate.to('/upload')
            return
        
        # Step 2: Fetch course sections from database
        await update_step(step_cards, progress_bar, progress_label, 1, "Fetching course sections...")
        await asyncio.sleep(1)
        
        db = SessionLocal()
        try:
            courses_with_sections = []
            for course_code in selected_course_codes:
                # Get all sections for this course
                offerings = db.query(CourseOffering).filter(
                    CourseOffering.semester_id == semester_id,
                    CourseOffering.course_code == course_code
                ).all()
                
                if offerings:
                    sections = []
                    for offering in offerings:
                        section_data = {
                            'id': offering.id,
                            'section': offering.section,
                            'course_code': offering.course_code,
                            'course_type': offering.course_type,
                            'day1': offering.day1,
                            'day2': offering.day2,
                            'time1': offering.time1,
                            'time2': offering.time2,
                            'faculty_name': offering.faculty_name,
                            'room1': offering.room1,
                            'room2': offering.room2
                        }
                        sections.append(section_data)
                    
                    courses_with_sections.append({
                        'code': course_code,
                        'title': offerings[0].title,
                        'credit': offerings[0].credit,
                        'sections': sections
                    })
        finally:
            db.close()
        
        # Step 3: Apply faculty preferences
        await update_step(step_cards, progress_bar, progress_label, 2, "Applying faculty preferences...")
        await asyncio.sleep(1)
        
        # Filter sections based on faculty preferences if specified
        if faculty_preferences:
            for course in courses_with_sections:
                if course['code'] in faculty_preferences:
                    preferred_section_ids = faculty_preferences[course['code']]
                    if preferred_section_ids:  # If specific faculty selected
                        course['sections'] = [s for s in course['sections'] if s['id'] in preferred_section_ids]
        
        # Step 4: Initialize schedule generator
        await update_step(step_cards, progress_bar, progress_label, 3, "Detecting time conflicts...")
        await asyncio.sleep(0.5)
        
        generator = ScheduleGenerator(courses_with_sections, user_preferences)
        
        # Step 5: Generate schedules
        await update_step(step_cards, progress_bar, progress_label, 4, "Generating schedule combinations...")
        
        # Run generation in chunks to show progress
        schedules = await asyncio.to_thread(generator.generate_schedules, num_options=10)
        
        # Step 6: Score and rank
        await update_step(step_cards, progress_bar, progress_label, 5, "Scoring and ranking schedules...")
        await asyncio.sleep(0.5)
        
        if not schedules:
            ui.notify('⚠️ No valid schedules found. Conflicts detected between selected courses.', type='warning')
            await asyncio.sleep(3)
            ui.navigate.to('/upload')
            return
        
        # Store results in session
        app.storage.user['generated_schedules'] = schedules
        app.storage.user['generation_metadata'] = {
            'total_courses': len(selected_course_codes),
            'total_schedules': len(schedules),
            'preferences_applied': user_preferences
        }
        
        # Complete
        progress_bar.value = 1.0
        progress_label.text = '100%'
        
        ui.notify(f'✓ Generated {len(schedules)} valid schedule options!', type='positive')
        await asyncio.sleep(1)
        ui.navigate.to('/results')
        
    except Exception as e:
        ui.notify(f'Error generating schedules: {str(e)}', type='negative')
        print(f"Processing error: {e}")
        await asyncio.sleep(3)
        ui.navigate.to('/upload')


async def update_step(step_cards, progress_bar, progress_label, current_step, message):
    """Update progress display"""
    total_steps = len(analysis_steps)
    progress = (current_step + 1) / total_steps
    
    progress_bar.value = progress
    progress_label.text = f'{int(progress * 100)}%'
    
    # Update step cards
    step_cards.clear()
    with step_cards:
        for j, step in enumerate(analysis_steps):
            with ui.row().classes('w-full items-center gap-4 p-4 bg-gray-50 rounded-lg'):
                if j < current_step:
                    ui.icon('check_circle', size='sm').classes('text-green-600')
                    ui.label(step).classes('text-gray-700 font-medium')
                elif j == current_step:
                    ui.spinner(size='sm', color='orange')
                    ui.label(step).classes('text-[#ff6900] font-semibold')
                else:
                    ui.icon('radio_button_unchecked', size='sm').classes('text-gray-400')
                    ui.label(step).classes('text-gray-500')
    
    await asyncio.sleep(0.5)
