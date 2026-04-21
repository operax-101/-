import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
import requests
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="FIRAS SCHEDULER", layout="wide", page_icon="📅")

# 2. قائمة التدرجات
gradients = {
    "تدرج ملكي (Royal Gold)": "linear-gradient(135deg, #1a1a1a 0%, #434343 100%)",
    "تدرج المحيط (Deep Ocean)": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
    "تدرج الغسق (Sunset Dusk)": "linear-gradient(135deg, #2c3e50 0%, #000000 100%)",
    "تدرج الأرجواني (Midnight)": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
}

# 3. السايدبار
st.sidebar.title("🎨 لوحة التحكم")
clr = st.sidebar.color_picker("اختر لون التميز (Accent Color):", "#D4AF37")
bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
selected_gradient = gradients[bg_key]

st.sidebar.divider()
st.sidebar.subheader("⏱️ إعدادات الإقامة")
iqama_offset = st.sidebar.slider("دقائق الانتظار للإقامة:", 5, 30, 20)

# 4. التصميم المخصص (CSS)
st.markdown(f"""
<style>
    .stApp {{ background: {selected_gradient} !important; background-attachment: fixed !important; }}
    [data-testid="stSidebar"] {{ background-color: rgba(0,0,0,0.5) !important; backdrop-filter: blur(10px); }}
    h1, h2, h3 {{ color: {clr} !important; text-align: center; text-shadow: 2px 2px 10px rgba(0,0,0,0.7); }}
    .category-header {{ background: rgba(255, 255, 255, 0.05); padding: 5px 15px; border-radius: 12px; border-right: 5px solid {clr}; margin-top: 25px; text-align: right; }}
    .p-box {{ border: 1px solid {clr}44; padding: 15px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(5px); }}
    .habit-card {{ border: 1px solid {clr}44; padding: 12px; border-radius: 12px; background: rgba(255,255,255,0.05); margin-bottom: 10px; text-align: center; }}
    .stButton>button {{ background-color: {clr} !important; color: #000000 !important; font-weight: bold !important; border-radius: 10px !important; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; justify-content: center; }}
    .stTabs [data-baseweb="tab"] {{ background-color: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px 20px; color: white; }}
    .focus-timer {{ font-size: 5rem; font-weight: bold; color: {clr}; text-align: center; font-family: 'Courier New', Courier, monospace; }}
</style>
""", unsafe_allow_html=True)

# 5. تهيئة مخزن البيانات
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []
if 'focus_points' not in st.session_state: st.session_state.focus_points = 0

def get_habit_message(habit):
    if habit['status'] is True:
        return "✅ بطل! استمر." if habit['type'] == 'good' else "⚠️ حاول غداً أن تكون أقوى."
    elif habit['status'] is False:
        return "💡 ابدأ الآن!" if habit['type'] == 'good' else "✨ إنجاز عظيم اليوم."
    return None

st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.1rem; color:{clr};'>CREATED BY: FIRAS | نقاط التركيز: {st.session_state.focus_points} 🏆</p>", unsafe_allow_html=True)

tab_home, tab_full, tab_habits, tab_focus = st.tabs(["🏠 الرئيسية", "📑 الجدول", "🎯 العادات", "⏱️ جلسة التركيز"])

# --- التبويب الأول: الرئيسية ---
with tab_home:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("🚀 المهام القادمة")
        if st.session_state.tk:
            now = dt.now().strftime("%H:%M")
            for t in st.session_state.tk[:3]: # عرض أول 3 مهام فقط للتبسيط
                st.markdown(f'<div style="border-right:4px solid {clr}; padding:10px; background:rgba(255,255,255,0.05); margin-bottom:5px;">{t["name"]} <span style="float:left; color:{clr};">{t["start"]}</span></div>', unsafe_allow_html=True)
        else: st.info("الجدول فارغ")
    with c2:
        st.subheader("🎯 العادات")
        for h in st.session_state.habits[:2]:
            msg = get_habit_message(h)
            st.markdown(f'<div class="habit-card" style="border-left:3px solid {clr};"><b>{h["name"]}</b><br><small>{msg if msg else "انتظار..."}</small></div>', unsafe_allow_html=True)

# --- التبويب الثاني: الجدول والصلوات --- (نفس الكود السابق للاختصار)
with tab_full:
    city = st.text_input("📍 المدينة:", "Muscat")
    # ... (كود أوقات الصلاة والجدول كما هو في الرد السابق)
    st.write("أضف مهامك هنا لإدارتها بشكل كامل.")

# --- التبويب الثالث: متتبع العادات ---
with tab_habits:
    # ... (كود العادات كما هو في الرد السابق)
    st.write("تتبع تقدمك اليومي هنا.")

# --- التبويب الرابع الجديد: جلسة التركيز (Focus Mode) ---
with tab_focus:
    st.subheader("⏱️ مؤقت بومودورو للتركيز")
    st.write("ركز في مهمتك لمدة 25 دقيقة واحصل على نقاط مكافأة!")
    
    focus_time = st.number_input("حدد وقت التركيز (بالدقائق):", 1, 60, 25)
    
    if st.button("بدء جلسة التركيز 🚀"):
        placeholder = st.empty()
        seconds = focus_time * 60
        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            placeholder.markdown(f'<div class="focus-timer">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
            seconds -= 1
        
        st.session_state.focus_points += 10
        st.balloons()
        st.success(f"رائع يا FIRAS! حصلت على 10 نقاط. مجموع نقاطك الآن: {st.session_state.focus_points}")
        placeholder.markdown(f'<div class="focus-timer">00:00</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **FIRAS**")
