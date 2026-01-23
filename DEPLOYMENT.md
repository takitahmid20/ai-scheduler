# AI Academic Scheduler - Deployment Guide

## 🚀 Deploy to Railway (Recommended - FREE)

Railway offers free hosting with:
- 500 hours/month free usage
- Automatic SSL certificates
- GitHub integration
- PostgreSQL database (optional)

### Steps:

1. **Push to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ai-scheduler.git
   git push -u origin main
   ```

2. **Deploy to Railway**:
   - Go to https://railway.app/
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select this repository
   - Railway will auto-detect Python and deploy!

3. **Set Environment Variables** (in Railway dashboard):
   - `STORAGE_SECRET` → `your-secret-key-here-random-string`
   - `PORT` → `8080` (auto-set)

4. **Access your app**:
   - Railway will give you a URL like: `https://your-app.railway.app`

---

## 🌐 Deploy to Render (Alternative - FREE)

Render offers:
- Free tier for web services
- Auto-deploy from Git
- Custom domains

### Steps:

1. **Push to GitHub** (same as above)

2. **Deploy to Render**:
   - Go to https://render.com/
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Name**: ai-academic-scheduler
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
     - **Plan**: Free

3. **Set Environment Variables**:
   - `STORAGE_SECRET` → `your-secret-key`
   - `PYTHON_VERSION` → `3.11.0`

4. **Deploy** and wait 2-3 minutes

---

## 📱 Local Installation Guide

For users who want to install on their device:

### Windows:
```bash
# 1. Install Python 3.11+ from python.org
# 2. Download/clone this repository
# 3. Open terminal in project folder
pip install -r requirements.txt
python app.py
```

### macOS:
```bash
# 1. Install Python (if not installed)
brew install python@3.11

# 2. Clone/download repository
# 3. Navigate to project folder
pip3 install -r requirements.txt
python3 app.py
```

### Linux:
```bash
sudo apt update
sudo apt install python3.11 python3-pip
pip3 install -r requirements.txt
python3 app.py
```

---

## 🗄️ Database Options

### Local (Current):
- Uses SQLite (file: `data/scheduler.db`)
- No setup needed
- Works offline

### Cloud (Recommended for production):
- Sign up for Supabase (free): https://supabase.com/
- Create new project
- Get connection string
- Set environment variable:
  ```
  SUPABASE_DB_URL=postgresql://user:pass@host:5432/dbname
  ```

---

## 🔒 Security Notes

**Before deploying publicly:**

1. Change `STORAGE_SECRET` to a strong random string
2. Use Supabase or PostgreSQL (not SQLite) for production
3. Enable HTTPS (automatic on Railway/Render)
4. Consider adding rate limiting

---

## 📊 Check Deployment

After deployment, verify:
- [ ] App loads at your URL
- [ ] Can create account
- [ ] Can login
- [ ] Can upload PDF (test with sample data)
- [ ] Can generate schedules
- [ ] PDF download works

---

## 🆘 Troubleshooting

**App not starting?**
- Check logs in Railway/Render dashboard
- Verify `requirements.txt` is correct
- Ensure PORT environment variable is set

**Database errors?**
- For cloud: Use Supabase PostgreSQL
- Check database connection string
- Verify tables are created (auto-created on first run)

**Session issues?**
- Set `STORAGE_SECRET` environment variable
- Clear browser cookies

---

## 💰 Cost Estimate

### Free Tier (Railway):
- 500 hours/month = ~20 days of 24/7 uptime
- Perfect for student projects
- Upgrade to $5/month for unlimited

### Free Tier (Render):
- Unlimited uptime
- Goes to sleep after 15 min inactivity
- Wakes up in ~1 minute on access

**Recommendation**: Start with Railway for always-on experience, switch to Render if you exceed 500 hours.

---

## 🎓 Your App URL

After deployment, share your app:
```
https://your-app-name.railway.app
or
https://your-app-name.onrender.com
```

Anyone can access it with just a browser - no installation needed!
