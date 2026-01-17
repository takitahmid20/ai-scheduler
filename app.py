"""
AI Academic Scheduler - Main Application
A NiceGUI-based system for generating optimal course schedules
"""

from nicegui import ui, app
from pages import (
    signin_page, signup_page, upload_page, 
    processing_page, results_page, profile_page
)
from pages.admin import (
    admin_login_page, admin_dashboard_page, 
    admin_upload_page, admin_manage_data_page
)

# Initialize database on startup
from backend.database import init_db
init_db()

# =====================================================
# APP CONFIGURATION
# =====================================================

app.title = 'AI Academic Scheduler'
app.favicon = '🎓'

# =====================================================
# ROUTING
# =====================================================

@ui.page('/')
def index():
    """Redirect to sign in page"""
    ui.navigate.to('/signin')

@ui.page('/signin')
def signin():
    """Sign in page"""
    signin_page()

@ui.page('/signup')
def signup():
    """Sign up page"""
    signup_page()

@ui.page('/upload')
def upload():
    """Upload data page"""
    if not app.storage.user.get('logged_in'):
        ui.navigate.to('/signin')
        return
    upload_page()

@ui.page('/processing')
def processing():
    """Processing/analysis page"""
    if not app.storage.user.get('logged_in'):
        ui.navigate.to('/signin')
        return
    processing_page()

@ui.page('/results')
def results():
    """Results page with generated schedules"""
    if not app.storage.user.get('logged_in'):
        ui.navigate.to('/signin')
        return
    results_page()

@ui.page('/profile')
def profile():
    """User profile page"""
    if not app.storage.user.get('logged_in'):
        ui.navigate.to('/signin')
        return
    profile_page()

# =====================================================
# ADMIN ROUTING
# =====================================================

@ui.page('/admin')
def admin_index():
    """Redirect to admin login"""
    ui.navigate.to('/admin/login')

@ui.page('/admin/login')
def admin_login():
    """Admin login page"""
    admin_login_page()

@ui.page('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if not app.storage.user.get('logged_in') or not app.storage.user.get('is_admin'):
        ui.navigate.to('/admin/login')
        return
    admin_dashboard_page()

@ui.page('/admin/upload')
def admin_upload():
    """Admin upload data page"""
    if not app.storage.user.get('logged_in') or not app.storage.user.get('is_admin'):
        ui.navigate.to('/admin/login')
        return
    admin_upload_page()

@ui.page('/admin/manage-data')
def admin_manage_data():
    """Admin manage data page"""
    if not app.storage.user.get('logged_in') or not app.storage.user.get('is_admin'):
        ui.navigate.to('/admin/login')
        return
    admin_manage_data_page()

# =====================================================
# APP STARTUP
# =====================================================

if __name__ in {"__main__", "__mp_main__"}:
    # Configure NiceGUI
    # For desktop app mode, set native=True
    # For browser mode, set native=False
    
    ui.run(
        title='AI Academic Scheduler',
        port=8080,
        reload=False,         # Disable reload for native mode
        native=True,          # Run as desktop app (set to False for browser)
        window_size=(1400, 900),  # Window size for native mode
        fullscreen=False,     # Set True for fullscreen
        frameless=False,      # Set True for frameless window
        storage_secret='ai-academic-scheduler-secret-key-2026'
    )
