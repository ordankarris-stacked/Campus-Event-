import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Campus Event Hub", page_icon="🎓", layout="wide")

# Custom CSS for a modern University look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .event-card { 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #e0e0e0; 
        background-color: white;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .category-tag {
        padding: 2px 8px;
        border-radius: 15px;
        font-size: 0.8em;
        background-color: #e2e3e5;
        color: #383d41;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA PERSISTENCE (In-Memory for Demo) ---
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
            "description": "Learn the basics of Python programming in this hands-on session.",
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
            "description": "Annual live music performances by student bands.",
            "attendees": 45
        }
    ]

if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []

# --- APP LOGIC ---

def add_event(title, edate, etime, loc, cat, org, desc):
    new_id = len(st.session_state.events) + 1
    st.session_state.events.append({
        "id": new_id,
        "title": title,
        "date": edate,
        "time": etime.strftime("%H:%M"),
        "location": loc,
        "category": cat,
        "organizer": org,
        "description": desc,
        "attendees": 0
    })

# --- UI LAYOUT ---

st.title("🎓 Campus Event Hub")
st.markdown("Connect, Discover, and Engage with your University Community.")

# Navigation Sidebar
menu = ["📡 Event Feed", "🗓️ Calendar View", "➕ Announce Event", "🔖 My Bookmarks"]
choice = st.sidebar.radio("Navigation", menu)

# --- PAGE: EVENT FEED ---
if choice == "📡 Event Feed":
    st.header("Upcoming Activities")
    
    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Search events...", "")
    with col2:
        cat_filter = st.selectbox("Category", ["All", "Workshop", "Social", "Sports", "Academic"])

    for ev in st.session_state.events:
        # Apply filters
        if search.lower() in ev['title'].lower() and (cat_filter == "All" or ev['category'] == cat_filter):
            with st.container():
                st.markdown(f"""
                <div class="event-card">
                    <h3>{ev['title']}</h3>
                    <span class="category-tag">{ev['category']}</span>
                    <p>📅 <b>Date:</b> {ev['date']} | ⏰ <b>Time:</b> {ev['time']}</p>
                    <p>📍 <b>Location:</b> {ev['location']}</p>
                    <p>👤 <b>Organizer:</b> {ev['organizer']}</p>
                    <p>{ev['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns([1, 4])
                with c1:
                    if st.button(f"Join/Save", key=f"btn_{ev['id']}"):
                        if ev['id'] not in st.session_state.bookmarks:
                            st.session_state.bookmarks.append(ev['id'])
                            st.success("Bookmarked!")
                        else:
                            st.info("Already bookmarked.")

# --- PAGE: CALENDAR VIEW ---
elif choice == "🗓️ Calendar View":
    st.header("Event Schedule")
    
    # Simple Calendar logic using a DataFrame
    df = pd.DataFrame(st.session_state.events)
    df['date'] = pd.to_datetime(df['date'])
    
    # Show a list view sorted by date as a proxy for a calendar in Streamlit
    st.write("Overview of all scheduled dates:")
    st.dataframe(df[['date', 'title', 'location', 'category']].sort_values('date'), use_container_width=True)

# --- PAGE: ANNOUNCE EVENT ---
elif choice == "➕ Announce Event":
    st.header("Promote your Activity")
    st.info("Fill out the details below to broadcast your event to all students.")
    
    with st.form("event_form", clear_on_submit=True):
        title = st.text_input("Event Title*")
        col1, col2 = st.columns(2)
        with col1:
            edate = st.date_input("Date", min_value=date.today())
        with col2:
            etime = st.time_input("Time")
        
        loc = st.text_input("Location (Building/Room or Online)")
        cat = st.selectbox("Category", ["Workshop", "Social", "Sports", "Academic"])
        org = st.text_input("Organizer/Club Name")
        desc = st.text_area("Short Description")
        
        submitted = st.form_submit_button("Launch Event 🚀")
        
        if submitted:
            if title and org:
                add_event(title, edate, etime, loc, cat, org, desc)
                st.balloons()
                st.success("Event announced successfully!")
            else:
                st.error("Please fill in the Title and Organizer fields.")

# --- PAGE: MY BOOKMARKS ---
elif choice == "🔖 My Bookmarks":
    st.header("Your Saved Events")
    
    if not st.session_state.bookmarks:
        st.write("You haven't joined any events yet.")
    else:
        bookmarked_events = [e for e in st.session_state.events if e['id'] in st.session_state.bookmarks]
        for ev in bookmarked_events:
            st.markdown(f"- **{ev['title']}** on {ev['date']} at {ev['location']}")
        
        if st.button("Clear All Bookmarks"):
            st.session_state.bookmarks = []
            st.rerun()

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Campus Hub v1.0 | Agile Student Project")