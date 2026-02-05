import streamlit as st
from datetime import date
from database import Session, DiaryEntry, Keyword, EntryImage
from file_manager import  show_image_gallery, save_uploaded_files, delete_file


def show_kalender():
    session = Session()
    st.subheader("📅 Lernheft")

    selected_date = st.date_input("Datum auswählen", date.today())
    entry = session.query(DiaryEntry).filter(DiaryEntry.date == selected_date).first()

    col_input, col_view = st.columns(2)

    with col_input:
        teacher = st.text_input("Lehrer", value=entry.teacher if entry else "")
        content = st.text_area("Themen heute?", value=entry.content if entry else "")
        keywords_str = st.text_input("Schlüsselwörter (mit Komma getrennt)",
                                     value=", ".join([k.word for k in entry.keywords]) if entry else "")

        uploaded_files = st.file_uploader("Fotos hinzufügen", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

        if st.button("Speichern"):
            if not entry:
                entry = DiaryEntry(date=selected_date)
                session.add(entry)
                session.flush()

            entry.teacher = teacher
            entry.content = content

            # file processing with filemanager.py
            if uploaded_files:
                paths = save_uploaded_files(uploaded_files, selected_date)
                for p in paths:
                    session.add(EntryImage(path=p, entry=entry))

            # Keywords update
            session.query(Keyword).filter(Keyword.entry_id == entry.id).delete()
            for word in keywords_str.split(","):
                if word.strip():
                    session.add(Keyword(word=word.strip().lower(), entry=entry))

            session.commit()
            st.success("Gespeichert!")
            st.rerun()

    with col_view:
        if entry:
            st.write(f"### Vorschau für {selected_date}")
            selected_img = show_image_gallery(entry.images)

            if selected_img:
                # deletes the selected file
                if st.button("🗑 Löschen", key="del_btn"):
                    if delete_file(selected_img.path):
                        session.delete(selected_img)
                        session.commit()
                        st.rerun()

            # Keywords
            if entry.keywords:
                st.write("Keywords:")
                cols = st.columns(len(entry.keywords))
                for i, kw in enumerate(entry.keywords):
                    if cols[i].button(kw.word, key=f"kw_{kw.id}"):
                        st.session_state.search_word = kw.word
                        st.session_state.trigger_search = True
                        st.rerun()
        else:
            st.info("Keine Notizen vorhanden.")

    session.close()