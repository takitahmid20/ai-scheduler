"""
Admin Course Upload Page
Upload PDF with course offerings and preview/edit extracted data
"""

from nicegui import ui, app
import os
import tempfile
from typing import List, Dict, Any

# Try to import PDF parser - it's optional
try:
    from ai.course_processor.pdf_parser import PDFParser, CourseExtractor
    PDF_PARSER_AVAILABLE = True
except ImportError:
    PDFParser = None
    CourseExtractor = None
    PDF_PARSER_AVAILABLE = False

from backend.database import SessionLocal
from backend.models import Semester, CourseOffering, CourseList


# Semester options
SEMESTERS = ['Spring', 'Summer', 'Fall']
PROGRAMS = ['BSCSE', 'BSDS']


def handle_admin_logout():
    """Handle admin logout"""
    # Clear all user session data
    if hasattr(app.storage, 'user'):
        app.storage.user.clear()
    ui.notify('Logged out successfully', type='positive')
    ui.navigate.to('/admin/login')


def nav_button(icon: str, label: str, path: str, active: bool = False):
    """Navigation button component"""
    classes = 'w-full justify-start gap-3 px-4 py-3 rounded-lg'
    if active:
        classes += ' bg-[#ff6900] text-white'
    else:
        classes += ' text-gray-300 hover:bg-gray-700'
    
    return ui.button(label, icon=icon, on_click=lambda: ui.navigate.to(path) if path != '#' else None).props('flat').classes(classes)


