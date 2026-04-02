import streamlit as st
import pandas as pd
from datetime import datetime as dt
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظم فراس - احترافي", layout="wide")

# 2. تعريف التدرجات اللونية القوية والواضحة
gradients = {
    "تدرج المحيط (Deep Ocean)": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
    "تدرج الغسق (Sunset Dusk)": "linear-gradient(135deg, #2c3e50 0%, #000000 100%)",
    "تدرج ملكي (Royal Gold)": "linear-gradient(135deg, #1a1a1a 0%, #434343 100%)",
    "تدرج الأرجواني (Midnight)": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
    "تدرج احترافي (Modern Grey)": "linear-gradient(135deg, #141e30 0%, #243b55 100%)"
}

# 3. الشريط الجانبي لتعديل المظهر
st.sidebar.title("🎨 لوحة التحكم")
clr = st.sidebar.color_picker("اختر لون الأزرار (Accent):", "#D4AF37")
bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
selected_gradient = gradients[bg_key]

# 4. الـ CSS السحري للوضوح التام والتدرج الواضح
st.markdown(f"""
<style>
    /* تطبيق التدرج الواضح على كامل الصفحة */
    .stApp {{
        background: {selected_gradient} !important;
        background-attachment: fixed !important;
    }}

    /* إجبار نصوص السايدبار على الوضوح الكامل */
    [data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.5) !important;
        border-right: 1px solid {clr}44;
    }}
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }}

    /* تحسين العناوين */
    h1, h2, h3 {{
        color: {clr} !important;
        text-align: center;
        text-shadow: 2px 2px 15px rgba(0,0,0,0.6);
        font-weight: 800 !important;
    }}

    /* نصوص البرنامج الأساسية */
    p, span, label, .stMarkdown {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}

    /* صناديق الصلاة الزجاجية */
    .p-box {{
        border: 2px solid {clr};
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: 0.3s ease;
        margin-bottom: 10px;
    }}
    .p-box:hover {{
        transform: translateY(-8px);
        border-color: #FFFFFF;
        box-shadow: 0 15px 35px {clr}33;
    }}

    /* زر الإضافة - تباين عالي جداً */
    .stButton>button {{
        background: {clr} !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        height: 50px !important;
        width: 100% !important;
        box-shadow: 0px 5px 20px {clr}55 !important;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: #FFFFFF !important;
        transform: scale(1.02);
    }}

    /* تنسيق الجداول */
    .stTable, table {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border-radius: 15px !important;
    }}
</style>
""", unsafe_allow_html=True)

# 5. محتوى الواجهة
st.title("📅 FERAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.4rem; color:{clr}; font-weight:bold;'>إبداع: فراس حمد المعمري</p>", unsafe_allow_html=True)

# 6. قسم أوقات الصلاة
city = st.text_input("📍 المدينة بالإنجليزية (مثال: Muscat):", "Muscat")

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
        cols[i].markdown(f"""
            <div class="p-box">
                <div style="color:{clr}; font-size: 1.4rem; font-weight:bold;">{v}</div>
                <div style="font-size: 1.2rem; color: white; margin-top:5px;">{time_12}</div>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# 7. قسم المهام
st.subheader("📝 جدولك اليومي")
if 'tk' not in st.session_state: st.session_state.tk = []

with st.form("main_form", clear_on_submit=True):
    c1, c2 = st.columns([3, 1])
    n = c1.text_input("ما هي مهمتك القادمة؟")
    tm = c2.time_input("اختر الوقت")
    if st.form_submit_button("إضافة المهمة الآن ✨"):
        if n:
            st.session_state.tk.append({"المهمة": n, "الوقت": tm.strftime("%I:%M %p")})
            st.rerun()

# 8. عرض المهام
if st.session_state.tk:
    df = pd.DataFrame(st.session_state.tk)
    st.dataframe(df, use_container_width=True)
    
    if st.button("🗑️ مسح الجدول"):
        st.session_state.tk = []
        st.rerun()

# الشريط الجانبي - التوقيع
st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **فراس حمد المعمري**")
