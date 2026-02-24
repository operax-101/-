import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظم فراس المعمري", layout="wide")

# --- التصميم الأسطوري (ذهبي وأسود) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { color: #D4AF37 !important; text-align: center; font-family: 'Cairo', sans-serif; }
    .stButton>button { background: linear-gradient(to right, #D4AF37, #8B6B13); color: white !important; border-radius: 8px; border: none; }
    .prayer-box { background: rgba(212, 175, 55, 0.1); padding: 15px; border-radius: 12px; border: 1px solid #D4AF37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 منظم الجدول الذكي - فراس حمد المعمري")

# --- الجزء الأول: تحديد الموقع وتواقيت الصلاة ---
st.subheader("🕌 تواقيت الصلاة الدقيقة")

# قائمة الولايات لضبط التوقيت 100%
location_options = {
    "مسقط": {"city": "Muscat", "country": "Oman"},
    "صحار": {"city": "Sohar", "country": "Oman"},
    "صلالة": {"city": "Salalah", "country": "Oman"},
    "نزوى": {"city": "Nizwa", "country": "Oman"},
    "البريمي": {"city": "Buraimi", "country": "Oman"},
    "عبري": {"city": "Ibri", "country": "Oman"}
}

selected_loc = st.selectbox("📍 حدد موقعك لضبط التوقيت بدقة:", list(location_options.keys()))

def get_prayer_times(city, country):
    # استخدام method=4 (رابطة العالم الإسلامي) أو 1 (أم القرى) لضبط الدقة
    url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=4"
    try:
        response = requests.get(url).json()
        return response['data']['timings']
    except:
        return None

timings = get_prayer_times(location_options[selected_loc]["city"], location_options[selected_loc]["country"])

if timings:
    cols = st.columns(5)
    prayers = {"Fajr": "الفجر", "Dhuhr": "الظهر", "Asr": "العصر", "Maghrib": "المغرب", "Isha": "العشاء"}
    for i, (key, val) in enumerate(prayers.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="prayer-box">
                    <p style="color: #D4AF37; margin: 0; font-weight: bold;">{val}</p>
                    <h2 style="margin: 5px 0;">{timings[key]}</h2>
                </div>
            """, unsafe_allow_html=True)

st.divider()

# --- الجزء الثاني: إضافة المهام (بدون تغيير في المنطق) ---
st.subheader("📝 جدول المهام اليومية")

with st.form("task_form"):
    task_name = st.text_input("اسم المهمة")
    task_time = st.time_input("وقت البدء")
    priority = st.selectbox("الأهمية", ["عالية 🔥", "متوسطة ⚡", "منخفضة ❄️"])
    submit = st.form_submit_button("إضافة المهمة ✨")

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if submit and task_name:
    st.session_state.tasks.append({
        "المهمة": task_name,
        "الوقت": task_time.strftime("%I:%M %p"),
        "الأهمية": priority
    })
    st.success(f"تمت إضافة المهمة في جدول {selected_loc}!")

# --- الجزء الثالث: عرض الجدول ---
if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    st.table(df)
    if st.button("تفريغ الجدول"):
        st.session_state.tasks = []
        st.rerun()
else:
    st.info("الجدول فارغ حالياً يا فراس.")

# الجانب
st.sidebar.markdown(f"### المبرمج:\n**فراس حمد المعمري**")
st.sidebar.info("هذا النظام يضبط التواقيت حسب الموقع المختار لضمان دقة 100%.")
