import streamlit as st
from database import Session, Keyword, DiaryEntry


def navigate_to_entry(target_date):
    st.session_state.selected_date = target_date
    st.session_state.menu_choice = "📅 Kalender / Lernheft"

def show_search(query=None):
    session = Session()
    st.subheader("🔍 Suche")

    # If the request is not passed through a function, we take it from the input line
    search_query = st.text_input("Suche", value=query if query else "").lower()

    if search_query:
        results = session.query(Keyword).filter(Keyword.word.contains(search_query)).all()

        if results:
            st.success(f"Gefunden: {len(results)}")
            for res in results:
                with st.expander(f"📅 {res.entry.date} — {res.entry.teacher}"):
                    st.write(res.entry.content)
                    st.caption(f"Keywords: {', '.join([k.word for k in res.entry.keywords])}")
                    st.button(
                        "Fullview / Edit ↗",
                        key=f"go_{res.entry.id}",
                        on_click=navigate_to_entry,
                        args=(res.entry.date,)
                    )
        else:
            st.warning("No results.")
    session.close()