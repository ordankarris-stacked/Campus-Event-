import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Campus Event Hub", page_icon="🎓", layout="wide")

# Modern Dark Theme CSS with Canvas LMS Style Navigation
st.markdown("""
    <style>
    /* Force a dark background for the entire app */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Sidebar styling to match the provided photo (Canvas LMS style) */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        min-width: 100px !important;
        max-width: 120px !important;
        border-right: 1px solid #30363d;
    }

    /* Red top bar accent */
    [data-testid="stSidebar"]::before {
        content: "";
        display: block;
        height: 50px;
        background-color: #E03E2D; /* Canvas Red */
        margin-bottom: 10px;
    }

    /* Standard high visibility colors */
    h1, h2, h3, .stMarkdown p {
        color: #ffffff !important;
    }
    
    .main-title {
        color: #ffffff !important; 
        font-weight: 800;
        font-size: 2rem;
        margin-bottom: 20px;
    }

    /* Course Card Styling based on screenshot */
    .course-card {
        background-color: #ffffff;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #2d3b45;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .course-card-banner {
        height: 120px;
        width: 100%;
        position: relative;
    }
    
    .course-card-content {
        padding: 15px;
        flex-grow: 1;
        background-color: #ffffff;
    }
    
    .course-title {
        color: #E03E2D;
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 4px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .course-subtitle {
        font-size: 0.8rem;
        color: #556b7d;
        margin-bottom: 2px;
    }
    
    .course-term {
        font-size: 0.75rem;
        color: #7d8a96;
    }
    
    .course-card-footer {
        padding: 10px 15px;
        border-top: 1px solid #f5f5f5;
        display: flex;
        gap: 15px;
        color: #7d8a96;
    }

    /* Role Badge */
    .role-badge {
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        text-transform: uppercase;
        font-weight: bold;
        margin-top: 5px;
    }
    .badge-teacher { background-color: #E03E2D; color: white; }
    .badge-student { background-color: #00acee; color: white; }
    
    /* Section Badge Styles */
    .section-badge {
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        margin-left: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .sec-business { background-color: #4CAF50; color: white; }
    .sec-computer { background-color: #2196F3; color: white; }

    /* Button styling for sidebar */
    [data-testid="stSidebar"] .stButton>button {
        background-color: transparent;
        color: white;
        border: none;
        padding: 15px 0px;
        height: auto;
        line-height: 1.2;
        font-size: 11px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #2d2d2d;
        color: #E03E2D;
    }

    .stButton>button p { color: inherit !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'users' not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "password123", "role": "Admin", "section": "Faculty"},
        "student": {"password": "pass", "role": "Student", "section": "Computer"}
    }

# ORIGINAL COURSE DATA - Restored to website's original sections
if 'courses' not in st.session_state:
    st.session_state.courses = [
        {
            "id": "BUS101", 
            "name": "Economics & Marketing", 
            "code": "BUS-101 Business Fundamentals", 
            "term": "2024 - Semester 1", 
            "color": "#4CAF50",
            "section": "Business"
        },
        {
            "id": "CS101", 
            "name": "Python & Data Structures", 
            "code": "CS-101 Computer Science I", 
            "term": "2024 - Semester 1", 
            "color": "#2196F3",
            "section": "Computer"
        },
        {
            "id": "LAW101", 
            "name": "Civil Law & Ethics", 
            "code": "LAW-101 Introduction to Law", 
            "term": "2024 - Semester 1", 
            "color": "#9C27B0",
            "section": "Law"
        }
    ]

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = {}

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "📊 Dashboard"

# --- AUTHENTICATION UI ---
if st.session_state.logged_in_user is None:
    st.markdown('<h1 style="text-align: center; color: #ffffff;">🎓 Campus LMS</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                if u in st.session_state.users and st.session_state.users[u]["password"] == p:
                    st.session_state.logged_in_user = u
                    if u not in st.session_state.bookmarks:
                        st.session_state.bookmarks[u] = []
                    st.rerun()
                else: st.error("Login failed")
else:
    current_user = st.session_state.logged_in_user
    user_data = st.session_state.users[current_user]
    
    if current_user not in st.session_state.bookmarks:
        st.session_state.bookmarks[current_user] = []

    # --- SIDEBAR ---
    with st.sidebar:
        if st.button("👤\nAccount", use_container_width=True): st.session_state.active_tab = "👤 Account"
        st.markdown(f'<div style="text-align:center; font-size:10px; color:#aaa; margin-top:-10px;">{current_user}</div>', unsafe_allow_html=True)
        
        if st.button("⏲️\nDashboard", use_container_width=True): st.session_state.active_tab = "📊 Dashboard"
        if st.button("📖\nCourses", use_container_width=True): st.session_state.active_tab = "📚 Courses"
        if st.button("📅\nCalendar", use_container_width=True): st.session_state.active_tab = "🗓️ Calendar"
        if st.button("📥\nInbox", use_container_width=True): st.session_state.active_tab = "📥 Inbox"
        
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in_user = None
            st.rerun()

    # --- MAIN CONTENT ---
    if st.session_state.active_tab == "📊 Dashboard":
        st.markdown('<h1 class="main-title">Dashboard</h1>', unsafe_allow_html=True)
        
        # Course Grid Layout for the 3 original courses
        cols = st.columns(3)
        for i, course in enumerate(st.session_state.courses):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="course-card">
                    <div class="course-card-banner" style="background-color: {course['color']};">
                        <div style="position: absolute; right: 10px; top: 10px; color: white; cursor: pointer;">⋮</div>
                    </div>
                    <div class="course-card-content">
                        <div class="course-title">{course['code']}</div>
                        <div class="course-subtitle">{course['name']}</div>
                        <div class="course-term">{course['term']}</div>
                    </div>
                    <div class="course-card-footer">
                        <span>📢</span>
                        <span>📝</span>
                        <span>💬</span>
                        <span>📁</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.write("")

    elif st.session_state.active_tab == "📚 Courses":
        st.markdown('<h1 class="main-title">Academic Catalog</h1>', unsafe_allow_html=True)
        st.table(pd.DataFrame(st.session_state.courses)[['section', 'code', 'name', 'term']])

    else:
        st.info(f"Viewing {st.session_state.active_tab} - Content coming soon.")
