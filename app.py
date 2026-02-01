import streamlit as st
from datetime import date
import pandas as pd
from kalender import show_kalender

# Настройки страницы
st.set_page_config(page_title="LernRadar - Progress", layout="wide")


# --- ЛОГИКА ПРОГРЕССА ---
def get_study_progress(start_dt, end_dt):
    today = date.today()
    total_days = (end_dt - start_dt).days
    passed_days = (today - start_dt).days

    percent = (passed_days / total_days) if total_days > 0 else 0
    percent = max(0.0, min(1.0, percent))  # Ограничение от 0 до 1
    days_left = max(0, (end_dt - today).days)

    return percent, days_left, passed_days


# --- ДАННЫЕ (Позже вынесем в конфиг/БД) ---
START_DATE = date(2025, 9, 15)  # Пример: начало
END_DATE = date(2027, 7, 31)  # Пример: конец

# --- ИНТЕРФЕЙС ---
st.title("📊 Progressbar Umschulung FIAE/FISI 2025-2027")

progress_pct, left, passed = get_study_progress(START_DATE, END_DATE)

# Визуальный прогресс-бар
st.progress(progress_pct)

# Метрики сверху
col1, col2, col3 = st.columns(3)
col1.metric("Geschafft", f"{progress_pct * 100:.2f}%%")
col2.metric("Tage noch", left)
col3.metric("Tage vorbei", passed)

st.divider()

# Сайдбар (Дерево меню)
st.sidebar.title("🌿 Navi")
st.sidebar.tree_select = st.sidebar.radio(
    "Optionen:",
    ["📅 Kalender / Lernheft", "🔍 Suche", "📁 My Projects", "⚙️ Einstellungen"]
)

# Заглушка для центральной части
if "Kalender" in st.sidebar.tree_select:
    show_kalender() # Просто вызываем функцию из другого файла
elif "Search" in st.sidebar.tree_select:
    # Здесь можно будет вызвать show_search() из search.py
    st.write("Suchmaschiene")