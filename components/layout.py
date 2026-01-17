from nicegui import ui, app

def create_header(title: str, user_name: str = None):
    """Create app header with title and optional user info"""
    with ui.header().classes('bg-white border-b border-gray-200 shadow-sm'):
        with ui.row().classes('w-full items-center justify-between px-6 py-3'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('school', size='md').classes('text-[#ff6900]')
                ui.label(title).classes('text-xl font-bold text-gray-800')
            
            if user_name:
                with ui.row().classes('items-center gap-3'):
                    with ui.button(icon='account_circle', on_click=lambda: ui.navigate.to('/profile')).props('flat'):
                        ui.label(user_name).classes('ml-2 text-gray-700')
                    ui.button('Logout', on_click=handle_logout).props('flat color=red-600 icon=logout')

def handle_logout():
    """Handle user logout"""
    app.storage.user.clear()
    ui.notify('Logged out successfully', type='info')
    ui.navigate.to('/signin')

def create_footer():
    """Create app footer"""
    with ui.footer().classes('bg-gray-50 border-t border-gray-200'):
        with ui.row().classes('w-full justify-center py-4'):
            ui.label('AI Academic Scheduler © 2026').classes('text-sm text-gray-600')

def create_page_container():
    """Create main page container"""
    return ui.column().classes('w-full max-w-6xl mx-auto p-8 gap-6')

def create_card_container():
    """Create a card container for content sections"""
    return ui.card().classes('w-full p-6 shadow-md rounded-lg border border-gray-100')
