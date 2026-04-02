import streamlit as st
import pandas as pd
from datetime import datetime as dt
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظم فراس - النسخة المثالية", layout="wide")

# 2. قائمة التدرجات
gradients = {
    "تدرج المحيط (Deep Ocean)": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
    "تدرج الغسق (Sunset Dusk)": "linear-gradient(135deg, #2c3e50 0%, #000000 100%)",
    "تدرج ملكي (Royal Gold)": "linear-gradient(135deg, #1a1a1a 0%, #434343 100%)",
    "تدرج الأرجواني (Midnight)": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
    "تدرج احترافي (Modern Grey)": "linear-gradient(135deg, #141e30 0%, #243b55 100%)"
}

# 3. السايدبار
st.sidebar.title("🎨 لوحة التحكم")
clr = st.sidebar.color_picker("اختر لون التميز (Accent Color):", "#D4AF37")
bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
selected_gradient = gradients[bg_key]

# 4. الـ CSS (تمت إضافة تنسيق الجدول الواضح)
st.markdown(f"""
<style>
    .stApp {{
        background: {selected_gradient} !important;
        background-attachment: fixed !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.5) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }}

    h1, h2, h3 {{
        color: {clr} !important;
        text-align: center;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.7);
    }}

    input {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid {clr} !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }}

    label {{
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }}

    .p-box {{
        border: 2px solid {clr};
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
    }}

    .stButton>button {{
        background-color: {clr} !important;
        color: #000000 !important;
        border: 2px solid white !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        height: 55px !important;
        width: 100% !important;
        box-shadow: 0px 0px 15px {clr}88 !important;
    }}

    /* --- تنسيق الجدول الجديد (واضح جداً) --- */
    .task-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 1.1rem;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid {clr};
    }}
    .task-table th {{
        background-color: {clr};
        color: black;
        padding: 12px;
        text-align: center;
    }}
    .task-table td {{
        padding: 12px;
        text-align: center;
        color: white;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    .task-table tr:hover {{
        background-color: rgba(255,255,255,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# 5. الواجهة
st.title("📅 FERAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.4rem; color:{clr}; font-weight:bold;'>إبداع: فراس حمد المعمري</p>", unsafe_allow_html=True)

# 6. أوقات الصلاة
city = st.text_input("📍 اكتب المدينة هنا (مثلاً: Muscat):", "Muscat")

@st.cache_data(ttl=3600)
def get_p(c):
    try:
        r = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={c}&country=Oman&method=4").json()
        return r['data']['timings']
    except: return None

t = get_p(city)
if t:
    cols = st.columns(5)
    p_names = {"Fajr":"الفجر","Dhuhr":"الظهر","Asr":"العصر","Maghrib":"المغرب","Isha":"العشاء"}
    for i, (k, v) in enumerate(p_names.items()):
        time_12 = dt.strptime(t[k], "%H:%M").strftime("%I:%M %p")
        cols[i].markdown(f'<div class="p-box"><b style="color:{clr}; font-size:1.3rem;">{v}</b><br><span style="color:white;">{time_12}</span></div>', unsafe_allow_html=True)

st.divider()

# 7. قسم المهام
if 'tk' not in st.session_state: st.session_state.tk = []

st.subheader("📝 أضف مهمة جديدة")
with st.form("task_form", clear_on_submit=True):
    c1, c2 = st.columns([3, 1])
    n = c1.text_input("ما هي المهمة التي تريد إنجازها؟")
    tm = c2.time_input("الوقت")
    submit = st.form_submit_button("إضافة المهمة الآن ✨")
    if submit and n:
        st.session_state.tk.append({"المهمة": n, "الوقت": tm.strftime("%I:%M %p")})
        st.rerun()

# 8. عرض الجدول (باستخدام التنسيق المخصص الجديد)
if st.session_state.tk:
    st.subheader("🕒 جدولك الحالي")
    
    # بناء الجدول يدوياً باستخدام HTML لضمان أفضل وضوح
    table_html = '<table class="task-table"><thead><tr><th>المهمة</th><th>الوقت</th></tr></thead><tbody>'
    for task in st.session_state.tk:
        table_html += f'<tr><td>{task["المهمة"]}</td><td>{task["الوقت"]}</td></tr>'
    table_html += '</tbody></table>'
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    if st.button("🗑️ مسح الكل"):
        st.session_state.tk = []
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **فراس حمد المعمري**")
