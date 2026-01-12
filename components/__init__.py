"""
Reusable UI components for the AI Academic Scheduler
"""

from .layout import create_header, create_footer, create_page_container, create_card_container
from .forms import create_input_field, create_file_upload, create_checkbox, create_select, create_preference_form
from .cards import create_file_status_card, create_schedule_card, create_analysis_step_card, create_stat_card
from .buttons import create_primary_button, create_secondary_button, create_outline_button, create_link_button, create_icon_button
from .loaders import create_loading_spinner, create_progress_bar, create_skeleton_card, simulate_processing

__all__ = [
    'create_header', 'create_footer', 'create_page_container', 'create_card_container',
    'create_input_field', 'create_file_upload', 'create_checkbox', 'create_select', 'create_preference_form',
    'create_file_status_card', 'create_schedule_card', 'create_analysis_step_card', 'create_stat_card',
    'create_primary_button', 'create_secondary_button', 'create_outline_button', 'create_link_button', 'create_icon_button',
    'create_loading_spinner', 'create_progress_bar', 'create_skeleton_card', 'simulate_processing'
]
