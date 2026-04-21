import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="FIRAS SCHEDULER", layout="wide", page_icon="📅")

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
    .p-box {{ border: 1px solid {clr}44; padding: 15px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(5px); transition: 0.3s; }}
    .p-box:hover {{ border-color: {clr}; transform: translateY(-3px); }}
    .home-box {{ border-right: 5px solid {clr}; padding: 15px; background: rgba(255,255,255,0.07); border-radius: 12px; margin-bottom: 12px; }}
    .iqama-text {{ font-size: 0.85rem; color: #ffffff; font-weight: bold; margin-top: 5px; opacity: 0.8; }}
    .stButton>button {{ background-color: {clr} !important; color: #000000 !important; font-weight: bold !important; border-radius: 10px !important; border: none !important; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ background-color: rgba(255,255,255,0.05); border-radius: 8px 8px 0 0; padding: 10px 20px; color: white; }}
    .stTabs [aria-selected="true"] {{ background-color: {clr}33 !important; border-bottom: 2px solid {clr} !important; }}
</style>
""", unsafe_allow_html=True)

# 5. العنوان الرئيسي
st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:{clr}; letter-spacing: 2px;'>CREATED BY: FIRAS</p>", unsafe_allow_html=True)

# تهيئة مخزن المهام
if 'tk' not in st.session_state:
    st.session_state.tk = []

# تنظيف البيانات القديمة
if st.session_state.tk and not all("category" in task for task in st.session_state.tk):
    st.session_state.tk = []
    st.rerun()

# --- 6. نظام التبويبات (Tabs) ---
tab_home, tab_full = st.tabs(["🏠 الرئيسية", "📑 إدارة الجدول"])

with tab_home:
    st.subheader("🚀 المهام القادمة")
    if st.session_state.tk:
        categories = sorted(list(set([t['category'] for t in st.session_state.tk])))
        now_str = dt.now().strftime("%H:%M")
        
        for cat in categories:
            cat_tasks = sorted([t for t in st.session_state.tk if t['category'] == cat], key=lambda x: x['raw_time'])
            next_task = next((t for t in cat_tasks if t['raw_time'] >= now_str), None)
            
            if not next_task and cat_tasks:
                next_task = cat_tasks[0] # عرض أول مهمة لليوم التالي

            st.markdown(f"""
            <div class="home-box">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 1.2rem; font-weight: bold; color: {clr};">📁 {cat}</span>
                    <span style="color: {clr}; font-family: monospace;">{next_task['start'] if next_task else ''}</span>
                </div>
                <div style="margin-top: 5px;">
                    <span style="color: white; opacity: 0.7; font-size: 0.9rem;">المهمة الحالية/القادمة:</span>
                    <div style="color: white; font-size: 1.1rem; font-weight: 500;">{next_task['name'] if next_task else 'مكتمل ✅'}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("الجدول فارغ حالياً. ابدأ بإضافة مهام في التبويب الثاني.")

with tab_full:
    # أوقات الصلاة
    city = st.text_input("📍 المدينة (لحساب أوقات الصلاة):", "Muscat")
    @st.cache_data(ttl=3600)
    def get_p(c):
        try:
            r = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={c}&country=Oman&method=4").json()
            return r['data']['timings']
        except: return None

    t_data = get_p(city)
    if t_data:
        p_names = {"Fajr":"الفجر","Dhuhr":"الظهر","Asr":"العصر","Maghrib":"المغرب","Isha":"العشاء"}
        cols = st.columns(len(p_names))
        for i, (k, v) in enumerate(p_names.items()):
            azan_dt = dt.strptime(t_data[k], "%H:%M")
            azan_str = azan_dt.strftime("%I:%M %p")
            iqama_dt = azan_dt + timedelta(minutes=iqama_offset)
            iqama_str = iqama_dt.strftime("%I:%M %p")
            
            cols[i].markdown(f"""
                <div class="p-box">
                    <div style="color:{clr}; font-weight:bold; margin-bottom:5px;">{v}</div>
                    <div style="color:white; font-size:1.1rem;">{azan_str}</div>
                    <div class="iqama-text">الإقامة: {iqama_str}</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # نموذج إضافة المهام
    with st.expander("➕ إضافة مهمة جديدة للجدول"):
        with st.form("task_form", clear_on_submit=True):
            col_a, col_b = st.columns([1, 2])
            category = col_a.text_input("المجموعة:", "عام")
            task_name = col_b.text_input("ماذا ستفعل؟")
            
            c1, c2 = st.columns(2)
            t_start = c1.time_input("وقت البدء")
            t_end = c2.time_input("وقت الانتهاء")
            
            if st.form_submit_button("حفظ المهمة ✅") and task_name:
                st.session_state.tk.append({
                    "id": str(dt.now().timestamp()), 
                    "category": category if category else "عام",
                    "name": task_name,
                    "start": t_start.strftime("%I:%M %p"),
                    "end": t_end.strftime("%I:%M %p"),
                    "raw_time": t_start.strftime("%H:%M") 
                })
                st.rerun()

    # عرض المهام حسب الفئات
    if st.session_state.tk:
        categories = sorted(list(set([t['category'] for t in st.session_state.tk])))
        for cat in categories:
            st.markdown(f'<div class="category-header"><h3>📁 {cat}</h3></div>', unsafe_allow_html=True)
            cat_tasks = sorted([t for t in st.session_state.tk if t['category'] == cat], key=lambda x: x['raw_time'])
            
            # عرض المهام في شبكة (Grid)
            n_cols = 4
            for i in range(0, len(cat_tasks), n_cols):
                batch = cat_tasks[i:i + n_cols]
                cols = st.columns(n_cols)
                for j, task in enumerate(batch):
                    with cols[j]:
                        st.markdown(f"""
                        <div class="p-box" style="margin-top: 10px; min-height: 100px;">
                            <div style="color:{clr}; font-weight: bold;">{task['name']}</div>
                            <div style="font-size: 0.85rem; color:white; opacity: 0.8;">{task['start']} - {task['end']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("حذف 🗑️", key=f"del_{task['id']}", use_container_width=True):
                            st.session_state.tk = [t for t in st.session_state.tk if t['id'] != task['id']]
                            st.rerun()
        
        st.divider()
        if st.button("🗑️ مسح الجدول بالكامل"):
            st.session_state.tk = []
            st.rerun()

# التذييل
st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align:center; color:{clr};'><b>FIRAS SCHEDULER v2.0</b></div>", unsafe_allow_html=True)
