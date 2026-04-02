import streamlit as st
import pandas as pd
from datetime import datetime as dt
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظم فراس", layout="wide")

# 2. الشريط الجانبي (المظهر)
st.sidebar.title("🎨 مظهر البرنامج")
clr = st.sidebar.color_picker("اختر لون التميز (Accent):", "#D4AF37")

# قائمة خلفيات موسعة
bg_options = {
    "أسود ملكي": "#000000",
    "أزرق ليلي": "#0e1117",
    "رمادي كربوني": "#262730",
    "بنفسجي غامق": "#120d1c",
    "رمادي فضائي": "#343a40"
}
bg_label = st.sidebar.selectbox("اختر لون الخلفية:", list(bg_options.keys()))
bg = bg_options[bg_label]

# نظام التنسيق المطور (CSS) لضمان الوضوح التام
st.markdown(f"""
<style>
    /* الخلفية الأساسية مع تدرج انسيابي */
    .stApp {{
        background: linear-gradient(180deg, {bg} 0%, #000000 100%) !important;
        background-attachment: fixed;
    }}
    
    /* إجبار نصوص السايدبار على الظهور بوضوح 100% */
    [data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(10px);
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }}

    /* العناوين الرئيسية */
    h1, h2, h3 {{
        color: {clr} !important;
        text-align: center;
        font-weight: 800 !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }}

    /* نصوص البرنامج العامة */
    p, span, label, .stMarkdown {{
        color: white !important;
        font-weight: 500 !important;
    }}

    /* صناديق الصلاة الاحترافية */
    .p-box {{
        border: 2px solid {clr};
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        transition: 0.3s;
    }}
    .p-box:hover {{
        transform: translateY(-5px);
        border-color: white;
    }}

    /* زر الإضافة - نص أسود عريض للوضوح */
    .stButton>button {{
        background-color: {clr} !important;
        color: black !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        width: 100% !important;
        padding: 10px !important;
        box-shadow: 0px 4px 15px {clr}44 !important;
    }}
    .stButton>button:hover {{
        background-color: white !important;
        color: black !important;
    }}

    /* تنسيق الجداول وحقول الإدخال */
    input {{
        color: white !important;
        background-color: rgba(255,255,255,0.1) !important;
    }}
</style>
""", unsafe_allow_html=True)

# 3. واجهة البرنامج الرئيسية
st.title("📅 FERAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.2rem; opacity:0.9;'>إبداع المبرمج: فراس حمد المعمري</p>", unsafe_allow_html=True)

# 4. جلب أوقات الصلاة
city = st.text_input("📍 المدينة (مثال: Muscat):", "Muscat")

@st.cache_data(ttl=3600)
def get_p(c):
    try:
        r = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={c}&country=Oman&method=4").json()
        return r['data']['timings']
    except:
        return None

t = get_p(city)
if t:
    cols = st.columns(5)
    p_names = {"Fajr":"الفجر","Dhuhr":"الظهر","Asr":"العصر","Maghrib":"المغرب","Isha":"العشاء"}
    for i, (k, v) in enumerate(p_names.items()):
        time_12 = dt.strptime(t[k], "%H:%M").strftime("%I:%M %p")
        cols[i].markdown(f"""
            <div class="p-box">
                <b style="color:{clr}; font-size: 1.2rem;">{v}</b><br>
                <span style="font-size: 1.1rem;">{time_12}</span>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# 5. إدارة المهام
st.subheader("📝 إضافة مهمة جديدة")
if 'tk' not in st.session_state: 
    st.session_state.tk = []

with st.form("task_form", clear_on_submit=True):
    c1, c2 = st.columns([3, 1])
    n = c1.text_input("ما هي المهمة القادمة؟")
    tm = c2.time_input("الوقت")
    if st.form_submit_button("إضافة المهمة ✨"):
        if n:
            st.session_state.tk.append({"المهمة": n, "الوقت": tm.strftime("%I:%M %p")})
            st.rerun()

# 6. عرض الجدول
if st.session_state.tk:
    st.subheader("🕒 جدول مهامك")
    df = pd.DataFrame(st.session_state.tk)
    st.table(df) # أو استخدم st.dataframe(df, use_container_width=True)
    
    if st.button("🗑️ مسح كل المهام"):
        st.session_state.tk = []
        st.rerun()

# التوقيع في السايدبار
st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **فراس حمد المعمري**")
