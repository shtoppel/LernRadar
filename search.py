import streamlit as st
from database import Session, Keyword, DiaryEntry


def show_search(query=None):
    session = Session()
    st.subheader("🔍 Suche nach Schlüsselwörter")

    # Если запрос не передан через функцию, берем из строки ввода
    search_query = st.text_input("Suche nach Schlüsselwörter", value=query if query else "").lower()

    if search_query:
        results = session.query(Keyword).filter(Keyword.word.contains(search_query)).all()

        if results:
            st.success(f"Gefunden: {len(results)}")
            for res in results:
                with st.expander(f"📅 {res.entry.date} — {res.entry.teacher}"):
                    st.write(res.entry.content)
                    st.caption(f"Keywords: {', '.join([k.word for k in res.entry.keywords])}")
        else:
            st.warning("No results.")
    session.close()