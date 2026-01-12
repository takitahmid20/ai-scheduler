# 🎨 UI Pages Overview

## Page-by-Page Breakdown

### 1️⃣ Sign In Page ([pages/signin.py](pages/signin.py))

**Route**: `/signin`

**Features**:
- Clean welcome message
- Email input field
- Password input field
- Primary "Sign In" button
- Links to "Forgot password?" and "Sign up"

**User Flow**:
```
User enters email & password → Click "Sign In" → Navigate to /upload
```

---

### 2️⃣ Sign Up Page ([pages/signup.py](pages/signup.py))

**Route**: `/signup`

**Features**:
- Full name input
- Email input
- Student ID input
- Department dropdown (CS, Engineering, Business, Math)
- Password input
- Confirm password input
- Primary "Create Account" button
- Link to sign in

**Validation**:
- All fields required
- Password matching
- Success notification on completion

---

### 3️⃣ Upload Page ([pages/upload.py](pages/upload.py))

**Route**: `/upload`

**Features**:
- **File Upload Section**:
  - 4 file upload zones (courses, faculty, timeslots, exams)
  - Accepts CSV and PDF files
  - Status cards showing upload progress
  - Visual feedback (✓ Uploaded / Pending)

- **Preferences Section** (Optional):
  - Time preference dropdown (Morning/Afternoon/Evening)
  - Checkbox: "Prioritize exam conflict avoidance"
  - Checkbox: "Maximize free days"
  - Text input: "Preferred faculty"

- **Action Button**:
  - "Generate Schedules" (disabled until all files uploaded)

**User Flow**:
```
Upload 4 required files → Set preferences (optional) → Click "Generate" → Navigate to /processing
```

---

### 4️⃣ Processing Page ([pages/processing.py](pages/processing.py))

**Route**: `/processing`

**Features**:
- Real-time progress visualization
- 5 analysis steps with status indicators:
  1. Reading uploaded files
  2. Extracting course data
  3. Analyzing constraints
  4. Checking exam conflicts
  5. Generating optimal schedules

- Progress bar showing overall completion (0-100%)
- Animated step indicators (unchecked → active → completed)

**Animation**:
- Each step takes ~2 seconds
- Visual transition from one step to next
- Auto-navigates to /results when complete

---

### 5️⃣ Results Page ([pages/results.py](pages/results.py))

**Route**: `/results`

**Features**:
- **Summary Statistics**:
  - Total Courses (5)
  - Zero Conflicts (✓)
  - Options Generated (2)

- **Schedule Cards** (2 options):
  - Card header with title
  - Favorite button (star icon)
  - Download button
  - Badges showing:
    - Conflicts count
    - Free days count
    - Total courses
  - Detailed course list with:
    - Course name
    - Time slot
    - Faculty name

- **Action Buttons**:
  - "Upload New Data" (secondary)
  - "Download All" (primary)

**Interactions**:
- Click star to favorite/unfavorite
- Click download to export schedule
- Visual distinction for favorited schedules (blue border)

---

### 6️⃣ Profile Page ([pages/profile.py](pages/profile.py))

**Route**: `/profile`

**Features**:
- **Personal Information Card**:
  - Full name (editable)
  - Email (editable)
  - Student ID (read-only)
  - Department dropdown
  - Current semester dropdown

- **Change Password Card**:
  - Current password input
  - New password input
  - Confirm new password input

- **Action Buttons**:
  - "Cancel" (secondary)
  - "Save Changes" (primary)

**User Flow**:
```
Edit fields → Click "Save Changes" → Success notification
```

---

## 🎨 Design System

### Colors
- **Primary**: Blue (#2563eb)
- **Success**: Green
- **Warning**: Yellow
- **Danger**: Red
- **Neutral**: Gray scale

### Typography
- **Page titles**: 3xl, bold
- **Section titles**: xl, semibold
- **Card titles**: lg, semibold
- **Body text**: base, regular
- **Labels**: sm, medium

### Spacing
- **Page container**: max-w-6xl, mx-auto, p-8
- **Card padding**: p-6
- **Gap between elements**: gap-4 to gap-8

### Components
- **Buttons**: Rounded (rounded-lg)
- **Cards**: Shadowed (shadow-md) with borders
- **Inputs**: Full width with labels
- **Icons**: Material Design icons

---

## 📱 Responsive Design

All pages use:
- Flexbox columns for mobile
- Max-width containers for desktop
- Responsive padding and gaps
- Scalable icons and buttons

---

## ✨ User Experience Features

### Visual Feedback
- ✅ Success notifications (green)
- ⚠️ Warning notifications (yellow)
- ❌ Error notifications (red)
- ℹ️ Info notifications (blue)

### Loading States
- Spinners during processing
- Progress bars with percentages
- Skeleton screens for loading content
- Animated step indicators

### Interactive Elements
- Hover effects on buttons
- Click feedback
- Icon animations
- Color transitions

### Navigation
- Automatic redirects after actions
- Breadcrumb-style progress
- Back/forward navigation
- Direct route access

---

## 🔄 Complete User Journey

```
1. START
   ↓
2. /signin or /signup (Create account or login)
   ↓
3. /upload (Upload 4 required files + set preferences)
   ↓
4. Click "Generate Schedules"
   ↓
5. /processing (Watch real-time progress)
   ↓
6. /results (View 2 optimal schedules)
   ↓
7. Actions:
   - Favorite schedules (star icon)
   - Download schedules
   - Upload new data (back to step 3)
   - View/edit profile (/profile)
```

---

## 🎯 UI Highlights

### What Makes This UI Great

1. **Clean & Modern**: No clutter, focused design
2. **Component-Based**: Easy to maintain and extend
3. **Visual Feedback**: Users always know what's happening
4. **Intuitive Flow**: Natural progression through steps
5. **Professional**: Ready for presentation
6. **Accessible**: Clear labels, good contrast, proper spacing

### Mock Data Quality

- Realistic course names and times
- Proper faculty names
- Sensible preferences
- Professional styling
- Production-ready appearance

---

## 🚀 Running & Testing

```bash
# Start the app
python3 app.py

# Test the flow
1. Visit http://localhost:8080
2. Navigate to /signup
3. Create an account
4. Go to /upload
5. Upload files (mock upload)
6. Set preferences
7. Click "Generate Schedules"
8. Watch /processing animation
9. View results at /results
10. Test favorite/download buttons
```

---

**Status**: All UI pages complete and functional! ✅
