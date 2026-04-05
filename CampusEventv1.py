import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Campus Event Hub", page_icon="🎓", layout="wide")

# Improved CSS for visibility and contrast
st.markdown("""
    <style>
    /* Main background color */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Event Card Styling */
    .event-card { 
        padding: 25px; 
        border-radius: 12px; 
        border-left: 5px solid #007bff;
        background-color: #ffffff;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #1f2937; /* Dark gray for text */
    }
    
    /* Heading inside card */
    .event-card h3 {
        color: #111827 !important;
        margin-top: 0px;
        font-weight: 700;
    }
    
    /* Text details inside card */
    .event-card p {
        color: #374151 !important;
        margin-bottom: 8px;
        line-height: 1.5;
    }
    
    /* Category Tag */
    .category-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75em;
        font-weight: 600;
        background-color: #e5e7eb;
        color: #374151;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Join Button Styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        background-color: #007bff;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
    }

    /* Fix for Search bar visibility */
    .stTextInput input {
        color: #111827;
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
st.markdown("Discover and join events happening around your campus.")

# Navigation Sidebar
menu = ["📡 Event Feed", "🗓️ Calendar View", "➕ Announce Event", "🔖 My Bookmarks"]
choice = st.sidebar.radio("Navigation", menu)

# --- PAGE: EVENT FEED ---
if choice == "📡 Event Feed":
    st.header("Upcoming Activities")
    
    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search events by name...", "")
    with col2:
        cat_filter = st.selectbox("Category Filter", ["All", "Workshop", "Social", "Sports", "Academic"])

    st.markdown("---")

    for ev in st.session_state.events:
        # Apply filters
        if search.lower() in ev['title'].lower() and (cat_filter == "All" or ev['category'] == cat_filter):
            with st.container():
                # Card HTML
                st.markdown(f"""
                <div class="event-card">
                    <span class="category-tag">{ev['category']}</span>
                    <h3>{ev['title']}</h3>
                    <p>📅 <b>Date:</b> {ev['date'].strftime('%B %d, %Y')} &nbsp;&nbsp; | &nbsp;&nbsp; ⏰ <b>Time:</b> {ev['time']}</p>
                    <p>📍 <b>Location:</b> {ev['location']}</p>
                    <p>👤 <b>Organizer:</b> {ev['organizer']}</p>
                    <p style="margin-top:10px; font-style: italic;">{ev['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Action Buttons
                c1, c2 = st.columns([1, 5])
                with c1:
                    is_bookmarked = ev['id'] in st.session_state.bookmarks
                    btn_label = "Saved ✅" if is_bookmarked else "Join / Save"
                    if st.button(btn_label, key=f"btn_{ev['id']}"):
                        if not is_bookmarked:
                            st.session_state.bookmarks.append(ev['id'])
                            st.rerun()
                        else:
                            st.toast("Already in your bookmarks!")

# --- PAGE: CALENDAR VIEW ---
elif choice == "🗓️ Calendar View":
    st.header("Event Schedule")
    
    if st.session_state.events:
        df = pd.DataFrame(st.session_state.events)
        df['date'] = pd.to_datetime(df['date'])
        
        st.write("Chronological list of upcoming campus activities:")
        st.dataframe(
            df[['date', 'title', 'location', 'category', 'organizer']].sort_values('date'), 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No events scheduled yet.")

# --- PAGE: ANNOUNCE EVENT ---
elif choice == "➕ Announce Event":
    st.header("Post a New Event")
    st.write("Fill out the details below to share your event with the campus.")
    
    with st.form("event_form", clear_on_submit=True):
        title = st.text_input("Event Title*")
        col1, col2 = st.columns(2)
        with col1:
            edate = st.date_input("Date", min_value=date.today())
        with col2:
            etime = st.time_input("Time")
        
        loc = st.text_input("Location (Building/Room)")
        cat = st.selectbox("Category", ["Workshop", "Social", "Sports", "Academic"])
        org = st.text_input("Club/Organizer Name*")
        desc = st.text_area("Event Description")
        
        submitted = st.form_submit_button("Post to Hub 🚀")
        
        if submitted:
            if title and org:
                add_event(title, edate, etime, loc, cat, org, desc)
                st.success(f"Successfully posted '{title}'!")
                st.balloons()
            else:
                st.error("Please provide both an Event Title and an Organizer name.")

# --- PAGE: MY BOOKMARKS ---
elif choice == "🔖 My Bookmarks":
    st.header("Your Saved Events")
    
    if not st.session_state.bookmarks:
        st.info("You haven't bookmarked any events yet. Head back to the Feed to find some!")
    else:
        bookmarked_events = [e for e in st.session_state.events if e['id'] in st.session_state.bookmarks]
        for ev in bookmarked_events:
            with st.expander(f"📌 {ev['title']} - {ev['date']}"):
                st.write(f"**Time:** {ev['time']}")
                st.write(f"**Location:** {ev['location']}")
                st.write(f"**Category:** {ev['category']}")
                st.write(f"**Description:** {ev['description']}")
        
        if st.button("Clear All Bookmarks"):
            st.session_state.bookmarks = []
            st.rerun()

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Campus Hub v1.1 | Visual Accessibility Update")
