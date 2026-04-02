import streamlit as st
import pandas as pd
from datetime import datetime as dt
import requests

# 1. الإعدادات والواجهة
st.set_page_config(page_title="منظم فراس", layout="wide")

# إعدادات الشريط الجانبي
st.sidebar.title("🎨 مظهر البرنامج")
clr = st.sidebar.color_picker("اختر لون التميز (Accent):", "#D4AF37")
bg = st.sidebar.selectbox("اختر لون الخلفية:", ["#0e1117", "#000000", "#1a1c23"])

# تحسين الـ CSS لضمان الوضوح التام
st.markdown(f"""
<style>
    /* تلوين الخلفية والجسم */
    .stApp {{
        background-color: {bg};
    }}
    
    /* التأكد من أن كل النصوص باللون الأبيض الواضح */
    .stApp, p, span, label, .stMarkdown {{
        color: #FFFFFF !important;
        font-weight: 500;
    }}

    /* تحسين العناوين */
    h1, h2, h3 {{
        color: {clr} !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}

    /* تنسيق أزرار الإدخال والحقول */
    .stTextInput>div>div>input, .stTimeInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid {clr}33 !important;
    }}

    /* تنسيق الزر */
    .stButton>button {{
        background: linear-gradient(135deg, {clr}, #8B6B13);
        color: white !important;
        border: none;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        transform: scale(1.02);
        box-shadow: 0px 4px 15px {clr}66;
    }}

    /* صناديق أوقات الصلاة */
    .p-box {{
        border: 2px solid {clr};
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        background: rgba(255, 255, 255, 0.07);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
    
    /* تنسيق الجدول */
    .styled-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 18px;
        text-align: right;
    }}
</style>
""", unsafe_allow_html=True)

st.title("📅 FERAS SCHEDULER")
st.markdown(f"<h3 style='font-size: 20px; opacity: 0.8;'>إبداع: فراس حمد المعمري</h3>", unsafe_allow_html=True)

# 2. أوقات الصلاة
city = st.text_input("المدينة (مثال: Muscat):", "Muscat")

@st.cache_data(ttl=3600) # لتسريع التطبيق وعدم تكرار الطلب كل ثانية
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
                <b style="color:{clr}; font-size: 20px;">{v}</b><br>
                <span style="font-size: 18px; color: white;">{time_12}</span>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# 3. إضافة المهام
st.subheader("📝 إضافة مهمة جديدة")
if 'tk' not in st.session_state: 
    st.session_state.tk = []

with st.form("f", clear_on_submit=True):
    col_n, col_t = st.columns([3, 1])
    n = col_n.text_input("ماذا ستنجز اليوم؟")
    tm = col_t.time_input("الوقت")
    submit = st.form_submit_button("إضافة المهمة ✨")
    
    if submit and n:
        st.session_state.tk.append({"المهمة": n, "الوقت": tm.strftime("%I:%M %p")})
        st.rerun()

# 4. عرض الجدول بتنسيق أوضح
if st.session_state.tk:
    st.subheader("🕒 جدولك الحالي")
    # تحويل المهام لجدول وتعديل عرضه
    df = pd.DataFrame(st.session_state.tk)
    st.dataframe(df, use_container_width=True)
    
    if st.button("🗑️ مسح جميع المهام"):
        st.session_state.tk = []
        st.rerun()

st.sidebar.markdown(f"---")
st.sidebar.write(f"المبرمج: **فراس حمد المعمري**")
