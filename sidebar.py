import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.title("🌿 Navi")
        st.radio(
            "Optionen:",
            ["📅 Kalender / Lernheft", "🔍 Suche", "📁 My Projects"],
            key="menu_choice"
        )
        st.divider()
        # this block is still in development
        st.caption("Umschulung Tracker v1.1")