from nicegui import ui
from components import create_header, create_footer
import asyncio

# Analysis steps
analysis_steps = [
    'Reading uploaded files',
    'Extracting course data',
    'Analyzing constraints',
    'Checking exam conflicts',
    'Generating optimal schedules',
]

def processing_page():
    """Processing page showing analysis progress"""
    ui.colors(primary='#2563eb')
    
    create_header('AI Academic Scheduler', 'Student Name')
    
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
                    ui.spinner(size='xl', color='blue')
                
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
                        progress_label = ui.label('0%').classes('text-sm font-bold text-blue-600')
                    progress_bar = ui.linear_progress(value=0).classes('w-full').props('size=8px color=primary')
        
        # Start processing simulation
        ui.timer(0.1, lambda: start_processing(step_cards, progress_bar, progress_label), once=True)
    
    create_footer()

async def start_processing(step_cards, progress_bar, progress_label):
    """Simulate processing with visual updates"""
    total_steps = len(analysis_steps)
    
    for i, step in enumerate(analysis_steps):
        await asyncio.sleep(2)  # Simulate processing time
        
        # Update progress
        progress = ((i + 1) / total_steps)
        progress_bar.value = progress
        progress_label.text = f'{int(progress * 100)}%'
        
        # Update step cards
        step_cards.clear()
        with step_cards:
            for j, s in enumerate(analysis_steps):
                with ui.row().classes('w-full items-center gap-4 p-4 bg-gray-50 rounded-lg'):
                    if j < i:
                        ui.icon('check_circle', size='sm').classes('text-green-600')
                        ui.label(s).classes('text-gray-700 font-medium')
                    elif j == i:
                        ui.spinner(size='sm', color='blue')
                        ui.label(s).classes('text-blue-600 font-semibold')
                    else:
                        ui.icon('radio_button_unchecked', size='sm').classes('text-gray-400')
                        ui.label(s).classes('text-gray-500')
    
    # Complete - navigate to results
    await asyncio.sleep(1)
    ui.notify('✓ Schedules generated successfully!', type='positive')
    ui.navigate.to('/results')
