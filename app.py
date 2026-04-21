import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="FIRAS SCHEDULER", layout="wide", page_icon="📅")

# 2. قائمة التدرجات المعتمدة
gradients = {
    "تدرج المحيط (Deep Ocean)": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
    "تدرج الغسق (Sunset Dusk)": "linear-gradient(135deg, #2c3e50 0%, #000000 100%)",
    "تدرج ملكي (Royal Gold)": "linear-gradient(135deg, #1a1a1a 0%, #434343 100%)",
    "تدرج الأرجواني (Midnight)": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)"
}

# 3. السايدبار (Control Panel)
st.sidebar.title("🎨 لوحة التحكم")
clr = st.sidebar.color_picker("اختر لون التميز:", "#D4AF37")
bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
selected_gradient = gradients[bg_key]
iqama_offset = st.sidebar.slider("دقائق الانتظار للإقامة:", 5, 30, 20)

# 4. التصميم المخصص (CSS) - النسخة المحسنة
st.markdown(f"""
<style>
    .stApp {{ background: {selected_gradient} !important; background-attachment: fixed !important; }}
    h1, h2, h3 {{ color: {clr} !important; text-align: center; text-shadow: 2px 2px 10px rgba(0,0,0,0.7); }}
    
    /* ستايل البطاقات المدمج */
    .firas-card {{ 
        background: rgba(0, 0, 0, 0.5); 
        border-radius: 12px; 
        border: 1px solid {clr}; 
        margin-bottom: 15px; 
        transition: 0.3s;
    }}
    .firas-card:hover {{ transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }}
    
    .card-header {{
        background: {clr};
        padding: 8px;
        color: black !important;
        text-align: center;
        font-weight: bold;
        border-radius: 10px 10px 0 0;
    }}
    .card-body {{ padding: 15px; text-align: center; color: white; }}
    
    .p-box {{ border: 2px solid {clr}; padding: 10px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); }}
    .stButton>button {{ background-color: {clr} !important; color: black !important; font-weight: bold; border-radius: 8px !important; }}
</style>
""", unsafe_allow_html=True)

# العنوان
st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:{clr};'>إعداد: FIRAS</p>", unsafe_allow_html=True)

# إدارة الحالة
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []

tab_home, tab_full, tab_habits = st.tabs(["🏠 الرئيسية", "📑 الجدول والصلوات", "🚀 متتبع العادات"])

# --- تبويب الجدول والصلوات (العودة للتصميم القديم الجميل) ---
with tab_full:
    city = st.text_input("📍 المدينة:", "Muscat")
    @st.cache_data(ttl=3600)
    def get_p(c):
        try: return requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={c}&country=Oman&method=4").json()['data']['timings']
        except: return None
    
    t_data = get_p(city)
    if t_data:
        cols = st.columns(5)
        p_names = {"Fajr":"الفجر","Dhuhr":"الظهر","Asr":"العصر","Maghrib":"المغرب","Isha":"العشاء"}
        for i, (k, v) in enumerate(p_names.items()):
            azan_dt = dt.strptime(t_data[k], "%H:%M")
            iq_dt = azan_dt + timedelta(minutes=iqama_offset)
            cols[i].markdown(f'<div class="p-box"><b style="color:{clr};">{v}</b><br>{azan_dt.strftime("%I:%M %p")}<br><small>الإقامة: {iq_dt.strftime("%I:%M %p")}</small></div>', unsafe_allow_html=True)
    
    st.divider()
    
    # نموذج الإضافة بشكل مرتب
    with st.form("task_form", clear_on_submit=True):
        st.markdown(f"<h3 style='font-size:1.2rem;'>📝 إضافة مهمة جديدة</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        cat_in = col1.text_input("المجموعة (مثل: دراسة):", "عام")
        name_in = col2.text_input("اسم المهمة:")
        col3, col4 = st.columns(2)
        s_in = col3.time_input("وقت البدء")
        e_in = col4.time_input("وقت الانتهاء")
        if st.form_submit_button("إضافة للمجموعة ✨") and name_in:
            st.session_state.tk.append({
                "id": str(dt.now().timestamp()), 
                "category": cat_in, 
                "name": name_in, 
                "start": s_in.strftime("%I:%M %p"), 
                "end": e_in.strftime("%I:%M %p")
            })
            st.rerun()

    # عرض المهام بنظام الشبكة (Grid) بدلاً من القائمة الطويلة
    if st.session_state.tk:
        st.subheader("📌 جدول مهامك الحالي")
        task_cols = st.columns(3) # يعرض 3 مهام في كل صف ليكون التصميم مرتباً
        for i, task in enumerate(st.session_state.tk):
            with task_cols[i % 3]:
                st.markdown(f"""
                    <div class="firas-card">
                        <div class="card-header">{task['category']}</div>
                        <div class="card-body">
                            <b>{task['name']}</b><br>
                            <small>⏱️ {task['start']} - {task['end']}</small>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"🗑️ حذف {task['name']}", key=task['id']):
                    st.session_state.tk.pop(i); st.rerun()

# (تبويب العادات والتبويبات الأخرى تبقى منظمة بنفس هذا الأسلوب)
