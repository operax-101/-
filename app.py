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
    "تدرج الأرجواني (Midnight)": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)"
}

# 3. السايدبار
st.sidebar.title("🎨 لوحة التحكم")
clr = st.sidebar.color_picker("اختر لون التميز:", "#D4AF37")
bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
selected_gradient = gradients[bg_key]
iqama_offset = st.sidebar.slider("دقائق الانتظار للإقامة:", 5, 30, 20)

# 4. التصميم المخصص (CSS)
st.markdown(f"""
<style>
    .stApp {{ background: {selected_gradient} !important; background-attachment: fixed !important; }}
    h1, h2, h3 {{ color: {clr} !important; text-align: center; }}
    .habit-card {{ background: rgba(0, 0, 0, 0.4); border-radius: 15px; border: 2px solid {clr}; margin-bottom: 20px; overflow: hidden; }}
    .habit-header {{ background: {clr}; padding: 10px; color: black !important; text-align: center; font-weight: bold; font-size: 1.2rem; }}
    .habit-body {{ padding: 20px; }}
    .category-header {{ background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; border-right: 5px solid {clr}; margin-top: 20px; text-align: right; color: white; }}
    .p-box {{ border: 2px solid {clr}; padding: 10px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); min-height: 120px; display: flex; flex-direction: column; justify-content: center; }}
    .home-box {{ border-left: 5px solid {clr}; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 10px; }}
    .stButton>button {{ background-color: {clr} !important; color: black !important; font-weight: bold; border-radius: 10px; width: 100%; }}
</style>
""", unsafe_allow_html=True)

# 5. منطق تحليل العادات
def analyze_habit(name):
    bad_keywords = ['سهر', 'تدخين', 'اكل سريع', 'غضب', 'تأجيل', 'تسويف', 'جوال', 'تلفون', 'حلويات', 'سكر']
    is_bad = any(word in name.lower() for word in bad_keywords)
    if is_bad:
        return {"type": "سيئة 👎", "on_success": "انتصار كبير! تجنب هذه العادة يقوي إرادتك.", "on_fail": "لا بأس، تذكر أن صحتك أهم. حاول غداً مجدداً."}
    return {"type": "حسنة 👍", "on_success": "استمر! أنت تصنع مستقبلك الآن.", "on_fail": "لا بأس بالعثرات، السر في الاستمرار. حاول الآن ولو لثوانٍ."}

# إدارة الحالة
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []
if st.session_state.habits and "info" not in st.session_state.habits[0]: st.session_state.habits = []

# العنوان
st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:{clr};'>إعداد: FIRAS</p>", unsafe_allow_html=True)

tab_home, tab_full, tab_habits = st.tabs(["🏠 الرئيسية", "📑 الجدول والصلوات", "🚀 متتبع العادات الذكي"])

# --- تبويب الرئيسية ---
with tab_home:
    st.subheader("🚀 نظرة سريعة")
    if st.session_state.tk:
        categories = sorted(list(set([t['category'] for t in st.session_state.tk])))
        now_time = dt.now().strftime("%H:%M")
        for cat in categories:
            cat_tasks = sorted([t for t in st.session_state.tk if t['category'] == cat], key=lambda x: x['raw_time'])
            next_task = next((t for t in cat_tasks if t['raw_time'] >= now_time), (cat_tasks[0] if cat_tasks else None))
            st.markdown(f"""<div class="home-box"><span style="font-size: 1.3rem; font-weight: bold; color: {clr};">📁 {cat}</span><br>
            <span style="color: white; opacity: 0.8;">المهمة القادمة: </span><b style="color: white;">{next_task['name'] if next_task else 'لا يوجد'}</b></div>""", unsafe_allow_html=True)
    else: st.info("أضف مهامك من تبويب الجدول.")

# --- تبويب الجدول والصلوات ---
with tab_full:
    city = st.text_input("📍 المدينة:", "Muscat")
    @st.cache_data(ttl=3600)
    def get_p(c):
        try: return requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={c}&country=Oman&method=4").json()['data']['timings']
        except: return None
    t_data = get_p(city)
    if t_data:
        cols = st.columns(5); p_names = {"Fajr":"الفجر","Dhuhr":"الظهر","Asr":"العصر","Maghrib":"المغرب","Isha":"العشاء"}
        for i, (k, v) in enumerate(p_names.items()):
            azan_dt = dt.strptime(t_data[k], "%H:%M")
            iq_dt = azan_dt + timedelta(minutes=iqama_offset)
            cols[i].markdown(f'<div class="p-box"><b style="color:{clr};">{v}</b><br><span style="color:white;">📢 {azan_dt.strftime("%I:%M %p")}</span><br><span style="font-size:0.7rem; color:white;">⏳ الإقامة: {iq_dt.strftime("%I:%M %p")}</span></div>', unsafe_allow_html=True)
    
    st.divider()
    with st.form("task_form", clear_on_submit=True):
        c_in = st.text_input("العنوان الرئيسي:"); n_in = st.text_input("المهمة:")
        c1, c2 = st.columns(2); s_in = c1.time_input("البداية"); e_in = c2.time_input("النهاية")
        if st.form_submit_button("إضافة ✨") and n_in:
            st.session_state.tk.append({"id": str(dt.now().timestamp()), "category": c_in, "name": n_in, "start": s_in.strftime("%I:%M %p"), "end": e_in.strftime("%I:%M %p"), "raw_time": s_in.strftime("%H:%M")})
            st.rerun()

    for task in st.session_state.tk:
        if st.button(f"❌ حذف {task['name']}", key=task['id']):
            st.session_state.tk = [t for t in st.session_state.tk if t['id'] != task['id']]; st.rerun()

# --- تبويب متتبع العادات الذكي ---
with tab_habits:
    st.subheader("🤖 محلل العادات")
    with st.expander("➕ أضف عادة جديدة"):
        with st.form("h_form", clear_on_submit=True):
            h_input = st.text_input("ما هي العادة؟")
            if st.form_submit_button("تحليل وإضافة ✨"):
                if h_input:
                    st.session_state.habits.append({"id": str(dt.now().timestamp()), "name": h_input, "info": analyze_habit(h_input), "status": None})
                    st.rerun()

    for i, habit in enumerate(st.session_state.habits):
        st.markdown(f'<div class="habit-card"><div class="habit-header">{habit["name"]} | {habit["info"]["type"]}</div><div class="habit-body">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("✅ تم", key=f"y_{habit['id']}"): habit['status'] = True
        if c2.button("❌ لم يتم", key=f"n_{habit['id']}"): habit['status'] = False
        if habit['status'] is True: st.success(habit['info']['on_success'])
        elif habit['status'] is False: st.warning(habit['info']['on_fail'])
        if st.button("🗑️ حذف", key=f"d_{habit['id']}"): st.session_state.habits.pop(i); st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **FIRAS**")
