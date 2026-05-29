# PAUSE - Wellness Productivity Dashboard

A beautiful, modern Streamlit dashboard for wellness-focused productivity tracking with a soft purple and white color palette.

![PAUSE Dashboard](https://img.shields.io/badge/PAUSE-Wellness%20Dashboard-8A2BE2)

## Features

### 🏠 Dashboard (Homepage)
- **Modern Wellness Design**: Soft purple and white color palette with clean minimalist layout
- **Daily Focus Tracking**: Monitor daily focus time and productivity metrics
- **Quick Overview**: Today's summary with key metrics at a glance
- **Navigation Hub**: Easy access to all PAUSE features via beautiful cards
- **Daily Inspiration**: Motivational quotes with refresh button

### ⏱️ Focus Timer Page
- **Pomodoro Timer**: Circular progress timer with visual countdown
- **Session Controls**: Start, pause, and reset buttons with intuitive interface
- **Session Management**: Customizable session lengths (15, 20, 25, 30, 45, 60 minutes)
- **Streak Tracking**: Session streak counter and daily completion tracking
- **Progress Visualization**: Visual progress bar showing sessions completed

### 📊 Analytics & Insights Page
- **Productivity Charts**: Interactive Plotly charts showing weekly trends
- **Performance Metrics**: Detailed KPIs with weekly comparisons
- **Focus Distribution**: Pie chart showing time allocation across activities
- **Monthly Progress**: Heatmap visualization of consistency over time
- **Data Export**: Export reports, raw data, and charts

### 🧘 Wellness & Mindfulness Page
- **Burnout Risk Assessment**: Visual gauge with detailed factor analysis
- **Motivational Quotes**: Expanded library of inspirational quotes
- **Wellness Dashboard**: Mindfulness score, sleep quality, stress and energy levels
- **Personalized Tips**: AI-generated wellness recommendations
- **Mindfulness Resources**: Guided meditations, articles, and tools
- **Quick Wellness Actions**: One-click meditation, nature breaks, and stretching

### 🎨 Consistent UI Across All Pages
- **Purple & White Theme**: Modern, calming color palette
- **Rounded Cards**: Soft, modern card design with hover effects
- **Responsive Layout**: Optimized for all screen sizes
- **Professional Spacing**: Clean, startup-style appearance
- **Gradient Effects**: Subtle purple gradients for visual appeal

## Installation

1. **Clone or navigate to the PAUSE directory**
   ```bash
   cd c:\Assignment\PAUSE
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install streamlit plotly pandas numpy
   ```

## Running the Multi-Page App

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The app will automatically open in your default browser at `http://localhost:8501`
   - If it doesn't open automatically, manually navigate to the URL shown in the terminal

3. **Navigate Between Pages**
   - **Dashboard**: Homepage with overview and navigation (`app.py`)
   - **Timer**: Focus timer with Pomodoro functionality (`pages/1_Timer.py`)
   - **Analytics**: Productivity charts and insights (`pages/2_Analytics.py`)
   - **Wellness**: Mindfulness and burnout assessment (`pages/3_Wellness.py`)

4. **Use Navigation Features**
   - Click navigation cards on the Dashboard to go to specific pages
   - Use "Back to Dashboard" buttons on each page to return home
   - Streamlit automatically shows page navigation in the sidebar

## Dashboard Components

### Main Dashboard
- **App Title**: "PAUSE" with subtitle "Focus smart. Live well."
- **Top Metrics**: Daily focus time, productivity score, breaks taken, mindfulness minutes
- **Weekly Chart**: Dual-axis chart showing focus hours and productivity scores
- **Focus Session Controls**: Start timed sessions with ambient sounds and goals

### Sidebar Navigation
- **Navigation Menu**: Dashboard, Focus Sessions, Wellness Stats, Settings
- **User Stats**: Focus streak and weekly goal progress
- **Quick Actions**: Refresh data, export reports, notifications
- **User Profile**: Wellness level with progress indicator

### Right Column Features
- **Burnout Risk Card**: Visual gauge showing risk level with factors
- **Motivational Quote**: Daily inspirational quote with refresh button
- **Silent Focus Room**: Preview of virtual co-working space
- **Wellness Tips**: Hydration reminders, 20-20-20 rule, micro-meditation

## Technical Details

- **Framework**: Streamlit multi-page application
- **Architecture**: Modular page structure with shared styling
- **Charts**: Plotly for interactive, beautiful visualizations
- **Styling**: Custom CSS with consistent purple theme across all pages
- **Data**: Sample data generation (no external APIs required)
- **Layout**: Responsive wide layout with consistent card-based design
- **Navigation**: Streamlit page system with custom navigation buttons
- **State Management**: Session state for timer functionality

## Color Palette

- **Primary Purple**: `#8A2BE2`
- **Light Purple**: `#E6E6FA`
- **Lighter Purple**: `#F5F0FF`
- **Dark Purple**: `#4B0082`
- **White**: `#FFFFFF`
- **Light Gray**: `#F8F9FA`

## Development

The app is structured with:
- **Modular code** with separate functions for data generation
- **Custom CSS** for consistent styling
- **Interactive components** with hover effects and animations
- **Responsive design** that works on different screen sizes

## Requirements

- Python 3.8+
- Streamlit 1.35.0+
- Plotly 5.24.1+
- Pandas 2.2.3+
- NumPy 1.26.4+

## License

This project is created for educational and demonstration purposes.

---

**PAUSE** - Because productivity should feel good, not stressful. 🧘✨