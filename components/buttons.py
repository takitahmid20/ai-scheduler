from nicegui import ui

def create_primary_button(text: str, on_click, icon: str = None, full_width: bool = False):
    """Create a primary action button"""
    btn_class = 'bg-[#ff6900] text-white font-medium px-6 py-2 rounded-lg hover:bg-[#e65f00]'
    if full_width:
        btn_class += ' w-full'
    
    btn = ui.button(text, on_click=on_click).classes(btn_class)
    if icon:
        btn.props(f'icon={icon}')
    return btn

def create_secondary_button(text: str, on_click, icon: str = None, full_width: bool = False):
    """Create a secondary action button"""
    btn_class = 'bg-gray-200 text-gray-700 font-medium px-6 py-2 rounded-lg hover:bg-gray-300'
    if full_width:
        btn_class += ' w-full'
    
    btn = ui.button(text, on_click=on_click).classes(btn_class)
    if icon:
        btn.props(f'icon={icon}')
    return btn

def create_outline_button(text: str, on_click, icon: str = None, full_width: bool = False):
    """Create an outlined button"""
    btn = ui.button(text, on_click=on_click).props('outline')
    btn_class = 'border-2 border-[#ff6900] text-[#ff6900] font-medium px-6 py-2 rounded-lg hover:bg-orange-50'
    if full_width:
        btn_class += ' w-full'
    btn.classes(btn_class)
    if icon:
        btn.props(f'icon={icon}')
    return btn

def create_danger_button(text: str, on_click, icon: str = None):
    """Create a danger/delete button"""
    btn = ui.button(text, on_click=on_click).classes('bg-red-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-red-700')
    if icon:
        btn.props(f'icon={icon}')
    return btn

def create_icon_button(icon: str, on_click, tooltip: str = None):
    """Create an icon-only button"""
    btn = ui.button(icon=icon, on_click=on_click).props('flat round')
    if tooltip:
        btn.tooltip(tooltip)
    return btn

def create_link_button(text: str, route: str):
    """Create a text link that navigates"""
    btn = ui.button(text, on_click=lambda: ui.navigate.to(route)).props('flat').classes('text-[#ff6900] hover:text-[#e65f00]')
    return btn
