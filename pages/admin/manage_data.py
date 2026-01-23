from nicegui import ui, app
from backend.database import SessionLocal
from backend.models import Semester, CourseOffering
from sqlalchemy import desc


def handle_admin_logout():
    """Handle admin logout"""
    # Clear all user session data
    if hasattr(app.storage, 'user'):
        app.storage.user.clear()
    ui.notify('Logged out successfully', type='positive')
    ui.navigate.to('/admin/login')


def admin_manage_data_page():
    """Admin page to manage course data"""
    ui.colors(primary='#ff6900')
    
    # State variables
    selected_semester = {'value': 'All'}
    selected_program = {'value': 'All'}
    search_query = {'value': ''}
    courses_data = {'rows': [], 'total': 0}
    table_ref = {'table': None}
    pagination = {'page': 1, 'per_page': 50, 'total_pages': 1}
    stats_label = {'label': None}
    
    def load_courses():
        """Load courses from database with pagination"""
        db = SessionLocal()
        try:
            query = db.query(CourseOffering).join(Semester)
            
            # Apply filters
            if selected_semester['value'] != 'All':
                parts = selected_semester['value'].split()
                if len(parts) == 2:
                    semester_name, year = parts
                    query = query.filter(
                        Semester.semester_name == semester_name,
                        Semester.year == int(year)
                    )
            
            if selected_program['value'] != 'All':
                query = query.filter(CourseOffering.program == selected_program['value'])
            
            if search_query['value']:
                search = f"%{search_query['value']}%"
                query = query.filter(
                    (CourseOffering.course_code.like(search)) |
                    (CourseOffering.title.like(search))
                )
            
            # Count total results
            total = query.count()
            courses_data['total'] = total
            
            # Calculate pagination
            pagination['total_pages'] = max(1, (total + pagination['per_page'] - 1) // pagination['per_page'])
            if pagination['page'] > pagination['total_pages']:
                pagination['page'] = 1
            
            # Apply pagination
            offset = (pagination['page'] - 1) * pagination['per_page']
            offerings = query.order_by(desc(CourseOffering.id)).limit(pagination['per_page']).offset(offset).all()
            
            # Format for table
            courses_data['rows'] = [
                {
                    'id': o.id,
                    'course_code': o.course_code,
                    'title': o.title,
                    'section': o.section,
                    'course_type': o.course_type,
                    'program': o.program,
                    'day1': o.day1 or '',
                    'day2': o.day2 or '',
                    'time1': o.time1 or '',
                    'faculty_name': o.faculty_name or '',
                    'credit': o.credit,
                    'semester_name': o.semester.semester_name,
                    'year': o.semester.year
                }
                for o in offerings
            ]
            
            if table_ref['table']:
                table_ref['table'].rows = courses_data['rows']
                table_ref['table'].update()
            
            # Update stats label
            if stats_label['label']:
                start = offset + 1 if total > 0 else 0
                end = min(offset + pagination['per_page'], total)
                stats_label['label'].set_text(f'Showing {start}-{end} of {total} courses')
            
            ui.notify(f'Loaded {len(courses_data["rows"])} courses', type='positive')
            
        finally:
            db.close()
    
    def next_page():
        """Go to next page"""
        if pagination['page'] < pagination['total_pages']:
            pagination['page'] += 1
            load_courses()
    
    def prev_page():
        """Go to previous page"""
        if pagination['page'] > 1:
            pagination['page'] -= 1
            load_courses()
    
    def go_to_page(page_num):
        """Go to specific page"""
        if 1 <= page_num <= pagination['total_pages']:
            pagination['page'] = page_num
            load_courses()
    
    def get_semester_options():
        """Get unique semesters from database"""
        db = SessionLocal()
        try:
            semesters = db.query(Semester).order_by(desc(Semester.year), Semester.semester_name).all()
            options = ['All'] + [f"{s.semester_name} {s.year}" for s in semesters]
            return options
        finally:
            db.close()
    
    def get_program_options():
        """Get unique programs from database"""
        db = SessionLocal()
        try:
            programs = db.query(CourseOffering.program).distinct().all()
            options = ['All'] + [p[0] for p in programs if p[0]]
            return options
        finally:
            db.close()
    
    def delete_course(course_id):
        """Delete a course offering"""
        db = SessionLocal()
        try:
            offering = db.query(CourseOffering).filter(CourseOffering.id == course_id).first()
            if offering:
                db.delete(offering)
                db.commit()
                ui.notify('Course deleted successfully', type='positive')
                load_courses()
        except Exception as e:
            db.rollback()
            ui.notify(f'Error deleting course: {str(e)}', type='negative')
        finally:
            db.close()
    
    def edit_course(course_id):
        """Edit a course offering"""
        db = SessionLocal()
        try:
            offering = db.query(CourseOffering).filter(CourseOffering.id == course_id).first()
            if not offering:
                ui.notify('Course not found', type='negative')
                return
            
            # Create edit dialog
            with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl'):
                ui.label('Edit Course').classes('text-xl font-bold mb-4')
                
                with ui.column().classes('w-full gap-4'):
                    course_code_input = ui.input('Course Code', value=offering.course_code).classes('w-full')
                    title_input = ui.input('Title', value=offering.title).classes('w-full')
                    section_input = ui.input('Section', value=offering.section).classes('w-full')
                    type_select = ui.select(['T', 'L'], label='Type', value=offering.course_type).classes('w-full')
                    
                    with ui.row().classes('w-full gap-4'):
                        day1_input = ui.input('Day 1', value=offering.day1 or '').classes('flex-1')
                        day2_input = ui.input('Day 2', value=offering.day2 or '').classes('flex-1')
                    
                    time1_input = ui.input('Time 1', value=offering.time1 or '').classes('w-full')
                    
                    with ui.row().classes('w-full gap-4'):
                        faculty_input = ui.input('Faculty Name', value=offering.faculty_name or '').classes('flex-1')
                        initial_input = ui.input('Faculty Initial', value=offering.faculty_initial or '').classes('flex-1')
                    
                    credit_input = ui.number('Credit', value=offering.credit, min=0, max=10).classes('w-full')
                    
                    with ui.row().classes('w-full justify-end gap-2 mt-4'):
                        ui.button('Cancel', on_click=dialog.close).props('flat')
                        ui.button('Save Changes', on_click=lambda: save_edits()).props('color=primary')
                
                def save_edits():
                    try:
                        offering.course_code = course_code_input.value
                        offering.title = title_input.value
                        offering.section = section_input.value
                        offering.course_type = type_select.value
                        offering.day1 = day1_input.value
                        offering.day2 = day2_input.value
                        offering.time1 = time1_input.value
                        offering.faculty_name = faculty_input.value
                        offering.faculty_initial = initial_input.value
                        offering.credit = int(credit_input.value)
                        
                        db.commit()
                        ui.notify('Course updated successfully', type='positive')
                        dialog.close()
                        load_courses()
                    except Exception as e:
                        db.rollback()
                        ui.notify(f'Error saving: {str(e)}', type='negative')
            
            dialog.open()
            
        finally:
            db.close()
    
    # Admin Header
    with ui.header().classes('bg-[#ff6900] text-white shadow-lg'):
        with ui.row().classes('w-full items-center justify-between px-6 py-3'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('admin_panel_settings', size='2rem')
                ui.label('Admin Dashboard').classes('text-2xl font-bold')
            
            with ui.row().classes('items-center gap-4'):
                ui.button('Back to Dashboard', icon='arrow_back', on_click=lambda: ui.navigate.to('/admin/dashboard')).props('flat')
                ui.button('Logout', icon='logout', on_click=handle_admin_logout).props('flat')
    
    with ui.row().classes('w-full h-screen'):
        # Sidebar Navigation
        with ui.column().classes('w-64 bg-gray-800 text-white p-4 gap-2'):
            ui.label('NAVIGATION').classes('text-xs text-gray-400 font-semibold mb-2 mt-4')
            
            nav_button('dashboard', 'Dashboard', '/admin/dashboard')
            nav_button('upload_file', 'Upload Courses', '/admin/upload-courses')
            nav_button('table_view', 'Manage Data', '/admin/manage-data', active=True)
            
            # Spacer to push logout to bottom
            ui.space()
            
            # Logout button at bottom
            ui.separator().classes('my-4')
            with ui.button(icon='logout', on_click=handle_admin_logout).props('flat').classes('w-full justify-start bg-red-600 hover:bg-red-700 text-white'):
                ui.label('Logout').classes('ml-3 font-semibold')
        
        # Main Content Area
        with ui.column().classes('flex-1 bg-gray-50 p-8 overflow-auto'):
            # Page title
            with ui.row().classes('w-full items-center justify-between mb-6'):
                with ui.column().classes('gap-2'):
                    ui.label('Manage Course Data').classes('text-3xl font-bold text-gray-800')
                    ui.label('View, edit, and manage all course information').classes('text-gray-600')
                
                ui.button('Refresh Data', icon='refresh', on_click=load_courses).props('color=primary')
            
            # Filters Card
            with ui.card().classes('w-full p-6 shadow-lg mb-6'):
                ui.label('Filters').classes('text-lg font-semibold text-gray-800 mb-4')
                
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1 gap-2'):
                        ui.label('Semester').classes('text-sm font-medium text-gray-700')
                        semester_select = ui.select(
                            get_semester_options(),
                            value='All',
                            on_change=lambda e: [selected_semester.update({'value': e.value})]
                        ).classes('w-full')
                    
                    with ui.column().classes('flex-1 gap-2'):
                        ui.label('Program').classes('text-sm font-medium text-gray-700')
                        program_select = ui.select(
                            get_program_options(),
                            value='All',
                            on_change=lambda e: [selected_program.update({'value': e.value})]
                        ).classes('w-full')
                    
                    with ui.column().classes('flex-1 gap-2'):
                        ui.label('Search').classes('text-sm font-medium text-gray-700')
                        search_input = ui.input(
                            placeholder='Search by code or title...',
                            on_change=lambda e: [search_query.update({'value': e.value})]
                        ).classes('w-full').props('outlined')
                    
                    with ui.column().classes('gap-2 justify-end'):
                        ui.label(' ').classes('text-sm')
                        ui.button('Apply Filters', icon='filter_alt', on_click=load_courses).props('color=primary')
            
            # Data Table Card
            with ui.card().classes('w-full p-6 shadow-lg'):
                with ui.row().classes('w-full items-center justify-between mb-4'):
                    ui.label('Course List').classes('text-lg font-semibold text-gray-800')
                    with ui.row().classes('gap-3 items-center'):
                        ui.badge(f'{courses_data["total"]} total', color='positive')
                        ui.select(
                            [25, 50, 100, 200, 500, 1000],
                            value=50,
                            on_change=lambda e: [
                                pagination.update({'per_page': e.value, 'page': 1}),
                                load_courses()
                            ]
                        ).props('dense outlined').classes('w-24').tooltip('Items per page')
                
                # Table
                columns = [
                    {'name': 'course_code', 'label': 'Course Code', 'field': 'course_code', 'align': 'left', 'sortable': True},
                    {'name': 'title', 'label': 'Course Title', 'field': 'title', 'align': 'left', 'sortable': True},
                    {'name': 'section', 'label': 'Section', 'field': 'section', 'align': 'center'},
                    {'name': 'course_type', 'label': 'Type', 'field': 'course_type', 'align': 'center'},
                    {'name': 'credit', 'label': 'Credit', 'field': 'credit', 'align': 'center'},
                    {'name': 'program', 'label': 'Program', 'field': 'program', 'align': 'center'},
                    {'name': 'faculty_name', 'label': 'Faculty', 'field': 'faculty_name', 'align': 'left'},
                    {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'},
                ]
                
                table = ui.table(
                    columns=columns,
                    rows=courses_data['rows'],
                    row_key='id'
                ).classes('w-full')
                
                table_ref['table'] = table
                
                # Add custom action buttons for each row
                table.add_slot('body-cell-actions', '''
                    <q-td :props="props">
                        <q-btn flat round dense icon="edit" color="primary" size="sm" @click="$parent.$emit('edit', props.row.id)" />
                        <q-btn flat round dense icon="delete" color="negative" size="sm" @click="$parent.$emit('delete', props.row.id)" />
                    </q-td>
                ''')
                
                table.on('edit', lambda e: edit_course(e.args))
                table.on('delete', lambda e: delete_course(e.args))
                
                # Pagination Controls
                with ui.row().classes('w-full justify-between items-center mt-6'):
                    stats_label['label'] = ui.label('Loading...').classes('text-sm text-gray-600')
                    
                    with ui.row().classes('gap-2 items-center'):
                        ui.button(icon='chevron_left', on_click=prev_page).props('flat dense').classes('text-gray-600')
                        
                        # Page numbers
                        with ui.row().classes('gap-1'):
                            # Show first page
                            if pagination['page'] > 3:
                                ui.button('1', on_click=lambda: go_to_page(1)).props('flat dense').classes('min-w-0 px-3')
                                if pagination['page'] > 4:
                                    ui.label('...').classes('px-2 text-gray-400')
                            
                            # Show pages around current page
                            for i in range(max(1, pagination['page'] - 2), min(pagination['total_pages'] + 1, pagination['page'] + 3)):
                                if i == pagination['page']:
                                    ui.label(str(i)).classes('px-3 py-1 bg-[#ff6900] text-white rounded')
                                else:
                                    ui.button(str(i), on_click=lambda p=i: go_to_page(p)).props('flat dense').classes('min-w-0 px-3')
                            
                            # Show last page
                            if pagination['page'] < pagination['total_pages'] - 2:
                                if pagination['page'] < pagination['total_pages'] - 3:
                                    ui.label('...').classes('px-2 text-gray-400')
                                ui.button(str(pagination['total_pages']), on_click=lambda: go_to_page(pagination['total_pages'])).props('flat dense').classes('min-w-0 px-3')
                        
                        ui.button(icon='chevron_right', on_click=next_page).props('flat dense').classes('text-gray-600')
    
    # Load initial data
    load_courses()

def nav_button(icon, label, link, active=False):
    """Create a navigation button"""
    classes = 'w-full justify-start'
    if active:
        classes += ' bg-[#ff6900]'
    
    with ui.button(icon=icon, on_click=lambda: ui.navigate.to(link) if link != '#' else None).props('flat align=left').classes(classes):
        ui.label(label).classes('ml-3')
