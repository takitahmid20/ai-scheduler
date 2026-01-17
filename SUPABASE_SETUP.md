# Supabase Database Setup Guide

## 📋 Prerequisites
- Supabase account (free tier available at https://supabase.com)
- Python environment with dependencies installed

## 🚀 Step-by-Step Setup

### 1. Create Supabase Project

1. Go to https://supabase.com and sign in
2. Click "New Project"
3. Choose organization and fill in:
   - **Project Name**: ai-scheduler (or your choice)
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Select closest to you
   - **Pricing Plan**: Free (or Pro if needed)
4. Click "Create new project" and wait for setup (1-2 minutes)

### 2. Get Database Connection String

1. In your Supabase project dashboard:
   - Go to **Project Settings** (⚙️ icon in sidebar)
   - Click **Database** in the left menu
   - Scroll to **Connection String** section
   - Select **Session mode** (not Transaction mode)
   - Copy the connection string

2. Replace `[YOUR-PASSWORD]` in the connection string with your database password

Example format:
```
postgresql://postgres:your-password@db.abcdefghijklmnop.supabase.co:5432/postgres
```

### 3. Get API Keys

1. In your Supabase project dashboard:
   - Go to **Project Settings** > **API**
   - Copy **Project URL**
   - Copy **anon/public key**

### 4. Configure Environment Variables

**Option A: Using .env file (Recommended)**

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your values:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   SUPABASE_DB_URL=postgresql://postgres:your-password@db.xxxxx.supabase.co:5432/postgres
   ```

3. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

4. Update `backend/config.py` to load .env:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

**Option B: Export environment variables**

```bash
export SUPABASE_URL="https://xxxxx.supabase.co"
export SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
export SUPABASE_DB_URL="postgresql://postgres:your-password@db.xxxxx.supabase.co:5432/postgres"
```

### 5. Install Dependencies

```bash
pip install psycopg2-binary
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### 6. Initialize Database Tables

Run your app - tables will be created automatically:
```bash
python app.py
```

You should see:
```
✅ Using Supabase PostgreSQL database
🐘 Connected to PostgreSQL (Supabase)
✅ Database tables created successfully
```

### 7. Verify Tables in Supabase

1. Go to your Supabase dashboard
2. Click **Table Editor** in sidebar
3. You should see these tables:
   - `users` - Student and admin accounts
   - `courses` - Course information
   - `schedules` - Generated schedules

## 🔍 Troubleshooting

### Connection Issues

**Error: "could not connect to server"**
- Check your database password is correct
- Verify the connection string format
- Ensure your IP is allowed (Supabase allows all by default)

**Error: "SSL connection required"**
- Supabase requires SSL. This is handled automatically by psycopg2

### Database Password Issues

**Forgot password?**
1. Go to **Project Settings** > **Database**
2. Click **Reset database password**
3. Update your `.env` file with new password

### Environment Variable Issues

**Variables not loading?**
- Make sure `.env` is in project root
- Install python-dotenv: `pip install python-dotenv`
- Check `.env` has no spaces around `=`
- Restart your application after changing `.env`

## 🔄 Switching Between SQLite and Supabase

The app automatically detects which database to use:

**Use Supabase:**
- Set `SUPABASE_DB_URL` environment variable

**Use SQLite (local):**
- Leave `SUPABASE_DB_URL` empty or unset
- Data stored in `data/scheduler.db`

## 📊 Viewing Database Data

### Using Supabase Dashboard
1. Go to **Table Editor**
2. Select table (users, courses, schedules)
3. View, edit, or delete records

### Using SQL Editor
1. Go to **SQL Editor** in sidebar
2. Run queries:
   ```sql
   SELECT * FROM users;
   SELECT * FROM courses WHERE department = 'Computer Science and Engineering';
   SELECT * FROM schedules WHERE user_id = 1;
   ```

## 🔐 Security Best Practices

1. **Never commit `.env` to git**
   - Already in `.gitignore`
   - Use `.env.example` for sharing template

2. **Use Row Level Security (RLS)**
   ```sql
   -- Enable RLS on users table
   ALTER TABLE users ENABLE ROW LEVEL SECURITY;
   
   -- Policy: Users can only see their own data
   CREATE POLICY "Users can view own data" ON users
     FOR SELECT USING (auth.uid() = id);
   ```

3. **Rotate passwords regularly**
   - Change database password every few months
   - Update `.env` file

## 🎯 Next Steps

1. ✅ Database connected
2. ✅ Tables created
3. 🔜 Test signup/signin
4. 🔜 Add course data
5. 🔜 Generate schedules

## 💡 Tips

- **Free tier limits**: 500MB database, 2GB bandwidth/month
- **Connection pooling**: Already configured in `database.py`
- **Backups**: Automatic daily backups on paid plans
- **Monitoring**: Check **Database** > **Usage** for metrics

## 📚 Resources

- [Supabase Docs](https://supabase.com/docs)
- [SQLAlchemy + PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