class CourseUploadPage:
    def __init__(self):
        self.extracted_courses: List[Dict[str, Any]] = []
        self.semester_select = None
        self.year_input = None
        self.program_select = None
        self.upload_area = None
        self.preview_container = None
        self.save_button = None
        
    def render(self):
        """Render the upload page"""
        ui.colors(primary='#ff6900')
        
        # Admin Header
        with ui.header().classes('bg-[#ff6900] text-white shadow-lg'):
            with ui.row().classes('w-full items-center justify-between px-6 py-3'):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('admin_panel_settings', size='2rem')
                    ui.label('Admin Dashboard').classes('text-2xl font-bold')
                
                with ui.row().classes('items-center gap-4'):
                    admin_name = app.storage.user.get('name', 'Admin')
                    ui.label(f'Hello, {admin_name}').classes('text-sm')
                    ui.button('Back to Dashboard', icon='arrow_back', on_click=lambda: ui.navigate.to('/admin/dashboard')).props('flat')
                    ui.button('Logout', icon='logout', on_click=handle_admin_logout).props('flat')
        
        with ui.row().classes('w-full h-screen'):
            # Sidebar Navigation
            with ui.column().classes('w-64 bg-gray-800 text-white p-4 gap-2'):
                ui.label('NAVIGATION').classes('text-xs text-gray-400 font-semibold mb-2 mt-4')
                
                nav_button('dashboard', 'Dashboard', '/admin/dashboard')
                nav_button('upload_file', 'Upload Courses', '/admin/upload-courses', active=True)
                nav_button('table_view', 'Manage Data', '/admin/manage-data')
                
                # Spacer to push logout to bottom
                ui.space()
                
                # Logout button at bottom
                ui.separator().classes('my-4')
                with ui.button(icon='logout', on_click=handle_admin_logout).props('flat').classes('w-full justify-start bg-red-600 hover:bg-red-700 text-white'):
                    ui.label('Logout').classes('ml-3 font-semibold')
            
            # Main Content Area
            with ui.column().classes('flex-1 bg-gray-50 p-8 overflow-auto'):
                # Check if PDF parser is available
                if not PDF_PARSER_AVAILABLE:
                    with ui.card().classes('w-full max-w-4xl p-8 bg-yellow-50 border-l-4 border-yellow-500'):
                        with ui.row().classes('items-start gap-4'):
                            ui.icon('warning', size='2rem').classes('text-yellow-600')
                            with ui.column().classes('gap-2'):
                                ui.label('PDF Upload Feature Unavailable').classes('text-xl font-bold text-gray-800')
                                ui.label('The PDF parsing library (pdfplumber) is not installed. Please install it to enable PDF upload.').classes('text-gray-700')
                                ui.label('Run: pip install pdfplumber').classes('font-mono bg-gray-800 text-white px-3 py-2 rounded mt-2')
                                ui.label('Note: You can still manage course data manually in the "Manage Data" section.').classes('text-sm text-gray-600 mt-2')
                    return
                
                # Upload Form Card
                with ui.card().classes('w-full max-w-6xl p-8 shadow-lg'):
                    ui.label('Semester Information').classes('text-xl font-semibold text-gray-800 mb-4')
                    
                    with ui.row().classes('w-full gap-4 mb-6'):
                        # Semester Selection
                        with ui.column().classes('flex-1 gap-2'):
                            ui.label('Semester').classes('text-sm font-semibold text-gray-700')
                            self.semester_select = ui.select(
                                SEMESTERS,
                                value=SEMESTERS[0]
                            ).classes('w-full')
                        
                        # Year Input
                        with ui.column().classes('flex-1 gap-2'):
                            ui.label('Year').classes('text-sm font-semibold text-gray-700')
                            self.year_input = ui.number(
                                value=2026,
                                min=2020,
                                max=2030,
                                step=1
                            ).classes('w-full')
                        
                        # Program Selection
                        with ui.column().classes('flex-1 gap-2'):
                            ui.label('Program').classes('text-sm font-semibold text-gray-700')
                            self.program_select = ui.select(
                                PROGRAMS,
                                value=PROGRAMS[0]
                            ).classes('w-full')
                    
                    ui.separator()
                    
                    # PDF Upload Section
                    ui.label('Upload PDF File').classes('text-xl font-semibold text-gray-800 mt-6 mb-4')
                    
                    with ui.column().classes('w-full gap-4'):
                        ui.upload(
                            on_upload=self.handle_upload,
                            auto_upload=True,
                            multiple=False,
                            max_file_size=10_000_000  # 10MB
                        ).props('accept=".pdf"').classes('w-full')
                        
                        ui.label('Accepted format: PDF only (Max 10MB)').classes('text-xs text-gray-500')
                
                    # Preview Container (hidden initially)
                    self.preview_container = ui.column().classes('w-full max-w-6xl gap-4 mt-6').style('display: none')
    
    async def handle_upload(self, e):
        """Handle PDF file upload"""
        try:
            ui.notify('Processing PDF...', type='info')
            
            # Get the file path - NiceGUI already saved it to a temp location
            file_path = str(e.file._path)
            
            # Extract courses from PDF directly
            courses = PDFParser.parse_pdf(file_path)
            
            if not courses:
                ui.notify('No course data found in PDF', type='negative')
                return
            
            # Process and validate courses
            self.extracted_courses = []
            for course in courses:
                # Clean and validate
                cleaned = CourseExtractor.clean_course_data(course)
                if CourseExtractor.validate_course_data(cleaned):
                    self.extracted_courses.append(cleaned)
            
            if not self.extracted_courses:
                ui.notify('No valid courses extracted', type='negative')
                return
            
            ui.notify(f'Extracted {len(self.extracted_courses)} courses successfully', type='positive')
            
            # Show preview
            self.show_preview()
            
        except Exception as ex:
            ui.notify(f'Error processing PDF: {str(ex)}', type='negative')
            import traceback
            traceback.print_exc()
            print(f"Upload error: {ex}")
    
    def show_preview(self):
        """Display preview of extracted courses"""
        self.preview_container.clear()
        self.preview_container.style('display: block')
        
        with self.preview_container:
            with ui.card().classes('w-full p-6 shadow-lg'):
                with ui.row().classes('w-full items-center justify-between mb-4'):
                    ui.label('Preview Extracted Data').classes('text-xl font-semibold text-gray-800')
                    with ui.row().classes('gap-2 items-center'):
                        ui.badge(f'{len(self.extracted_courses)} courses', color='positive')
                        ui.button('Save All Courses', icon='save', on_click=self.save_courses, color='positive')
                
                ui.label('Review and edit the extracted data before saving').classes('text-sm text-gray-600 mb-4')
                ui.label('💡 Click on any cell to edit. Changes are saved automatically.').classes('text-xs text-orange-600 mb-2')
                
                # Create editable grid
                columns = [
                    {'name': 'program', 'label': 'Program', 'field': 'program', 'sortable': True, 'align': 'left', 'editable': True},
                    {'name': 'course_code', 'label': 'Course Code', 'field': 'course_code', 'sortable': True, 'align': 'left', 'editable': True},
                    {'name': 'title', 'label': 'Title', 'field': 'title', 'sortable': True, 'align': 'left', 'editable': True},
                    {'name': 'section', 'label': 'Section', 'field': 'section', 'sortable': True, 'align': 'center', 'editable': True},
                    {'name': 'course_type', 'label': 'Type', 'field': 'course_type', 'sortable': True, 'align': 'center', 'editable': True},
                    {'name': 'day1', 'label': 'Day 1', 'field': 'day1', 'align': 'center', 'editable': True},
                    {'name': 'day2', 'label': 'Day 2', 'field': 'day2', 'align': 'center', 'editable': True},
                    {'name': 'time1', 'label': 'Time 1', 'field': 'time1', 'align': 'left', 'editable': True},
                    {'name': 'faculty_name', 'label': 'Faculty', 'field': 'faculty_name', 'align': 'left', 'editable': True},
                    {'name': 'faculty_initial', 'label': 'Initial', 'field': 'faculty_initial', 'align': 'center', 'editable': True},
                    {'name': 'credit', 'label': 'Credit', 'field': 'credit', 'sortable': True, 'align': 'center', 'editable': True},
                ]
                
                table = ui.table(
                    columns=columns,
                    rows=self.extracted_courses,
                    row_key='course_code'
                ).classes('w-full')
                
                # Make table cells editable
                table.add_slot('body-cell', '''
                    <q-td :props="props" @click="$parent.$emit('edit', props)">
                        <div class="cursor-pointer hover:bg-gray-100 px-2 py-1">
                            {{ props.value }}
                        </div>
                    </q-td>
                ''')
                
                def handle_edit(e):
                    """Handle cell edit"""
                    row = e.args['row']
                    col = e.args['col']
                    
                    # Show edit dialog
                    with ui.dialog() as dialog, ui.card():
                        ui.label(f'Edit {col["label"]}').classes('text-lg font-bold mb-4')
                        
                        if col['name'] == 'course_type':
                            # Dropdown for course type
                            new_value = ui.select(['T', 'L'], value=row[col['name']]).classes('w-full')
                        elif col['name'] == 'credit':
                            # Number input for credit
                            new_value = ui.number(value=int(row[col['name']]) if row[col['name']] else 0, min=0, max=10).classes('w-full')
                        else:
                            # Text input for other fields
                            new_value = ui.input(value=str(row[col['name']] or '')).classes('w-full')
                        
                        with ui.row().classes('w-full justify-end gap-2 mt-4'):
                            ui.button('Cancel', on_click=dialog.close).props('flat')
                            ui.button('Save', on_click=lambda: save_edit(row, col['name'], new_value.value, dialog))
                    
                    dialog.open()
                
                def save_edit(row, field, value, dialog):
                    """Save edited value"""
                    row[field] = value
                    table.update()
                    ui.notify(f'Updated {field}', type='positive')
                    dialog.close()
                
                table.on('edit', handle_edit)
                
                # Action buttons
                with ui.row().classes('w-full justify-end gap-4 mt-6'):
                    ui.button('Cancel', icon='close', on_click=self.cancel_upload).props('outline').classes('text-gray-600')
                    ui.button('Save All Courses', icon='save', on_click=self.save_courses, color='positive')
    
    def cancel_upload(self):
        """Cancel and clear upload"""
        self.extracted_courses = []
        self.preview_container.clear()
        self.preview_container.style('display: none')
        ui.notify('Upload cancelled', type='info')
    
    async def save_courses(self):
        """Save all courses to database"""
        try:
            ui.notify('Saving courses to database...', type='info')
            
            db = SessionLocal()
            
            try:
                # Create semester record
                semester = Semester(
                    semester_name=self.semester_select.value,
                    year=int(self.year_input.value),
                    program=self.program_select.value,
                    uploaded_by=app.storage.user.get('id')
                )
                db.add(semester)
                db.flush()  # Get semester ID
                
                # Track unique courses for course_list
                unique_courses = {}
                
                # Create course offering records
                for course in self.extracted_courses:
                    # Add to course offerings
                    offering = CourseOffering(
                        semester_id=semester.id,
                        program=course.get('program', ''),
                        course_code=course.get('course_code', ''),
                        title=course.get('title', ''),
                        section=course.get('section', ''),
                        course_type=course.get('course_type', 'T'),
                        credit=course.get('credit', 0),
                        day1=course.get('day1', ''),
                        day2=course.get('day2', ''),
                        time1=course.get('time1', ''),
                        time2=course.get('time2', ''),
                        room1=course.get('room1', ''),
                        room2=course.get('room2', ''),
                        faculty_name=course.get('faculty_name', ''),
                        faculty_initial=course.get('faculty_initial', '')
                    )
                    db.add(offering)
                    
                    # Track unique courses by course_code
                    course_code = course.get('course_code', '')
                    if course_code and course_code not in unique_courses:
                        unique_courses[course_code] = {
                            'title': course.get('title', ''),
                            'credit': course.get('credit', 0)
                        }
                
                # Update course_list table (add new courses, skip existing)
                for course_code, course_info in unique_courses.items():
                    # Check if course already exists in course_list
                    existing = db.query(CourseList).filter(
                        CourseList.course_code == course_code
                    ).first()
                    
                    if not existing:
                        # Add new course to master list
                        new_course = CourseList(
                            course_code=course_code,
                            title=course_info['title'],
                            credit=course_info['credit']
                        )
                        db.add(new_course)
                
                db.commit()
                
                ui.notify(f'Successfully saved {len(self.extracted_courses)} courses!', type='positive')
                
                # Clear and reset
                self.extracted_courses = []
                self.preview_container.clear()
                self.preview_container.style('display: none')
                
            except Exception as e:
                db.rollback()
                raise e
            finally:
                db.close()
                
        except Exception as ex:
            ui.notify(f'Error saving courses: {str(ex)}', type='negative')
            print(f"Save error: {ex}")


def admin_upload_courses_page():
    """Entry point for the upload courses page"""
    page = CourseUploadPage()
    page.render()
