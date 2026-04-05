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

    /* Auth Box styling */
    .auth-container {
        max-width: 400px;
        margin: auto;
        padding: 40px;
        background-color: #1c2128;
        border-radius: 15px;
        border: 1px solid #30363d;
        text-align: center;
    }

    /* Hide default Streamlit sidebar radio selector */
    div[data-testid="stSidebarUserContent"] .stRadio {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA PERSISTENCE ---
if 'users' not in st.session_state:
    st.session_state.users = {
        "admin": "password123",
        "student": "canvas2024"
    }

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

if 'events' not in st.session_state:
    st.session_state.events = [
        {
            "id": 1,
            "title": "Python Workshop for Beginners",
            "date": date(2024, 4, 15),
            "time": "14:00",
            "location": "IT Lab 4",
            "category": "Workshop",
            "organizer": "Coding Club",
            "description": "Learn the basics of Python programming in this hands-on session. No prior experience required!",
            "attendees": 12
        },
        {
            "id": 2,
            "title": "Spring Music Festival",
            "date": date(2024, 4, 20),
            "time": "18:00",
            "location": "Main Courtyard",
            "category": "Social",
            "organizer": "Music Society",
            "description": "Enjoy a night of live performances from local student bands and solo artists.",
            "attendees": 45
        }
    ]

# Ensure bookmarks is always initialized as a dictionary
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = {}

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "📊 Dashboard"

# --- AUTHENTICATION UI ---
def show_login_page():
    st.markdown('<h1 style="text-align: center; color: #ffd700;">🎓 Campus Hub Login</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In", use_container_width=True)
                
                if submit:
                    if username in st.session_state.users and st.session_state.users[username] == password:
                        st.session_state.logged_in_user = username
                        # Initialize user bookmarks upon login if they don't exist
                        if username not in st.session_state.bookmarks:
                            st.session_state.bookmarks[username] = []
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
        
        with tab2:
            with st.form("register_form"):
                new_user = st.text_input("Choose Username")
                new_pass = st.text_input("Choose Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                reg_submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if reg_submit:
                    if not new_user or not new_pass:
                        st.warning("Please fill in all fields.")
                    elif new_user in st.session_state.users:
                        st.error("Username already exists.")
                    elif new_pass != confirm_pass:
                        st.error("Passwords do not match.")
                    else:
                        st.session_state.users[new_user] = new_pass
                        st.session_state.bookmarks[new_user] = []
                        st.success("Account created! You can now login.")

# --- MAIN APP LOGIC ---
def add_event(title, edate, etime, loc, cat, org, desc):
    new_id = max([e['id'] for e in st.session_state.events]) + 1 if st.session_state.events else 1
    st.session_state.events.append({
        "id": new_id, "title": title, "date": edate, "time": etime.strftime("%H:%M"),
        "location": loc, "category": cat, "organizer": org, "description": desc, "attendees": 0
    })

# Check if user is logged in
if st.session_state.logged_in_user is None:
    show_login_page()
else:
    # --- NAVIGATION SIDEBAR (Canvas Style) ---
    current_user = st.session_state.logged_in_user
    
    with st.sidebar:
        # Account Section
        st.markdown(f"""
            <div class="nav-item">
                <div class="nav-icon" style="background: #555; border-radius: 50%; width: 40px; height: 40px; line-height: 40px; margin: 0 auto 5px auto;">👤</div>
                <div class="nav-text" style="color: #ffffff; font-weight: bold;">Account</div>
                <div style="font-size: 10px; color: #aaa;">{current_user}</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", key="logout_btn", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()

        st.markdown("---")

        # Match labels to the Canvas image icons
        nav_items = [
            {"id": "📊 Dashboard", "label": "Dashboard", "icon": "⏲️"},
            {"id": "📚 Courses", "label": "Courses", "icon": "📖"},
            {"id": "🗓️ Calendar", "label": "Calendar", "icon": "📅"},
            {"id": "📥 Inbox", "label": "Inbox", "icon": "📥"},
            {"id": "❓ Help", "label": "Help", "icon": "❓"}
        ]

        for item in nav_items:
            # Note: We display the icon and label stacked to mimic the Canvas look
            if st.button(f"{item['icon']}\n{item['label']}", key=f"nav_{item['id']}", use_container_width=True):
                st.session_state.active_tab = item['id']
                st.rerun()

    # --- MAIN CONTENT ---
    choice = st.session_state.active_tab
    
    # Safety check for bookmarks
    if current_user not in st.session_state.bookmarks:
        st.session_state.bookmarks[current_user] = []

    if choice == "📊 Dashboard":
        st.markdown(f'<h1 class="main-title">🎓 Event Dashboard</h1>', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            search = st.text_input("🔍 Search events...", "")
        with col2:
            cat_filter = st.selectbox("Category", ["All", "Workshop", "Social", "Sports", "Academic"])

        for ev in reversed(st.session_state.events):
            if search.lower() in ev['title'].lower() and (cat_filter == "All" or ev['category'] == cat_filter):
                st.markdown(f"""
                <div class="event-card">
                    <h3>{ev['title']}</h3>
                    <div class="event-details">
                        <b>📅 Date:</b> {ev['date']} | <b>⏰ Time:</b> {ev['time']} | <b>📍 Location:</b> {ev['location']}<br>
                        <b>👤 Organizer:</b> {ev['organizer']}<br><br>
                        <i>{ev['description']}</i>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns([1, 4])
                with c1:
                    is_saved = ev['id'] in st.session_state.bookmarks[current_user]
                    btn_label = "✅ Saved" if is_saved else "📥 Join/Save"
                    if st.button(btn_label, key=f"join_{ev['id']}", disabled=is_saved):
                        st.session_state.bookmarks[current_user].append(ev['id'])
                        st.rerun()

    elif choice == "📚 Courses":
        st.header("Academic Activities & Courses")
        st.info("This section displays academic-related events and study groups.")
        academic_events = [e for e in st.session_state.events if e['category'] == "Academic"]
        if academic_events:
            for ev in academic_events:
                st.write(f"📖 **{ev['title']}** - {ev['date']} at {ev['location']}")
        else:
            st.write("No academic events currently scheduled.")

    elif choice == "🗓️ Calendar":
        st.header("Schedule Overview")
        if st.session_state.events:
            df = pd.DataFrame(st.session_state.events)
            df['date'] = pd.to_datetime(df['date'])
            st.dataframe(
                df[['date', 'title', 'location', 'category', 'organizer']].sort_values('date'), 
                use_container_width=True, 
                hide_index=True
            )
        else:
            st.info("No events scheduled yet.")

    elif choice == "📥 Inbox":
        st.header("Your Saved Events (Inbox)")
        user_bookmarks = st.session_state.bookmarks.get(current_user, [])
        bookmarked = [e for e in st.session_state.events if e['id'] in user_bookmarks]
        
        if not bookmarked:
            st.info("Your inbox is empty. Save events from the Dashboard to see them here.")
        else:
            for ev in bookmarked:
                with st.expander(f"📌 {ev['title']} - {ev['date']}"):
                    st.write(f"**Location:** {ev['location']}")
                    st.write(f"**Time:** {ev['time']}")
                    st.write(f"**Description:** {ev['description']}")
                    if st.button(f"Remove from Inbox", key=f"rem_{ev['id']}"):
                        st.session_state.bookmarks[current_user].remove(ev['id'])
                        st.rerun()
        
        st.divider()
        st.subheader("Post a New Announcement")
        with st.form("event_form", clear_on_submit=True):
            title = st.text_input("Event Title*")
            col1, col2 = st.columns(2)
            with col1: edate = st.date_input("Date", value=date.today())
            with col2: etime = st.time_input("Time")
            loc = st.text_input("Location")
            cat = st.selectbox("Category", ["Workshop", "Social", "Sports", "Academic"])
            org = st.text_input("Organizer*", value=current_user)
            desc = st.text_area("Description")
            
            if st.form_submit_button("Post Announcement 🚀"):
                if title and org:
                    add_event(title, edate, etime, loc, cat, org, desc)
                    st.success(f"Successfully posted '{title}'!")
                else:
                    st.error("Please provide both an Event Title and an Organizer.")

    elif choice == "❓ Help":
        st.header("Help & Support")
        st.markdown(f"**User:** {current_user}")
        st.markdown("""
        ### Navigation Guide
        - **Dashboard**: Browse and search all campus events. Click 'Join/Save' to track them.
        - **Courses**: Focus on academic workshops and study sessions.
        - **Calendar**: View a tabular list of all upcoming dates.
        - **Inbox**: Manage your personal list of saved events and post new announcements.
        """)
