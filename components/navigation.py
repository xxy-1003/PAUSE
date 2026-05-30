"""
Top Navigation Component for PAUSE App
This provides consistent top navigation across all pages
"""

import streamlit as st

def create_top_navigation(current_page="Home"):
    """
    Create a top navigation bar that is always visible
    
    Args:
        current_page: The current page name ("Home", "Timer", "Analytics")
    """
    
    # CSS for top navigation
    st.markdown("""
    <style>
        /* Top Navigation Bar */
        .top-nav {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
            padding: 1rem;
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.05) 0%, rgba(75, 0, 130, 0.05) 100%);
            border-radius: 12px;
            border: 1px solid rgba(138, 43, 226, 0.1);
        }
        
        .nav-button {
            background: transparent;
            color: #4B0082;
            border: 2px solid #8A2BE2;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        
        .nav-button:hover {
            background: linear-gradient(135deg, #8A2BE2, #4B0082);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
        }
        
        .nav-button.active {
            background: linear-gradient(135deg, #8A2BE2, #4B0082);
            color: white;
            border-color: #4B0082;
        }
        
        .nav-button.active:hover {
            background: linear-gradient(135deg, #4B0082, #8A2BE2);
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Create navigation columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Home button
        home_active = "active" if current_page == "Home" else ""
        if st.button("🏠 Home", use_container_width=True, type="primary" if current_page == "Home" else "secondary"):
            if current_page != "Home":
                st.switch_page("app.py")
    
    with col2:
        # Timer button
        timer_active = "active" if current_page == "Timer" else ""
        if st.button("⏱ Timer", use_container_width=True, type="primary" if current_page == "Timer" else "secondary"):
            if current_page != "Timer":
                st.switch_page("pages/1_Timer.py")
    
    with col3:
        # Analytics button
        analytics_active = "active" if current_page == "Analytics" else ""
        if st.button("📊 Analytics", use_container_width=True, type="primary" if current_page == "Analytics" else "secondary"):
            if current_page != "Analytics":
                st.switch_page("pages/2_Analytics.py")
    
    # Add a separator
    st.markdown("---")