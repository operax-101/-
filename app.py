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
    "تدرج الأرجواني (Midnight)": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)"
}

# 3. السايدبار
st.sidebar.title("🎨 لوحة التحكم")
clr = st.sidebar.color_picker("اختر لون التميز (Accent Color):", "#D4AF37")
bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
selected_gradient = gradients[bg_key]
iqama_offset = st.sidebar.slider("دقائق الانتظار للإقامة:", 5, 30, 20)

# 4. التصميم المخصص (CSS)
st.markdown(f"""
<style>
    .stApp {{ background: {selected_gradient} !important; background-attachment: fixed !important; }}
    h1, h2, h3 {{ color: {clr} !important; text-align: center; text-shadow: 2px 2px 10px rgba(0,0,0,0.7); }}
    
    /* ستايل البطاقات للمهام والعادات */
    .custom-card {{ 
        background: rgba(0, 0, 0, 0.4); 
        border-radius: 15px; 
        border: 2px solid {clr}; 
        margin-bottom: 20px; 
        overflow: hidden;
    }}
    .card-header {{
        background: {clr};
        padding: 10px;
        color: black !important;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
    }}
    .card-body {{ padding: 15px; color: white; }}
    
    .p-box {{ border: 2px solid {clr}; padding: 10px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); }}
    .home-box {{ border-left: 5px solid {clr}; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 10px; }}
    .stButton>button {{ background-color: {clr} !important; color: black !important; font-weight: 900 !important; border-radius: 10px !important; }}
</style>
""", unsafe_allow_html=True)

# 5. منطق تحليل العادات الذكي
def analyze_habit(name):
    bad_keywords = ['سهر', 'تدخين', 'اكل سريع', 'غضب', 'تأجيل', 'تسويف', 'جوال', 'حلويات', 'سكر']
    is_bad = any(word in name.lower() for word in bad_keywords)
    if is_bad:
        return {"type": "سيئة 👎", "on_success": "انتصار كبير! قوة إرادة حديدية 💎", "on_fail": "لا بأس، تذكر هدفك وحاول مجدداً!"}
    return {"type": "حسنة 👍", "on_success": "بطل! استمر في الإنجاز ✨", "on_fail": "ابدأ بصغير! حاول مجدداً."}

# إدارة الحالة
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []

# حماية البيانات
if st.session_state.habits and "info" not in st.session_state.habits[0]: st.session_state.habits = []

st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.4rem; color:{clr}; font-weight:bold;'>إعداد: FIRAS</p>", unsafe_allow_html=True)

tab_home, tab_full, tab_habits = st.tabs(["🏠 الرئيسية", "📑 الجدول والصلوات", "🚀 متتبع العادات الذكي"])

# --- تبويب الرئيسية ---
with tab_home:
    st.subheader("🚀 نظرة سريعة")
    if st.session_state.tk:
        categories = sorted(list(set([t['category'] for t in st.session_state.tk])))
        for cat in categories:
            cat_tasks = [t for t in st.session_state.tk if t['category'] == cat]
            for t in cat_tasks:
                st.markdown(f"""<div class="home-box"><b style="color:{clr};">{cat}</b>: {t['name']} <span style="float:left;">{t['start']}</span></div>""", unsafe_allow_html=True)
    else: st.info("لا توجد مهام حالياً.")

# --- تبويب الجدول والصلوات (رجوع نظام البطاقات للمهام) ---
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
            cols[i].markdown(f'<div class="p-box"><b style="color:{clr};">{v}</b><br>{azan_dt.strftime("%I:%M %p")}<br><small>الإقامة: {iq_dt.strftime("%I:%M %p")}</small></div>', unsafe_allow_html=True)
    
    st.divider()
    with st.form("task_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        cat_in = c1.text_input("العنوان الرئيسي (مثلاً: المذاكرة):", "عام")
        name_in = c2.text_input("اسم المهمة:")
        t1, t2 = st.columns(2)
        s_in = t1.time_input("البداية"); e_in = t2.time_input("النهاية")
        if st.form_submit_button("إضافة للمجموعة ✨") and name_in:
            st.session_state.tk.append({"id": str(dt.now().timestamp()), "category": cat_in, "name": name_in, "start": s_in.strftime("%I:%M %p"), "end": e_in.strftime("%I:%M %p"), "raw_time": s_in.strftime("%H:%M")})
            st.rerun()

    # عرض المهام بنظام البطاقات (كما كانت سابقاً)
    if st.session_state.tk:
        for i, task in enumerate(st.session_state.tk):
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-header">{task['category']} | {task['name']}</div>
                    <div class="card-body" style="text-align:center;">
                        ⏱️ من <b>{task['start']}</b> إلى <b>{task['end']}</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"🗑️ حذف مهمة {task['name']}", key=f"del_{task['id']}"):
                st.session_state.tk.pop(i); st.rerun()

# --- تبويب العادات الذكي ---
with tab_habits:
    st.subheader("🤖 محلل العادات")
    with st.expander("➕ أضف عادة"):
        with st.form("h_form", clear_on_submit=True):
            h_input = st.text_input("اكتب العادة هنا:")
            if st.form_submit_button("تحليل وإضافة"):
                if h_input:
                    st.session_state.habits.append({"id": str(dt.now().timestamp()), "name": h_input, "info": analyze_habit(h_input), "status": None})
                    st.rerun()

    for i, habit in enumerate(st.session_state.habits):
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-header">{habit['name']} | {habit['info']['type']}</div>
                <div class="card-body">
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("✅ تم", key=f"y_{habit['id']}"): habit['status'] = True
        if c2.button("❌ لم يتم", key=f"n_{habit['id']}"): habit['status'] = False
        if habit['status'] is True: st.success(habit['info']['on_success'])
        elif habit['status'] is False: st.warning(habit['info']['on_fail'])
        if st.button("🗑️ حذف العادة", key=f"dh_{habit['id']}"): st.session_state.habits.pop(i); st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **FIRAS**")
