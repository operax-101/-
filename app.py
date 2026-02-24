import streamlit as st
import pandas as pd
from datetime import datetime as dt
import requests

# 1. الإعدادات والواجهة (تغيير الألوان مثل جوجل)
st.set_page_config(page_title="منظم فراس", layout="wide")
st.sidebar.title("🎨 مظهر البرنامج")
clr = st.sidebar.color_picker("اختر لونك:", "#D4AF37")
bg = st.sidebar.selectbox("الخلفية:", ["#0e1117", "#000000", "#262730"])

st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:white; }}
    h1, h2 {{ color:{clr} !important; text-align:center; }}
    .stButton>button {{ background:linear-gradient(to right,{clr},#8B6B13); color:white; border:none; width:100%; }}
    .p-box {{ border:1px solid {clr}; padding:10px; border-radius:10px; text-align:center; background:rgba(255,255,255,0.05); }}
</style>""", unsafe_allow_html=True)

st.title("📅 FERAS SCHEDULER")
st.write(f"<p style='text-align:center;'>إبداع: فراس حمد المعمري</p>", unsafe_allow_html=True)

# 2. أوقات الصلاة (عالمي ونظام 12 ساعة)
city = st.text_input("المدينة (EN):", "Muscat")
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
        cols[i].markdown(f'<div class="p-box"><b style="color:{clr}">{v}</b><br>{time_12}</div>', unsafe_allow_html=True)

st.divider()

# 3. المهام
if 'tk' not in st.session_state: st.session_state.tk = []
with st.form("f"):
    n = st.text_input("المهمة")
    tm = st.time_input("الوقت")
    if st.form_submit_button("إضافة ✨"):
        if n:
            st.session_state.tk.append({"المهمة":n, "الوقت":tm.strftime("%I:%M %p")})
            st.rerun()

# 4. الجدول
if st.session_state.tk:
    st.table(pd.DataFrame(st.session_state.tk))
    if st.button("مسح"):
        st.session_state.tk = []
        st.rerun()

st.sidebar.write(f"المبرمج: فراس حمد المعمري")
