# Project Structure Overview

## 📂 Directory Layout

```
AI/
├── app.py                     # Main application entry
├── requirements.txt           # Python dependencies
│
├── components/               # ✅ Reusable UI Components
│   ├── __init__.py
│   ├── layout.py            # Headers, footers, containers
│   ├── forms.py             # Input fields, file uploads, preferences
│   ├── cards.py             # Status cards, schedule cards, stat cards
│   ├── buttons.py           # Primary, secondary, outline buttons
│   └── loaders.py           # Spinners, progress bars, skeletons
│
├── pages/                   # ✅ Application Pages
│   ├── __init__.py
│   ├── signin.py           # Sign in page
│   ├── signup.py           # Sign up page
│   ├── upload.py           # File upload & preferences page
│   ├── processing.py       # Real-time processing page
│   ├── results.py          # Schedule results display
│   └── profile.py          # User profile management
│
├── core/                   # 🚧 Backend Logic (Placeholder)
│   ├── __init__.py
│   ├── auth.py            # User authentication & registration
│   ├── data_processor.py  # CSV/PDF parsing & normalization
│   └── scheduler.py       # AI scheduling algorithm
│
└── data/                  # 📁 Data Storage
    ├── users.json         # User accounts (auto-generated)
    └── processed/         # Processed user data (auto-generated)
```

## 🎨 Component Architecture

### Layout Components ([components/layout.py](components/layout.py))
- `create_header()` - App header with user info
- `create_footer()` - App footer
- `create_page_container()` - Main content container
- `create_card_container()` - Card wrapper

### Form Components ([components/forms.py](components/forms.py))
- `create_input_field()` - Styled text input
- `create_file_upload()` - File upload with drag & drop
- `create_checkbox()` - Styled checkbox
- `create_select()` - Dropdown select
- `create_preference_form()` - Complete preference form

### Card Components ([components/cards.py](components/cards.py))
- `create_file_status_card()` - Upload status indicator
- `create_schedule_card()` - Schedule result display
- `create_analysis_step_card()` - Processing step indicator
- `create_stat_card()` - Statistics display

### Button Components ([components/buttons.py](components/buttons.py))
- `create_primary_button()` - Main action button
- `create_secondary_button()` - Secondary action
- `create_outline_button()` - Outlined button
- `create_link_button()` - Navigation link

### Loader Components ([components/loaders.py](components/loaders.py))
- `create_loading_spinner()` - Loading indicator
- `create_progress_bar()` - Progress tracking
- `create_skeleton_card()` - Loading skeleton
- `simulate_processing()` - Async processing simulation

## 🔄 Page Flow

```
/ (root)
  ↓
/signin ←→ /signup
  ↓
/upload (with preferences)
  ↓
/processing (real-time progress)
  ↓
/results (2 schedule options)
  ↓
/profile (user settings)
```

## 🧩 Features Implemented

### ✅ Phase 1: UI & Structure (COMPLETED)
- [x] Clean, modern UI design
- [x] Component-based architecture
- [x] All page structures created
- [x] Navigation and routing
- [x] Mock data flow
- [x] File upload interface
- [x] Preference form
- [x] Real-time processing visualization
- [x] Schedule result cards
- [x] User profile management

### 🚧 Phase 2: Backend Logic (TODO)
- [ ] Implement authentication in [core/auth.py](core/auth.py)
- [ ] Add CSV/PDF parsing in [core/data_processor.py](core/data_processor.py)
- [ ] Build constraint analysis
- [ ] Implement preference scoring
- [ ] Create schedule optimization algorithm
- [ ] Add data validation
- [ ] Implement export functionality

## 🎯 Key Design Decisions

1. **Component-Based**: All UI elements are reusable components
2. **Mock Data**: UI works with placeholder data for demonstration
3. **Clean Separation**: UI (pages/) and logic (core/) are separate
4. **No Database**: Uses JSON for lightweight storage
5. **Extensible**: Easy to add new features and constraints

## 🚀 Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python3 app.py

# Access at: http://localhost:8080
```

## 📝 Next Steps

1. **Implement Authentication**: Complete [core/auth.py](core/auth.py) with password hashing
2. **Add Data Parsing**: Implement CSV/PDF parsing with pandas and pdfplumber
3. **Build Scheduler**: Create constraint-based scheduling algorithm
4. **Add Validation**: Validate uploaded data format and content
5. **Export Features**: Add schedule export (CSV, PDF, iCal)
6. **Testing**: Add unit tests for core modules

## 💡 Tips for Development

- UI is ready - focus on backend logic
- Use the mock data structure as reference
- Core modules have TODO comments marking where to add logic
- Test each module independently before integration
- Keep the clean UI/backend separation

---

**Status**: Phase 1 Complete ✅ | Phase 2 Ready to Start 🚧
