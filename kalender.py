import streamlit as st
from datetime import date
from database import Session, DiaryEntry, Keyword


def show_kalender():
    session = Session()
    st.subheader("📅 Lernheft")

    selected_date = st.date_input("Datum auswählen", date.today())

    # Пытаемся найти существующую запись
    entry = session.query(DiaryEntry).filter(DiaryEntry.date == selected_date).first()

    col_input, col_view = st.columns(2)

    with col_input:
        teacher = st.text_input("Lehrer", value=entry.teacher if entry else "")
        content = st.text_area("Themen heute?", value=entry.content if entry else "")
        keywords_str = st.text_input("Schlüsselwörter (mit Klammern getrennt)",
                                     value=", ".join([k.word for k in entry.keywords]) if entry else "")

        if st.button("Speichern"):
            if not entry:
                entry = DiaryEntry(date=selected_date)
                session.add(entry)

            entry.teacher = teacher
            entry.content = content

            # Обновляем теги (простая логика)
            session.query(Keyword).filter(Keyword.entry_id == entry.id).delete()
            for word in keywords_str.split(","):
                if word.strip():
                    session.add(Keyword(word=word.strip().lower(), entry=entry))

            session.commit()
            st.success("Daten sind gespeichert!")

    with col_view:
        st.write("### Vorschau")
        if entry:
            st.markdown(f"**Lehrer:** {entry.teacher}")
            st.write(f"**Notizen:** {entry.content}")
            # Красиво выводим теги кнопками (просто для визуала)
            if entry.keywords:
                st.write("Tags:")
                cols = st.columns(len(entry.keywords))
                for i, kw in enumerate(entry.keywords):
                    cols[i].button(kw.word, key=f"kw_{kw.id}")
        else:
            st.info("Es gibt keine Daten an diesem Tag.")

    session.close()  # Важно закрывать сессию