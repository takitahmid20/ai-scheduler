"""
AI Academic Scheduler - Main Application
A NiceGUI-based system for generating optimal course schedules
"""

from nicegui import ui, app
from pages import (
    signin_page, signup_page, upload_page, 
    processing_page, results_page, profile_page
)

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
    # TODO: Add authentication check
    # if not app.storage.user.get('logged_in'):
    #     ui.navigate.to('/signin')
    #     return
    upload_page()

@ui.page('/processing')
def processing():
    """Processing/analysis page"""
    # TODO: Add authentication check
    processing_page()

@ui.page('/results')
def results():
    """Results page with generated schedules"""
    # TODO: Add authentication check
    results_page()

@ui.page('/profile')
def profile():
    """User profile page"""
    # TODO: Add authentication check
    profile_page()

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
