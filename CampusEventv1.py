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

    .nav-item-active {
        background-color: #ffffff !important;
        color: #E03E2D !important;
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
        padding: 10px 0px;
        height: auto;
        line-height: 1.2;
        font-size: 11px;
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

    /* Hide default Streamlit sidebar radio selector but keep functionality */
    div[data-testid="stSidebarUserContent"] .stRadio {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA PERSISTENCE ---
# Initialize Users
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

if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = {} # Store as dict of list {username: [event_ids]}

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "📡 Feed"

# --- AUTHENTICATION UI ---
def show_login_page():
    st.markdown('<h1 style="text-align: center; color: #ffd700;">🎓 Campus Hub Login</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.logged_in_user = username
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("Choose Username")
            new_pass = st.text_input("Choose Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            reg_submit = st.form_submit_button("Create Account")
            
            if reg_submit:
                if not new_user or not new_pass:
                    st.warning("Please fill in all fields.")
                elif new_user in st.session_state.users:
                    st.error("Username already exists.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                else:
                    st.session_state.users[new_user] = new_pass
                    st.success("Account created! You can now login.")

# --- MAIN APP LOGIC ---
def add_event(title, edate, etime, loc, cat, org, desc):
    if st.session_state.events:
        new_id = max(e['id'] for e in st.session_state.events) + 1
    else:
        new_id = 1
    st.session_state.events.append({
        "id": new_id, "title": title, "date": edate, "time": etime.strftime("%H:%M"),
        "location": loc, "category": cat, "organizer": org, "description": desc, "attendees": 0
    })

# Check if user is logged in
if st.session_state.logged_in_user is None:
    show_login_page()
else:
    # --- NAVIGATION SIDEBAR ---
    with st.sidebar:
        # Account Section
        st.markdown(f"""
            <div class="nav-item">
                <div class="nav-icon" style="background: #555; border-radius: 50%; width: 40px; height: 40px; line-height: 40px; margin: 0 auto 5px auto;">👤</div>
                <div class="nav-text" style="color: #00acee;">{st.session_state.logged_in_user}</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", key="logout_btn", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()

        st.markdown("---")

        nav_items = [
            {"id": "📡 Feed", "label": "Feed", "icon": "📡"},
            {"id": "🗓️ Calendar", "label": "Calendar", "icon": "📅"},
            {"id": "➕ Post", "label": "Announce", "icon": "➕"},
            {"id": "🔖 Saved", "label": "Inbox", "icon": "🔖"},
            {"id": "❓ Help", "label": "Help", "icon": "❓"}
        ]

        for item in nav_items:
            if st.button(f"{item['icon']}\n{item['label']}", key=f"nav_{item['id']}", use_container_width=True):
                st.session_state.active_tab = item['id']
                st.rerun()

    # --- MAIN CONTENT ---
    choice = st.session_state.active_tab
    current_user = st.session_state.logged_in_user
    
    # Initialize user bookmarks if not exists
    if current_user not in st.session_state.bookmarks:
        st.session_state.bookmarks[current_user] = []

    if choice == "📡 Feed":
        st.markdown(f'<h1 class="main-title">🎓 Event Feed</h1>', unsafe_allow_html=True)
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
                    <p>📅 {ev['date']} | ⏰ {ev['time']} | 📍 {ev['location']}</p>
                    <p>👤 <b>Organizer:</b> {ev['organizer']}</p>
                    <p><i>{ev['description']}</i></p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns([1, 4])
                with c1:
                    if st.button("Join / Save", key=f"join_{ev['id']}"):
                        if ev['id'] not in st.session_state.bookmarks[current_user]:
                            st.session_state.bookmarks[current_user].append(ev['id'])
                            st.toast(f"Saved {ev['title']}!")
                        else:
                            st.toast("Already bookmarked!")

    elif choice == "🗓️ Calendar":
        st.header("Event Schedule")
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

    elif choice == "➕ Post":
        st.header("Post a New Event")
        with st.form("event_form", clear_on_submit=True):
            title = st.text_input("Event Title*")
            col1, col2 = st.columns(2)
            with col1: edate = st.date_input("Date", value=date.today())
            with col2: etime = st.time_input("Time")
            loc = st.text_input("Location")
            cat = st.selectbox("Category", ["Workshop", "Social", "Sports", "Academic"])
            org = st.text_input("Organizer (Club/Dept)*", value=current_user)
            desc = st.text_area("Description")
            
            if st.form_submit_button("Post to Hub 🚀"):
                if title and org:
                    add_event(title, edate, etime, loc, cat, org, desc)
                    st.success(f"Successfully posted '{title}'!")
                    st.balloons()
                else:
                    st.error("Please provide both an Event Title and an Organizer.")

    elif choice == "🔖 Saved":
        st.header("Your Saved Events")
        user_bookmarks = st.session_state.bookmarks[current_user]
        bookmarked = [e for e in st.session_state.events if e['id'] in user_bookmarks]
        
        if not bookmarked:
            st.info("You haven't saved any events yet.")
        else:
            for ev in bookmarked:
                with st.expander(f"📌 {ev['title']} - {ev['date']}"):
                    st.write(f"**Location:** {ev['location']}")
                    st.write(f"**Time:** {ev['time']}")
                    st.write(f"**Description:** {ev['description']}")
                    if st.button(f"Remove Bookmark", key=f"rem_{ev['id']}"):
                        st.session_state.bookmarks[current_user].remove(ev['id'])
                        st.rerun()

    elif choice == "❓ Help":
        st.header("Help & Support")
        st.markdown(f"Logged in as: **{current_user}**")
        st.markdown("""
        ### Quick Guide
        - Register if you are a new student.
        - Login to join events or post your own.
        - Saved events are private to your account.
        """)
