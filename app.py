import streamlit as st
import pandas as pd
from datetime import datetime as dt
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظم فراس - النسخة النهائية", layout="wide")

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

# 4. الـ CSS (تم إصلاح الزر هنا)
st.markdown(f"""
<style>
    /* الخلفية المتدرجة */
    .stApp {{
        background: {selected_gradient} !important;
        background-attachment: fixed !important;
    }}

    /* نصوص السايدبار */
    [data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.5) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }}

    /* العناوين */
    h1, h2, h3 {{
        color: {clr} !important;
        text-align: center;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.7);
    }}

    /* صناديق الصلاة */
    .p-box {{
        border: 2px solid {clr};
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }}

    /* --- إصلاح زر إضافة مهمة --- */
    .stButton>button {{
        background-color: {clr} !important; /* اللون ظاهر دائماً وليس فقط عند التأشير */
        color: #000000 !important; /* النص أسود وعريض ليكون واضحاً جداً */
        border: 2px solid white !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        height: 55px !important;
        width: 100% !important;
        display: block !important;
        box-shadow: 0px 0px 15px {clr}88 !important; /* توهج خفيف ليبرز الزر */
        margin-top: 10px;
        transition: all 0.3s ease-in-out;
    }}

    /* تأثير عند وضع الماوس (اختياري للجمالية) */
    .stButton>button:hover {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        transform: scale(1.02);
        box-shadow: 0px 0px 25px #FFFFFF88 !important;
    }}

    /* تحسين حقول الإدخال */
    .stTextInput input {{
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid {clr}55 !important;
        height: 45px;
    }}
</style>
""", unsafe_allow_html=True)

# 5. الواجهة
st.title("📅 FERAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.4rem; color:{clr}; font-weight:bold;'>إبداع: فراس حمد المعمري</p>", unsafe_allow_html=True)

# 6. أوقات الصلاة
city = st.text_input("📍 المدينة (Muscat):", "Muscat")

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

with st.container():
    st.subheader("📝 أضف مهمة جديدة")
    with st.form("task_form", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        n = c1.text_input("ما هي المهمة؟")
        tm = c2.time_input("الوقت")
        submit = st.form_submit_button("إضافة المهمة الآن ✨")
        if submit and n:
            st.session_state.tk.append({"المهمة": n, "الوقت": tm.strftime("%I:%M %p")})
            st.rerun()

# 8. الجدول
if st.session_state.tk:
    st.subheader("🕒 جدولك الحالي")
    df = pd.DataFrame(st.session_state.tk)
    st.table(df)
    if st.button("🗑️ مسح الكل"):
        st.session_state.tk = []
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **فراس حمد المعمري**")
