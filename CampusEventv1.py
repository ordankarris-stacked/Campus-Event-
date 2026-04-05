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

    /* Custom Navigation Item Styling */
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 15px 5px;
        color: #ffffff;
        text-decoration: none;
        transition: background 0.3s;
        cursor: pointer;
        text-align: center;
    }
    
    .nav-item:hover {
        background-color: #2d2d2d;
    }

    .nav-icon {
        font-size: 24px;
        margin-bottom: 5px;
    }

    .nav-text {
        font-size: 12px;
        font-weight: 500;
    }

    /* Standard high visibility colors */
    h1, h2, h3, .stMarkdown p {
        color: #ffffff !important;
    }
    
    .main-title {
        color: #ffd700 !important; 
        font-weight: 800;
        font-size: 2.5rem;
    }

    /* Event Card Styling */
    .event-card { 
        padding: 25px; 
        border-radius: 12px; 
        border: 1px solid #30363d;
        border-left: 5px solid #ffd700;
        background-color: #1c2128;
        margin-bottom: 20px;
    }
    
    .event-card h3 {
        color: #ffd700 !important;
        margin-bottom: 10px;
    }
    
    .event-details {
        color: #e6edf3 !important;
        font-size: 0.95rem;
        line-height: 1.6;
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
    .badge-admin { background-color: #ffd700; color: black; }
    
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
    .sec-law { background-color: #9C27B0; color: white; }

    /* Button styling */
    .stButton>button {
        background-color: #ffd700;
        color: #000000;
        font-weight: bold;
        border: none;
    }
    
    /* Sidebar button specifics to look like Nav items */
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
        color: white;
    }

    /* Account button specific style override */
    .account-nav-btn button {
        height: 100px !important;
    }

    /* Hide default Streamlit sidebar radio selector */
    div[data-testid="stSidebarUserContent"] .stRadio {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA PERSISTENCE ---
if 'users' not in st.session_state:
    # Pre-configured student accounts with their respective sections and passwords
    st.session_state.users = {
        "admin": {"password": "password123", "role": "Admin", "section": "Faculty"},
        "teacher_jane": {"password": "teach", "role": "Teacher", "section": "Faculty"},
        "studentA": {"password": "pass", "role": "Student", "section": "Business"},
        "studentB": {"password": "pass", "role": "Student", "section": "Computer"},
        "studentC": {"password": "pass", "role": "Student", "section": "Law"},
        "student": {"password": "canvas2024", "role": "Student", "section": "General"}
    }

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

if 'events' not in st.session_state:
    st.session_state.events = [
        {
            "id": 1,
            "title": "Introduction to Python Quiz",
            "date": date(2024, 4, 15),
            "time": "14:00",
            "location": "Online / Canvas",
            "category": "Quiz",
            "organizer": "teacher_jane",
            "description": "A mandatory quiz covering the first three weeks of Python basics.",
            "type": "Task"
        },
        {
            "id": 2,
            "title": "Spring Music Festival",
            "date": date(2024, 4, 20),
            "time": "18:00",
            "location": "Main Courtyard",
            "category": "Social",
            "organizer": "admin",
            "description": "Enjoy a night of live performances.",
            "type": "Event"
        }
    ]

if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = {}

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "📊 Dashboard"

# --- AUTHENTICATION UI ---
def show_login_page():
    st.markdown('<h1 style="text-align: center; color: #ffd700;">🎓 Campus LMS Login</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In", use_container_width=True)
                
                if submit:
                    if username in st.session_state.users:
                        stored_creds = st.session_state.users[username]
                        if stored_creds["password"] == password:
                            st.session_state.logged_in_user = username
                            if username not in st.session_state.bookmarks:
                                st.session_state.bookmarks[username] = []
                            st.rerun()
                        else:
                            st.error("Invalid password.")
                    else:
                        st.error("User not found.")
        
        with tab2:
            with st.form("register_form"):
                new_user = st.text_input("Choose Username")
                new_pass = st.text_input("Choose Password", type="password")
                role = st.selectbox("I am a...", ["Student", "Teacher"])
                # New section selection for registration
                section = st.selectbox("Section", ["Business", "Computer", "Law"]) if role == "Student" else "Faculty"
                reg_submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if reg_submit:
                    if not new_user or not new_pass:
                        st.warning("Please fill in all fields.")
                    elif new_user in st.session_state.users:
                        st.error("Username already exists.")
                    else:
                        st.session_state.users[new_user] = {"password": new_pass, "role": role, "section": section}
                        st.session_state.bookmarks[new_user] = []
                        st.success(f"Account created in {section} section! You can now login.")

# --- MAIN APP LOGIC ---
def add_event(title, edate, etime, loc, cat, org, desc, etype="Task"):
    new_id = max([e['id'] for e in st.session_state.events]) + 1 if st.session_state.events else 1
    st.session_state.events.append({
        "id": new_id, "title": title, "date": edate, "time": etime.strftime("%H:%M"),
        "location": loc, "category": cat, "organizer": org, "description": desc, "type": etype
    })

# Check if user is logged in
if st.session_state.logged_in_user is None:
    show_login_page()
else:
    current_user = st.session_state.logged_in_user
    user_data = st.session_state.users[current_user]
    user_role = user_data["role"]
    user_section = user_data.get("section", "General")
    
    # CSS helper for sections
    section_class = f"sec-{user_section.lower()}" if user_section in ["Business", "Computer", "Law"] else ""

    # --- NAVIGATION SIDEBAR (Canvas Style) ---
    with st.sidebar:
        # Account Section (Interactive Button)
        badge_class = f"badge-{user_role.lower()}"
        
        if st.button(f"👤\nAccount", key="nav_👤 Account", use_container_width=True):
            st.session_state.active_tab = "👤 Account"
            st.rerun()
            
        st.markdown(f"""
            <div style="text-align: center; margin-top: -15px; margin-bottom: 10px;">
                <div style="font-size: 10px; color: #aaa;">{current_user}</div>
                <div style="display: flex; justify-content: center; gap: 5px; align-items: center;">
                    <span class="role-badge {badge_class}">{user_role}</span>
                    {f'<span class="section-badge {section_class}">{user_section}</span>' if user_role == "Student" else ''}
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", key="logout_btn", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()

        st.markdown("---")

        nav_items = [
            {"id": "📊 Dashboard", "label": "Dashboard", "icon": "⏲️"},
            {"id": "📚 Courses", "label": "Courses", "icon": "📖"},
            {"id": "🗓️ Calendar", "label": "Calendar", "icon": "📅"},
            {"id": "📥 Inbox", "label": "Inbox", "icon": "📥"}
        ]
        
        if user_role in ["Teacher", "Admin"]:
            nav_items.insert(3, {"id": "📝 Assign", "label": "Assign", "icon": "✍️"})

        for item in nav_items:
            if st.button(f"{item['icon']}\n{item['label']}", key=f"nav_{item['id']}", use_container_width=True):
                st.session_state.active_tab = item['id']
                st.rerun()

    # --- MAIN CONTENT ---
    choice = st.session_state.active_tab
    
    if current_user not in st.session_state.bookmarks:
        st.session_state.bookmarks[current_user] = []

    if choice == "👤 Account":
        st.markdown(f'<h1 class="main-title">👤 User Profile</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
                <div style="background: #1c2128; padding: 40px; border-radius: 50%; width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; border: 2px solid #ffd700; margin: auto;">
                    <span style="font-size: 60px;">👤</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Account Details")
            st.write(f"**Username:** {current_user}")
            st.write(f"**Role:** {user_role}")
            if user_role == "Student":
                st.write(f"**Academic Section:** {user_section}")
            
            badge_class = f"badge-{user_role.lower()}"
            st.markdown(f"**Status:** <span class='role-badge {badge_class}'>Active {user_role}</span>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.info(f"You are currently recognized as a member of the **{user_section}** department. Your access level is set to **{user_role}**.")

    elif choice == "📊 Dashboard":
        st.markdown(f'<h1 class="main-title">🎓 {user_section} Dashboard</h1>', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("🔍 Search tasks/events...", "")
        with col2:
            cat_filter = st.selectbox("Type", ["All", "Quiz", "Assignment", "Task", "Social"])

        for ev in reversed(st.session_state.events):
            matches_search = search.lower() in ev['title'].lower()
            matches_cat = (cat_filter == "All" or ev['category'] == cat_filter)
            
            if matches_search and matches_cat:
                st.markdown(f"""
                <div class="event-card">
                    <h3>{ev['title']} <span style="font-size: 12px; color: #aaa;">({ev['category']})</span></h3>
                    <div class="event-details">
                        <b>📅 Due/Date:</b> {ev['date']} | <b>⏰ Time:</b> {ev['time']} | <b>📍 Location:</b> {ev['location']}<br>
                        <b>👤 Assigned by:</b> {ev['organizer']}<br><br>
                        <i>{ev['description']}</i>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns([1, 4])
                with c1:
                    is_saved = ev['id'] in st.session_state.bookmarks[current_user]
                    btn_label = "✅ Joined" if is_saved else "📥 Join Task"
                    if st.button(btn_label, key=f"join_{ev['id']}"):
                        if is_saved:
                            st.session_state.bookmarks[current_user].remove(ev['id'])
                        else:
                            st.session_state.bookmarks[current_user].append(ev['id'])
                        st.rerun()

    elif choice == "📝 Assign":
        if user_role not in ["Teacher", "Admin"]:
            st.error("Access Denied.")
        else:
            st.header("Assign New Task / Quiz")
            with st.form("assignment_form", clear_on_submit=True):
                title = st.text_input("Title (e.g., Math Quiz 1)*")
                col1, col2 = st.columns(2)
                with col1: edate = st.date_input("Due Date", value=date.today())
                with col2: etime = st.time_input("Due Time")
                loc = st.text_input("Location / Link", value="Canvas Online")
                cat = st.selectbox("Category", ["Assignment", "Quiz", "Task", "Discussion"])
                desc = st.text_area("Instructions / Description")
                
                if st.form_submit_button("Post to Students 🚀"):
                    if title:
                        add_event(title, edate, etime, loc, cat, current_user, desc, etype="Task")
                        st.success(f"Task '{title}' assigned.")
                    else:
                        st.error("Please provide a title.")

    elif choice == "🗓️ Calendar":
        st.header("Academic Calendar")
        if st.session_state.events:
            df = pd.DataFrame(st.session_state.events)
            st.dataframe(df[['date', 'title', 'category', 'organizer']].sort_values('date'), use_container_width=True, hide_index=True)

    elif choice == "📥 Inbox":
        st.header("My Active Tasks")
        user_bookmarks = st.session_state.bookmarks.get(current_user, [])
        bookmarked = [e for e in st.session_state.events if e['id'] in user_bookmarks]
        
        if not bookmarked:
            st.info("No active tasks.")
        else:
            for ev in bookmarked:
                with st.expander(f"📌 {ev['title']} - Due: {ev['date']}"):
                    st.write(f"**Instructions:** {ev['description']}")
                    if st.button("Unregister / Leave", key=f"rem_{ev['id']}"):
                        st.session_state.bookmarks[current_user].remove(ev['id'])
                        st.rerun()

    elif choice == "📚 Courses":
        st.header(f"Courses for {user_section}")
        if user_section == "Business":
            st.write("Current: Econ 101, Marketing, Finance Basics.")
        elif user_section == "Computer":
            st.write("Current: Python Basics, Data Structures, Web Dev.")
        elif user_section == "Law":
            st.write("Current: Civil Law, Criminal Justice, Ethics.")
        else:
            st.write("Select a course track from your advisor.")
