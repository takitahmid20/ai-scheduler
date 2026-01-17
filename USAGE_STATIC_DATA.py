"""
Example: Using Static Data in Pages
This demonstrates how to use constants and data_service in your pages
"""

from nicegui import ui
from backend.constants import (
    DEPARTMENTS, TRIMESTERS, YEAR_LEVELS, 
    WEEKDAYS, TIME_SLOTS, COURSE_TYPES
)
from backend.data_service import DataService

def example_page():
    """Example page showing how to use static data"""
    
    ui.label('Static Data Examples').classes('text-2xl font-bold')
    
    with ui.column().classes('w-full gap-4'):
        
        # Example 1: Using constants directly
        ui.label('Example 1: Direct Import').classes('text-lg font-semibold mt-4')
        department_dropdown = ui.select(
            label='Select Department',
            options=DEPARTMENTS,
            value=DEPARTMENTS[0]
        ).classes('w-64')
        
        # Example 2: Using DataService
        ui.label('Example 2: Using DataService').classes('text-lg font-semibold mt-4')
        trimester_dropdown = ui.select(
            label='Select Trimester',
            options=DataService.get_trimesters(),
            value='Fall'
        ).classes('w-64')
        
        # Example 3: Multiple dropdowns
        ui.label('Example 3: Course Schedule Form').classes('text-lg font-semibold mt-4')
        with ui.row().classes('gap-4'):
            ui.select('Day', options=WEEKDAYS).classes('w-40')
            ui.select('Start Time', options=TIME_SLOTS).classes('w-40')
            ui.select('Course Type', options=COURSE_TYPES).classes('w-48')
        
        # Example 4: Dynamic dropdown based on selection
        ui.label('Example 4: Dynamic Options').classes('text-lg font-semibold mt-4')
        dept_select = ui.select(
            'Department',
            options=DEPARTMENTS
        ).classes('w-64')
        
        prefix_label = ui.label('')
        
        def show_prefixes(e):
            prefixes = DataService.get_course_prefixes(e.value)
            prefix_label.text = f'Course prefixes: {", ".join(prefixes) if prefixes else "None"}'
        
        dept_select.on_value_change(show_prefixes)
        
        # Example 5: Using helper functions
        ui.label('Example 5: Helper Functions').classes('text-lg font-semibold mt-4')
        time_range = DataService.format_time_range('09:00', 90)
        ui.label(f'Time range: {time_range}').classes('text-gray-700')
        
        # Example 6: Validation
        ui.label('Example 6: Validation').classes('text-lg font-semibold mt-4')
        test_dept = "Computer Science and Engineering"
        is_valid = DataService.is_valid_department(test_dept)
        ui.label(f'{test_dept}: {"✅ Valid" if is_valid else "❌ Invalid"}').classes('text-gray-700')


# How to use in your actual pages:
"""
USAGE EXAMPLES:

1. In signup/profile pages:
   from backend.constants import DEPARTMENTS, YEAR_LEVELS
   
   department_select = ui.select('Department', options=DEPARTMENTS)
   year_select = ui.select('Year', options=YEAR_LEVELS)

2. In course pages:
   from backend.constants import TRIMESTERS, COURSE_TYPES, CREDIT_OPTIONS
   
   trimester = ui.select('Trimester', options=TRIMESTERS)
   course_type = ui.select('Type', options=COURSE_TYPES)
   credits = ui.select('Credits', options=CREDIT_OPTIONS)

3. In schedule pages:
   from backend.constants import WEEKDAYS, TIME_SLOTS
   
   day = ui.select('Day', options=WEEKDAYS)
   time = ui.select('Time', options=TIME_SLOTS)

4. Using DataService for cleaner code:
   from backend.data_service import DataService
   
   # Get all options
   departments = DataService.get_departments()
   
   # Get specific data
   prefixes = DataService.get_course_prefixes('Computer Science and Engineering')
   
   # Validate input
   if DataService.is_valid_department(user_input):
       # Process
   
   # Format data
   time_range = DataService.format_time_range('09:00', 90)  # "09:00 - 10:30"
"""
