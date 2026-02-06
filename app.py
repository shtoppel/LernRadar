import streamlit as st
from datetime import date
from kalender import show_kalender
from search import show_search
from sidebar import show_sidebar
import os

# Create folder if not exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# 1. Options
st.set_page_config(page_title="LernRadar", layout="wide")

# 2. Const varriables
START_DATE = date(2025, 9, 15)
END_DATE = date(2027, 7, 30)

def get_progress_data(start_dt, end_dt):
    today = date.today()
    total = (end_dt - start_dt).days
    passed = (today - start_dt).days
    percent = max(0.0, min(1.0, passed / total))
    return percent, max(0, (end_dt - today).days), passed

# 3. state inizialisation
if "menu_choice" not in st.session_state:
    st.session_state.menu_choice = "📅 Kalender / Lernheft"

if "trigger_search" not in st.session_state:
    st.session_state.trigger_search = False

# Trigge's check
if st.session_state.trigger_search:
    st.session_state.menu_choice = "🔍 Suche"
    st.session_state.trigger_search = False # Сбрасываем, чтобы не зациклиться
# 4. Call the sidebar
show_sidebar()

# 5. Progress Tracker with calculations
st.title("📊 Progressbar Umschulung Fachinformatiker 2025-2027")
progress_pct, left, passed = get_progress_data(START_DATE, END_DATE)

st.progress(progress_pct)

col1, col2, col3 = st.columns(3)
col1.metric("Geschafft", f"{progress_pct * 100:.2f}%")
col2.metric("Tage noch", left)
col3.metric("Tage vorbei", passed)

st.divider()

# 6. Content
if st.session_state.menu_choice == "📅 Kalender / Lernheft":
    show_kalender()
elif st.session_state.menu_choice == "🔍 Suche":
    show_search(st.session_state.get("search_word", ""))
    st.session_state.search_word = ""
elif st.session_state.menu_choice == "📁 My Projects":
    st.info("Hier kommen meine Projekte hin...")