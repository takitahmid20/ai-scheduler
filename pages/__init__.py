"""
Page modules for the AI Academic Scheduler
"""

from .signin import signin_page
from .signup import signup_page
from .upload import upload_page
from .processing import processing_page
from .results import results_page
from .profile import profile_page

__all__ = [
    'signin_page',
    'signup_page', 
    'upload_page',
    'processing_page',
    'results_page',
    'profile_page'
]
