from nicegui import ui
import asyncio

def create_loading_spinner(text: str = 'Loading...'):
    """Create a loading spinner with text"""
    with ui.column().classes('items-center gap-3'):
        ui.spinner(size='lg', color='orange')
        ui.label(text).classes('text-gray-600')

def create_progress_bar(progress: float, text: str = ''):
    """Create a progress bar (0-100)"""
    with ui.column().classes('w-full gap-2'):
        if text:
            ui.label(text).classes('text-sm text-gray-600')
        ui.linear_progress(value=progress / 100).classes('w-full')
        ui.label(f'{int(progress)}%').classes('text-xs text-gray-500 text-right')

def create_skeleton_card():
    """Create a skeleton loading card"""
    with ui.card().classes('p-6 w-full'):
        with ui.column().classes('gap-3 w-full'):
            ui.skeleton().classes('h-6 w-3/4 bg-gray-200 rounded')
            ui.skeleton().classes('h-4 w-full bg-gray-200 rounded')
            ui.skeleton().classes('h-4 w-5/6 bg-gray-200 rounded')
            ui.skeleton().classes('h-4 w-4/6 bg-gray-200 rounded')

async def simulate_processing(steps: list, step_callback):
    """Simulate processing steps with delays"""
    for i, step in enumerate(steps):
        await asyncio.sleep(1.5)  # Simulate processing time
        step_callback(i)
