import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات
st.set_page_config(page_title="منظم فراس", layout="wide")

# 2. تصميم (أسطر قصيرة)
st.markdown("<style>h1{color:#D4AF37;text-align:center;}</style>", unsafe_allow_html=True)

st.title("📅 FERAS SCHEDULER")
st.write("المبرمج: فراس حمد المعمري")

# 3. جلب التوقيت (إحداثيات مسقط لضمان الدقة)
def get_t():
    u = "http://api.aladhan.com/v1/timings?latitude=23.58&longitude=58.40&method=1"
    try:
        r = requests.get(u).json()
        return r['data']['timings']
    except: return None

t = get_t()

if t:
    st.subheader("🕌 مواقيت الصلاة (عمان)")
    # عرض بسيط ومباشر لتجنب أخطاء الأعمدة
    p = {"Fajr":"الفجر", "Dhuhr":"الظهر", "Asr":"العصر", "Maghrib":"المغرب", "Isha":"العشاء"}
    for k, v in p.items():
        tm = datetime.strptime(t[k], "%H:%M").strftime("%I:%M %p")
        st.write(f"**{v}:** {tm}")

st.divider()

# 4. المهام
if 'list' not in st.session_state: st.session_state.list = []

job = st.text_input("المهمة")
tm_in = st.time_input("الوقت")

if st.button("إضافة"):
    if job:
        st.session_state.list.append({"المهمة": job, "الوقت": tm_in.strftime("%I:%M %p")})
        st.rerun()

# 5. الجدول
if st.session_state.list:
    st.table(pd.DataFrame(st.session_state.list))
    if st.button("تفريغ"):
        st.session_state.list = []
        st.rerun()

# 6. التوقيع
st.sidebar.write("فراس حمد المعمري")
