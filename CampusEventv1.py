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

    /* Hide default Streamlit sidebar radio selector but keep functionality */
    div[data-testid="stSidebarUserContent"] .stRadio {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA PERSISTENCE ---
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
    st.session_state.bookmarks = []

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "📡 Feed"

if 'editing_event_id' not in st.session_state:
    st.session_state.editing_event_id = None

# --- APP LOGIC ---

def add_event(title, edate, etime, loc, cat, org, desc):
    if st.session_state.events:
        new_id = max(e['id'] for e in st.session_state.events) + 1
    else:
        new_id = 1
    st.session_state.events.append({
        "id": new_id, "title": title, "date": edate, "time": etime.strftime("%H:%M"),
        "location": loc, "category": cat, "organizer": org, "description": desc, "attendees": 0
    })

def update_event(event_id, title, edate, etime, loc, cat, org, desc):
    for i, ev in enumerate(st.session_state.events):
        if ev['id'] == event_id:
            st.session_state.events[i] = {
                "id": event_id, "title": title, "date": edate,
                "time": etime.strftime("%H:%M") if hasattr(etime, 'strftime') else etime,
                "location": loc, "category": cat, "organizer": org, "description": desc,
                "attendees": ev.get('attendees', 0)
            }
            break

# --- NAVIGATION SIDEBAR (Canvas LMS Style) ---
with st.sidebar:
    # Account Icon (Visual only)
    st.markdown("""
        <div class="nav-item">
            <div class="nav-icon" style="background: #555; border-radius: 50%; width: 40px; height: 40px; line-height: 40px; margin: 0 auto 5px auto;">👤</div>
            <div class="nav-text" style="color: #00acee;">Account</div>
        </div>
    """, unsafe_allow_html=True)

    nav_items = [
        {"id": "📡 Feed", "label": "Feed", "icon": "📡"},
        {"id": "🗓️ Calendar", "label": "Calendar", "icon": "📅"},
        {"id": "➕ Post", "label": "Announce", "icon": "➕"},
        {"id": "🔖 Saved", "label": "Inbox", "icon": "🔖"},
        {"id": "❓ Help", "label": "Help", "icon": "❓"}
    ]

    for item in nav_items:
        is_active = st.session_state.active_tab == item['id']
        
        # We use standard Streamlit buttons styled via CSS to behave like the Nav Items
        if st.button(f"{item['icon']}\n{item['label']}", key=f"nav_{item['id']}", use_container_width=True):
            st.session_state.active_tab = item['id']
            st.rerun()

# --- MAIN CONTENT ---
choice = st.session_state.active_tab

if choice == "📡 Feed":
    st.markdown('<h1 class="main-title">🎓 Event Feed</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search events...", "")
    with col2:
        cat_filter = st.selectbox("Category", ["All", "Workshop", "Social", "Sports", "Academic"])

    # Show events in reverse chronological order
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
            
            # Action buttons for the feed
            c1, c2 = st.columns([1, 4])
            with c1:
                if st.button("Join / Save", key=f"join_{ev['id']}"):
                    if ev['id'] not in st.session_state.bookmarks:
                        st.session_state.bookmarks.append(ev['id'])
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
    st.write("Share an activity with the campus community.")
    with st.form("event_form", clear_on_submit=True):
        title = st.text_input("Event Title*")
        col1, col2 = st.columns(2)
        with col1: 
            edate = st.date_input("Date", value=date.today())
        with col2: 
            etime = st.time_input("Time")
        loc = st.text_input("Location")
        cat = st.selectbox("Category", ["Workshop", "Social", "Sports", "Academic"])
        org = st.text_input("Organizer (Club/Dept)*")
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
    bookmarked = [e for e in st.session_state.events if e['id'] in st.session_state.bookmarks]
    
    if not bookmarked:
        st.info("You haven't saved any events yet. Check the Feed to find interesting activities!")
    else:
        for ev in bookmarked:
            with st.expander(f"📌 {ev['title']} - {ev['date']}"):
                st.write(f"**Location:** {ev['location']}")
                st.write(f"**Time:** {ev['time']}")
                st.write(f"**Description:** {ev['description']}")
                if st.button(f"Remove Bookmark", key=f"rem_{ev['id']}"):
                    st.session_state.bookmarks.remove(ev['id'])
                    st.rerun()

elif choice == "❓ Help":
    st.header("Help & Support")
    st.markdown("""
    ### Welcome to the Campus Event Hub!
    
    - **📡 Feed**: Browse all upcoming events on campus.
    - **🗓️ Calendar**: See events in a structured list view.
    - **➕ Post**: Create and share your own events.
    - **🔖 Saved**: Access events you've joined or saved for later.
    
    If you encounter any issues, please contact the student support team.
    """)
