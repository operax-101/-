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
    .p-box {{ border: 1px solid {clr}44; padding: 15px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(5px); transition: 0.3s; }}
    .p-box:hover {{ border-color: {clr}; transform: translateY(-3px); }}
    .habit-card {{ border: 1px solid {clr}44; padding: 15px; border-radius: 15px; background: rgba(255,255,255,0.05); margin-bottom: 10px; text-align: center; }}
    .stButton>button {{ background-color: {clr} !important; color: #000000 !important; font-weight: bold !important; border-radius: 10px !important; border: none !important; width: 100%; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; justify-content: center; }}
    .stTabs [data-baseweb="tab"] {{ background-color: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px 20px; color: white; }}
    .stTabs [aria-selected="true"] {{ background-color: {clr}33 !important; border-bottom: 2px solid {clr} !important; }}
    .timer-display {{ font-size: 4rem; font-weight: bold; color: {clr}; text-align: center; font-family: monospace; text-shadow: 0 0 20px {clr}55; }}
    .sticky-note {{ background: rgba(255, 255, 255, 0.05); border-right: 4px solid {clr}; padding: 15px; border-radius: 10px; color: white; white-space: pre-wrap; }}
</style>
""", unsafe_allow_html=True)

# 5. تهيئة مخزن البيانات (Session State)
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []
if 'notes_content' not in st.session_state: st.session_state.notes_content = ""

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

# 6. نظام التبويبات المحدث
tab_home, tab_study, tab_full, tab_habits, tab_notes = st.tabs(["🏠 الرئيسية", "📚 جلسة الدراسة", "📑 الجدول والصلوات", "🎯 متتبع العادات", "📝 الملاحظات"])

# --- التبويب الأول: الرئيسية (تم ربط الملاحظات هنا) ---
with tab_home:
    col_sched, col_side = st.columns([2, 1])
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

    with col_side:
        # عرض الملاحظات المثبتة في الرئيسية
        st.subheader("📌 ملاحظات مثبتة")
        if st.session_state.notes_content.strip():
            st.markdown(f'<div class="sticky-note">{st.session_state.notes_content}</div>', unsafe_allow_html=True)
        else:
            st.info("لا توجد ملاحظات مثبتة حالياً.")
        
        st.divider()
        st.subheader("🎯 العادات")
        if st.session_state.habits:
            for i, habit in enumerate(st.session_state.habits[:2]):
                msg = get_habit_message(habit)
                card_border = clr if habit['type'] == 'good' else "#ff4b4b"
                st.markdown(f"""
                <div style="border: 1px solid {card_border}66; padding: 12px; border-radius: 12px; background: rgba(0,0,0,0.3); margin-bottom: 10px;">
                    <div style="color:{card_border}; font-weight:bold; font-size:1rem;">{habit['name']}</div>
                    <div style="color:white; font-size:0.85rem; margin-top:5px;">{msg if msg else "لم يتم التقييم بعد ⏳"}</div>
                </div>
                """, unsafe_allow_html=True)

# --- التبويب الجديد: الملاحظات (هنا تكتب الملاحظات لتظهر في الرئيسي) ---
with tab_notes:
    st.subheader("📝 دفتر الملاحظات")
    st.markdown("ما تكتبه هنا سيظهر تلقائياً في التبويب الرئيسي كـ **ملاحظات مثبتة**.")
    # ربط المدخلات بمخزن البيانات
    st.session_state.notes_content = st.text_area("اكتب ملاحظاتك، أهدافك، أو تذكيراتك هنا:", 
                                               value=st.session_state.notes_content, 
                                               height=400,
                                               placeholder="مثال: مراجعة فصل الكيمياء غداً...")
    if st.button("حفظ وتحديث 💾"):
        st.success("تم تثبيت الملاحظات بنجاح!")
        st.rerun()

# --- بقية التبويبات (بدون تغيير حرصاً على الكود الأصلي) ---
with tab_study:
    st.subheader("⏱️ مؤقت التركيز (بومودورو)")
    col_input1, col_input2 = st.columns(2)
    study_mins = col_input1.number_input("دقائق الدراسة:", min_value=1, max_value=120, value=25)
    break_mins = col_input2.number_input("دقائق الراحة:", min_value=1, max_value=30, value=5)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        placeholder = st.empty()
        progress_bar = st.progress(0)
        mode = st.radio("اختر الوضع:", ["دراسة 📖", "راحة ☕"], horizontal=True)
        if st.button("ابدأ التوقيت الآن 🚀"):
            total_seconds = (study_mins if "دراسة" in mode else break_mins) * 60
            remaining = total_seconds
            while remaining > 0:
                mins, secs = divmod(remaining, 60)
                placeholder.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                progress_bar.progress(1 - (remaining / total_seconds))
                time.sleep(1)
                remaining -= 1
            st.balloons()
            st.success("انتهى الوقت!")
            placeholder.markdown(f'<div class="timer-display">00:00</div>', unsafe_allow_html=True)

with tab_full:
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
                if msg: st.info(msg)
    if st.button("🔄 تصفير التتبع لليوم الجديد"):
        for h in st.session_state.habits: h['status'] = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align:center; color:{clr};'><b>FIRAS SCHEDULER v2.4</b></div>", unsafe_allow_html=True)
