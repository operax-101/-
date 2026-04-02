import streamlit as st
import pandas as pd
from datetime import datetime as dt
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظم فراس الذكي", layout="wide")

# 2. قائمة التدرجات اللونية (Gradients)
gradients = {
    "ليل مسقط (Dark Blue)": "linear-gradient(180deg, #0f2027, #203a43, #2c5364)",
    "الفجر الذهبي (Golden)": "linear-gradient(180deg, #131112, #2c2512, #4e4321)",
    "الغروب الأرجواني (Deep Purple)": "linear-gradient(180deg, #0f0c29, #302b63, #24243e)",
    "غابة ليلية (Dark Green)": "linear-gradient(180deg, #000000, #09203f, #1e4b52)",
    "رمادي ملكي (Silver/Black)": "linear-gradient(180deg, #232526, #414345)",
    "أزرق كهربائي (Electric)": "linear-gradient(180deg, #000428, #004e92)",
    "احترافي (Carbon)": "linear-gradient(180deg, #141e30, #243b55)",
    "أسود مطلق (Solid Black)": "linear-gradient(180deg, #000000, #111111)"
}

# 3. الشريط الجانبي
st.sidebar.title("🎨 لوحة التحكم بالمظهر")
clr = st.sidebar.color_picker("اختر لون الأزرار والحدود (Accent):", "#D4AF37")
bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
selected_gradient = gradients[bg_key]

# 4. نظام الـ CSS المتكامل (الحل النهائي للوضوح)
st.markdown(f"""
<style>
    /* تطبيق التدرج على كامل التطبيق */
    .stApp {{
        background: {selected_gradient} !important;
        background-attachment: fixed !important;
    }}

    /* إجبار كل نصوص السايدبار على اللون الأبيض الصريح */
    [data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.4) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }}

    /* العناوين بلمسة احترافية */
    h1, h2, h3 {{
        color: {clr} !important;
        text-align: center;
        font-weight: 800 !important;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.7);
    }}

    /* نصوص البرنامج */
    p, span, label, .stMarkdown {{
        color: white !important;
        font-weight: 600 !important;
    }}

    /* صناديق الصلاة - تصميم زجاجي (Glassmorphism) */
    .p-box {{
        border: 2px solid {clr};
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        background: rgba(0, 0, 0, 0.4); 
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        transition: 0.4s ease;
    }}
    .p-box:hover {{
        transform: scale(1.05);
        border-color: white;
        background: rgba(255, 255, 255, 0.1);
    }}

    /* الزر - تباين عالي جداً (نص أسود عريض) */
    .stButton>button {{
        background-color: {clr} !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        height: 50px !important;
        width: 100% !important;
        box-shadow: 0px 5px 15px {clr}66 !important;
    }}
    .stButton>button:hover {{
        background-color: white !important;
        transform: translateY(-3px);
    }}

    /* تحسين شكل حقول الإدخال */
    .stTextInput input, .stTimeInput input {{
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid {clr}55 !important;
    }}
</style>
""", unsafe_allow_html=True)

# 5. محتوى البرنامج
st.title("📅 FERAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.3rem; color:{clr};'>إبداع: فراس حمد المعمري</p>", unsafe_allow_html=True)

# 6. أوقات الصلاة
city = st.text_input("📍 اكتب مدينتك بالإنجليزية (مثال: Muscat):", "Muscat")

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
                <div style="color:{clr}; font-size: 1.4rem; font-weight:bold; margin-bottom:5px;">{v}</div>
                <div style="font-size: 1.2rem; color: white;">{time_12}</div>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# 7. إضافة المهام
st.subheader("📝 أضف مهمة لجدولك")
if 'tk' not in st.session_state: st.session_state.tk = []

with st.form("task_form", clear_on_submit=True):
    col_input, col_time = st.columns([3, 1])
    n = col_input.text_input("ما هي المهمة؟")
    tm = col_time.time_input("الوقت")
    if st.form_submit_button("إضافة المهمة الآن ✨"):
        if n:
            st.session_state.tk.append({"المهمة": n, "الوقت": tm.strftime("%I:%M %p")})
            st.rerun()

# 8. عرض المهام بتنسيق نظيف
if st.session_state.tk:
    st.subheader("🕒 جدولك لليوم")
    df = pd.DataFrame(st.session_state.tk)
    st.table(df)
    
    if st.button("🗑️ مسح الجدول"):
        st.session_state.tk = []
        st.rerun()

# التذييل
st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **فراس حمد المعمري**")
