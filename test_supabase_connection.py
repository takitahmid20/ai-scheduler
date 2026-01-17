"""
Test Supabase Database Connection
Run this to diagnose connection issues
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

# Load environment variables
load_dotenv()

SUPABASE_DB_URL = os.getenv('SUPABASE_DB_URL', '')

print("=" * 60)
print("🔍 Supabase Connection Test")
print("=" * 60)

if not SUPABASE_DB_URL:
    print("❌ SUPABASE_DB_URL not set in .env file")
    exit(1)

# Parse connection string (hide password)
url_parts = SUPABASE_DB_URL.replace('postgresql://', '').split('@')
if len(url_parts) == 2:
    user_pass = url_parts[0]
    host_db = url_parts[1]
    user = user_pass.split(':')[0]
    print(f"📌 User: {user}")
    print(f"📌 Host: {host_db}")
    print(f"📌 Password: {'*' * 16}")
else:
    print(f"📌 Connection URL: {SUPABASE_DB_URL[:50]}...")

print("\n" + "=" * 60)
print("🔄 Attempting connection...")
print("=" * 60)

try:
    # Try to connect
    conn = psycopg2.connect(SUPABASE_DB_URL)
    print("✅ Connection successful!")
    
    # Try to execute a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ PostgreSQL version: {version[0]}")
    
    # Check for existing tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"\n📊 Existing tables ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("\n📊 No tables found (fresh database)")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ All checks passed! Supabase is ready to use.")
    print("=" * 60)
    
except OperationalError as e:
    print(f"\n❌ Connection failed!")
    print(f"Error: {e}")
    print("\n" + "=" * 60)
    print("🔧 Troubleshooting steps:")
    print("=" * 60)
    print("1. Check if your Supabase project is ACTIVE (not paused)")
    print("   → Go to: https://supabase.com/dashboard")
    print("   → Click on your project")
    print("   → Look for 'Paused' status and click 'Restore'")
    print()
    print("2. Verify your database password")
    print("   → Project Settings > Database > Database Password")
    print("   → You may need to reset it")
    print()
    print("3. Check your connection string format")
    print("   → Project Settings > Database > Connection String")
    print("   → Use 'Session mode' (not Transaction mode)")
    print()
    print("4. Network/Firewall issues")
    print("   → Ensure your internet connection is stable")
    print("   → Check if firewalls are blocking port 5432 or 6543")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    print("=" * 60)
