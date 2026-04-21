import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
import requests

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
    .p-box {{ border: 1px solid {clr}44; padding: 15px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(5px); transition: 0.3s; }}
    .p-box:hover {{ border-color: {clr}; transform: translateY(-3px); }}
    .habit-card {{ border: 1px solid {clr}44; padding: 15px; border-radius: 15px; background: rgba(255,255,255,0.05); margin-bottom: 10px; text-align: center; }}
    .stButton>button {{ background-color: {clr} !important; color: #000000 !important; font-weight: bold !important; border-radius: 10px !important; border: none !important; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; justify-content: center; }}
    .stTabs [data-baseweb="tab"] {{ background-color: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px 20px; color: white; }}
    .stTabs [aria-selected="true"] {{ background-color: {clr}33 !important; border-bottom: 2px solid {clr} !important; }}
    .advice-box {{ font-size: 0.9rem; margin-top: 8px; padding: 5px; border-radius: 5px; background: rgba(255,255,255,0.1); }}
</style>
""", unsafe_allow_html=True)

# 5. تهيئة مخزن البيانات (Session State)
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []

# دالة لجلب العبارات (نفس المنطق في التبويبات والصفحة الرئيسية)
def get_habit_message(habit):
    if habit['status'] is True:
        if habit['type'] == 'good': return "✅ بطل! استمر في هذا الإنجاز. 🌟"
        else: return "⚠️ لا بأس، حاول غداً أن تكون أقوى. 👊"
    elif habit['status'] is False:
        if habit['type'] == 'good': return "💡 تذكر لماذا بدأت، حاول الآن! 🔥"
        else: return "✨ إنجاز عظيم! انتصرت على نفسك اليوم. 🌟"
    return None

# العنوان الرئيسي
st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:{clr}; letter-spacing: 2px;'>CREATED BY: FIRAS</p>", unsafe_allow_html=True)

# 6. نظام التبويبات
tab_home, tab_full, tab_habits = st.tabs(["🏠 الرئيسية", "📑 الجدول والصلوات", "🎯 متتبع العادات"])

# --- التبويب الأول: الرئيسية ---
with tab_home:
    col_sched, col_habit_mini = st.columns([2, 1])
    
    with col_sched:
        st.subheader("🚀 المهام القادمة")
        if st.session_state.tk:
            now_str = dt.now().strftime("%H:%M")
            categories = sorted(list(set([t['category'] for t in st.session_state.tk])))
            for cat in categories:
                cat_tasks = sorted([t for t in st.session_state.tk if t['category'] == cat], key=lambda x: x['raw_time'])
                next_task = next((t for t in cat_tasks if t['raw_time'] >= now_str), cat_tasks[0] if cat_tasks else None)
                st.markdown(f"""
                <div style="border-right: 5px solid {clr}; padding: 15px; background: rgba(255,255,255,0.07); border-radius: 12px; margin-bottom: 10px;">
                    <span style="color:{clr}; font-weight:bold;">📁 {cat}</span><br>
                    <span style="color:white; font-size:1.1rem;">المهمة القادمة: <b>{next_task['name'] if next_task else 'لا يوجد'}</b></span>
                    <span style="float:left; color:{clr};">{next_task['start'] if next_task else ''}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد مهام.")

    with col_habit_mini:
        st.subheader("🎯 أهم العادات")
        if st.session_state.habits:
            # عرض أول عادتين فقط
            for i, habit in enumerate(st.session_state.habits[:2]):
                msg = get_habit_message(habit)
                card_border = clr if habit['type'] == 'good' else "#ff4b4b"
                st.markdown(f"""
                <div style="border: 1px solid {card_border}66; padding: 12px; border-radius: 12px; background: rgba(0,0,0,0.3); margin-bottom: 10px;">
                    <div style="color:{card_border}; font-weight:bold; font-size:1rem;">{habit['name']}</div>
                    <div style="color:white; font-size:0.85rem; margin-top:5px;">
                        {msg if msg else "لم يتم التقييم بعد ⏳"}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("أضف عاداتك لتظهر هنا")

# --- التبويب الثاني: الجدول والصلوات ---
with tab_full:
    # أوقات الصلاة
    city = st.text_input("📍 المدينة:", "Muscat")
    @st.cache_data(ttl=3600)
    def get_prayer_times(c):
        try:
            r = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={c}&country=Oman&method=4").json()
            return r['data']['timings']
        except: return None

    t_data = get_prayer_times(city)
    if t_data:
        p_names = {"Fajr":"الفجر","Dhuhr":"الظهر","Asr":"العصر","Maghrib":"المغرب","Isha":"العشاء"}
        cols = st.columns(5)
        for i, (k, v) in enumerate(p_names.items()):
            azan_dt = dt.strptime(t_data[k], "%H:%M")
            iqama_dt = azan_dt + timedelta(minutes=iqama_offset)
            cols[i].markdown(f"""<div class="p-box"><b style="color:{clr};">{v}</b><br>{azan_dt.strftime("%I:%M %p")}<br><small style="opacity:0.7;">إقامة: {iqama_dt.strftime("%I:%M %p")}</small></div>""", unsafe_allow_html=True)

    st.divider()
    
    # نموذج إضافة مهمة
    with st.expander("➕ إضافة مهمة جديدة"):
        with st.form("task_form", clear_on_submit=True):
            c_cat = st.text_input("الفئة:", "عام")
            c_name = st.text_input("اسم المهمة:")
            c1, c2 = st.columns(2)
            t_s = c1.time_input("البداية")
            t_e = c2.time_input("النهاية")
            if st.form_submit_button("إضافة ✅") and c_name:
                st.session_state.tk.append({"id": str(dt.now().timestamp()), "category": c_cat, "name": c_name, "start": t_s.strftime("%I:%M %p"), "end": t_e.strftime("%I:%M %p"), "raw_time": t_s.strftime("%H:%M")})
                st.rerun()

    if st.session_state.tk:
        categories = sorted(list(set([t['category'] for t in st.session_state.tk])))
        for cat in categories:
            st.markdown(f'<div class="category-header"><h3>📁 {cat}</h3></div>', unsafe_allow_html=True)
            cat_tasks = sorted([t for t in st.session_state.tk if t['category'] == cat], key=lambda x: x['raw_time'])
            cols = st.columns(4)
            for j, task in enumerate(cat_tasks):
                with cols[j % 4]:
                    st.markdown(f'<div class="p-box" style="margin-bottom:5px;"><b>{task["name"]}</b><br><small>{task["start"]} - {task["end"]}</small></div>', unsafe_allow_html=True)
                    if st.button("❌", key=task['id']):
                        st.session_state.tk = [t for t in st.session_state.tk if t['id'] != task['id']]
                        st.rerun()

# --- التبويب الثالث: متتبع العادات ---
with tab_habits:
    st.subheader("🎯 متتبع العادات اليومي")
    with st.expander("➕ أضف عادة جديدة"):
        with st.form("habit_form", clear_on_submit=True):
            h_name = st.text_input("اسم العادة:")
            h_type = st.radio("نوع العادة:", ["جيدة ✨", "سيئة ⚠️"], horizontal=True)
            if st.form_submit_button("إضافة"):
                if h_name:
                    st.session_state.habits.append({"name": h_name, "type": "good" if "جيدة" in h_type else "bad", "status": None})
                    st.rerun()

    if st.session_state.habits:
        h_cols = st.columns(2)
        for i, habit in enumerate(st.session_state.habits):
            with h_cols[i % 2]:
                card_clr = clr if habit['type'] == 'good' else "#ff4b4b"
                st.markdown(f"""<div class="habit-card" style="border-top: 4px solid {card_clr};">
                    <h4 style="margin:0;">{habit['name']}</h4>
                </div>""", unsafe_allow_html=True)
                
                b1, b2, b3 = st.columns([1,1,1])
                if b1.button("✅ فعلت", key=f"y_{i}"): habit['status'] = True
                if b2.button("❌ لم أفعل", key=f"n_{i}"): habit['status'] = False
                if b3.button("🗑️", key=f"d_{i}"):
                    st.session_state.habits.pop(i)
                    st.rerun()

                msg = get_habit_message(habit)
                if msg:
                    if "✅" in msg or "✨" in msg: st.success(msg)
                    elif "⚠️" in msg: st.warning(msg)
                    else: st.info(msg)
    
    if st.button("🔄 تصفير التتبع لليوم الجديد"):
        for h in st.session_state.habits: h['status'] = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align:center; color:{clr};'><b>FIRAS SCHEDULER v2.2</b></div>", unsafe_allow_html=True)
