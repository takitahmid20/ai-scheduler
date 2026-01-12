# 🖥️ Desktop Application Setup

## Running as Desktop App (Not Browser)

Your app is now configured to run as a **native desktop application** instead of opening in a browser.

### 📦 Installation Steps

#### 1. Install Required Dependencies

```bash
# Install NiceGUI with native mode support
pip install "nicegui[native]"
```

**On macOS**, you might also need:
```bash
# Install PyWebView dependencies for macOS
pip install pywebview[qt]
```

Or alternatively:
```bash
pip install pywebview[cocoa]
```

#### 2. Run the Application

```bash
python3 app.py
```

The app will open in its own window - **NOT in your browser!** 🎉

---

## ⚙️ Configuration Options

Edit [app.py](app.py) to customize the window:

```python
ui.run(
    title='AI Academic Scheduler',
    native=True,              # Desktop mode ON
    window_size=(1400, 900),  # Window width x height
    fullscreen=False,         # True = open fullscreen
    frameless=False,          # True = no title bar
    reload=False,             # No hot reload in native mode
)
```

### Window Size Options
- `window_size=(1400, 900)` - Default (good for laptops)
- `window_size=(1920, 1080)` - HD display
- `fullscreen=True` - Auto fullscreen

### Window Style Options
- `frameless=False` - Normal window with title bar ✅
- `frameless=True` - Borderless window (custom UI)

---

## 🔄 Switching Between Modes

### Browser Mode (Development)
```python
ui.run(
    native=False,    # Browser mode
    reload=True,     # Hot reload enabled
    show=True,       # Auto-open browser
)
```

### Desktop Mode (Production)
```python
ui.run(
    native=True,           # Desktop app
    window_size=(1400, 900),
    reload=False,          # No reload
)
```

---

## 📦 Creating Standalone Executable (Optional)

To create a **standalone .app or .exe** file that doesn't require Python:

### Using PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Create standalone executable
pyinstaller --onefile --windowed --name "AI-Academic-Scheduler" app.py

# Your app will be in: dist/AI-Academic-Scheduler
```

### Using py2app (macOS only)

```bash
# Install py2app
pip install py2app

# Create setup.py
python setup.py py2app

# Your .app will be in: dist/AI-Academic-Scheduler.app
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'webview'"
**Solution**: Install PyWebView
```bash
pip install pywebview
```

### Issue: Window doesn't open on macOS
**Solution**: Install Qt or Cocoa backend
```bash
pip install pywebview[qt]
# OR
pip install pywebview[cocoa]
```

### Issue: "native mode not available"
**Solution**: Reinstall with native extras
```bash
pip uninstall nicegui
pip install "nicegui[native]"
```

### Issue: App opens in browser instead
**Solution**: Check that `native=True` in [app.py](app.py)

---

## ✅ Current Configuration

Your [app.py](app.py) is configured as:
- ✅ Native mode: **ENABLED**
- ✅ Window size: **1400 x 900**
- ✅ Frameless: **NO** (has title bar)
- ✅ Fullscreen: **NO**

---

## 📝 Quick Start Commands

```bash
# 1. Install dependencies
pip install "nicegui[native]" pywebview

# 2. Run as desktop app
python3 app.py

# That's it! Your app opens in a window 🎉
```

---

## 🎯 What You Get

When running in native mode:
- ✅ Standalone desktop window
- ✅ No browser needed
- ✅ App icon in dock/taskbar
- ✅ Can minimize/maximize/close like any app
- ✅ Faster startup
- ✅ Better performance
- ✅ Professional appearance

---

## 🔍 Comparison

| Feature | Browser Mode | Native Mode |
|---------|-------------|-------------|
| Opening | Opens in browser tab | Opens in desktop window |
| Dependencies | Just NiceGUI | NiceGUI + PyWebView |
| Development | Hot reload ✅ | No hot reload |
| Production | Less professional | More professional ✅ |
| Distribution | Needs browser | Standalone app ✅ |
| Performance | Good | Better ✅ |

---

**Recommendation**: Use **native mode** for your final project presentation! 🚀
