"""
Backend Configuration
Manages application settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
BASE_DIR = Path(__file__).parent.parent

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '')  # Your Supabase project URL
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')  # Your Supabase anon key

# Database configuration
# Format: postgresql://postgres:[YOUR-PASSWORD]@[HOST]:5432/postgres
SUPABASE_DB_URL = os.getenv('SUPABASE_DB_URL', '')

# Fallback to SQLite if Supabase not configured
if SUPABASE_DB_URL:
    DATABASE_URL = SUPABASE_DB_URL
    print("✅ Using Supabase PostgreSQL database")
else:
    DATABASE_URL = 'sqlite:///./data/scheduler.db'
    print("⚠️  Using local SQLite database (set SUPABASE_DB_URL to use Supabase)")

# Admin credentials
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "1234"

# File upload settings
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure directories exist (only for SQLite)
if not SUPABASE_DB_URL:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "data").mkdir(exist_ok=True)