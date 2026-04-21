import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
import requests
import random

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
    .category-header {{ background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; border-right: 5px solid {clr}; margin-top: 20px; text-align: right; color: white; }}
    .p-box {{ border: 2px solid {clr}; padding: 10px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); min-height: 120px; display: flex; flex-direction: column; justify-content: center; }}
    .habit-card {{ background: rgba(0, 0, 0, 0.4); padding: 20px; border-radius: 15px; border: 2px solid {clr}; margin-bottom: 20px; }}
    .home-box {{ border-left: 5px solid {clr}; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 10px; }}
    .stButton>button {{ background-color: {clr} !important; color: #000000 !important; font-weight: 900 !important; border-radius: 12px !important; width: 100%; }}
</style>
""", unsafe_allow_html=True)

# 5. العنوان الرئيسي
st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.4rem; color:{clr}; font-weight:bold;'>إعداد: FIRAS</p>", unsafe_allow_html=True)

# تهيئة المخازن
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []

# --- 6. نظام التبويبات ---
tab_home, tab_full, tab_habits = st.tabs(["🏠 الرئيسية", "📑 الجدول والصلوات", "🚀 متتبع العادات"])

# --- تبويب الرئيسية ---
with tab_home:
    st.subheader("🚀 نظرة سريعة على يومك")
    if st.session_state.tk:
        categories = sorted(list(set([t['category'] for t in st.session_state.tk])))
        now_time = dt.now().strftime("%H:%M")
        for cat in categories:
            cat_tasks = sorted([t for t in st.session_state.tk if t['category'] == cat], key=lambda x: x['raw_time'])
            next_task = next((t for t in cat_tasks if t['raw_time'] >= now_time), (cat_tasks[0] if cat_tasks else None))
            st.markdown(f"""<div class="home-box"><span style="font-size: 1.3rem; font-weight: bold; color: {clr};">📁 {cat}</span><br>
            <span style="color: white; opacity: 0.8;">المهمة القادمة: </span><b style="color: white; font-size: 1.1rem;">{next_task['name'] if next_task else 'لا يوجد'}</b> 
            <span style="float: left; color: {clr};">{next_task['start'] if next_task else ''}</span></div>""", unsafe_allow_html=True)
    else: st.info("لا توجد مهام حالياً.")

# --- تبويب الجدول والصلوات ---
with tab_full:
    city = st.text_input("📍 اكتب المدينة هنا:", "Muscat")
    @st.cache_data(ttl=3600)
    def get_p(c):
        try:
            r = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={c}&country=Oman&method=4").json()
            return r['data']['timings']
        except: return None
    t_data = get_p(city)
    if t_data:
        cols = st.columns(5); p_names = {"Fajr":"الفجر","Dhuhr":"الظهر","Asr":"العصر","Maghrib":"المغرب","Isha":"العشاء"}
        for i, (k, v) in enumerate(p_names.items()):
            azan_dt = dt.strptime(t_data[k], "%H:%M")
            iqama_dt = azan_dt + timedelta(minutes=iqama_offset)
            cols[i].markdown(f'<div class="p-box"><b style="color:{clr}; font-size:1.2rem;">{v}</b><br><span style="color:white;">📢 {azan_dt.strftime("%I:%M %p")}</span><br><span style="color:white; font-size:0.8rem; opacity:0.8;">⏳ الإقامة: {iqama_dt.strftime("%I:%M %p")}</span></div>', unsafe_allow_html=True)
    
    st.divider()
    with st.form("task_form", clear_on_submit=True):
        cat_in = st.text_input("العنوان الرئيسي:", "عام")
        name_in = st.text_input("اسم المهمة:")
        c1, c2 = st.columns(2)
        start_in = c1.time_input("البداية"); end_in = c2.time_input("النهاية")
        if st.form_submit_button("إضافة للمجموعة ✨") and name_in:
            st.session_state.tk.append({"id": str(dt.now().timestamp()), "category": cat_in, "name": name_in, "start": start_in.strftime("%I:%M %p"), "end": end_in.strftime("%I:%M %p"), "raw_time": start_in.strftime("%H:%M")})
            st.rerun()

    for task in st.session_state.tk:
        if st.button(f"❌ حذف {task['name']}", key=task['id']):
            st.session_state.tk = [t for t in st.session_state.tk if t['id'] != task['id']]; st.rerun()

# --- تبويب متتبع العادات (تم إصلاح مكان الصندوق) ---
with tab_habits:
    st.subheader("💪 متتبع العادات الذكي")
    
    with st.expander("➕ أضف عادة جديدة لتتبعها"):
        with st.form("habit_form", clear_on_submit=True):
            h_name = st.text_input("اسم العادة:")
            h_type = st.radio("نوع العادة:", ["عادة حسنة 👍", "عادة سيئة 👎"], horizontal=True)
            if st.form_submit_button("إضافة"):
                if h_name:
                    st.session_state.habits.append({"id": str(dt.now().timestamp()), "name": h_name, "type": h_type, "status": None})
                    st.rerun()

    if st.session_state.habits:
        for i, habit in enumerate(st.session_state.habits):
            # بداية الصندوق (Card)
            st.markdown(f'<div class="habit-card">', unsafe_allow_html=True)
            
            st.write(f"### {habit['name']} ({habit['type']})")
            col_h1, col_h2 = st.columns(2)
            
            if col_h1.button("✅ سويتها / تجنبتها", key=f"yes_{habit['id']}"):
                habit['status'] = True
            if col_h2.button("❌ ما سويتها / وقعت فيها", key=f"no_{habit['id']}"):
                habit['status'] = False
            
            # عرض الرسائل داخل الصندوق
            if habit['status'] is True:
                msg = "بطل! استمر في الإنجاز ✨" if habit['type'] == "عادة حسنة 👍" else "قوة إرادة حديدية! 💎"
                st.success(msg)
            elif habit['status'] is False:
                msg = "نصيحة: ابدأ بصغير! حاول فعل جزء بسيط منها الآن." if habit['type'] == "عادة حسنة 👍" else "لا بأس، تذكر لماذا أردت تركها وحاول مجدداً!"
                st.info(msg)
            
            if st.button("🗑️ حذف هذه العادة", key=f"del_h_{habit['id']}"):
                st.session_state.habits.pop(i)
                st.rerun()
                
            # نهاية الصندوق
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("ابدأ بإضافة أول عادة لك!")

st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **FIRAS**")
