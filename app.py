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
    .note-card {{ border-right: 4px solid {clr}; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 10px; }}
    .stButton>button {{ background-color: {clr} !important; color: #000000 !important; font-weight: bold !important; border-radius: 10px !important; border: none !important; width: 100%; }}
    .timer-display {{ font-size: 4rem; font-weight: bold; color: {clr}; text-align: center; font-family: monospace; text-shadow: 0 0 20px {clr}55; }}
</style>
""", unsafe_allow_html=True)

# 5. تهيئة مخزن البيانات
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []
if 'notes' not in st.session_state: st.session_state.notes = []

def get_habit_message(habit):
    if habit['status'] is True:
        return "✅ بطل! استمر في هذا الإنجاز. 🌟" if habit['type'] == 'good' else "⚠️ لا بأس، حاول غداً أن تكون أقوى. 👊"
    elif habit['status'] is False:
        return "💡 تذكر لماذا بدأت، حاول الآن! 🔥" if habit['type'] == 'good' else "✨ إنجاز عظيم! انتصرت على نفسك اليوم. 🌟"
    return None

st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:{clr}; letter-spacing: 2px;'>CREATED BY: FIRAS</p>", unsafe_allow_html=True)

# 6. نظام التبويبات
tab_home, tab_study, tab_full, tab_habits, tab_notes = st.tabs(["🏠 الرئيسية", "📚 الدراسة", "📑 الجدول", "🎯 العادات", "📝 الملاحظات"])

# --- التبويب الأول: الرئيسية (تم تحديثه لإظهار الملاحظات المثبتة) ---
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
        else: st.info("لا توجد مهام.")

    with col_side:
        # قسم الملاحظات المثبتة في الرئيسية
        st.subheader("📌 ملاحظات مثبتة")
        pinned_notes = [n for n in st.session_state.notes if n.get('pinned', False)]
        if pinned_notes:
            for n in pinned_notes:
                st.markdown(f"""<div style="background:{clr}22; border-right:4px solid {clr}; padding:10px; border-radius:8px; margin-bottom:5px; font-size:0.9rem;">📌 {n['text']}</div>""", unsafe_allow_html=True)
        else:
            st.write("<small>لا توجد ملاحظات مثبتة</small>", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("🎯 العادات")
        if st.session_state.habits:
            for habit in st.session_state.habits[:2]:
                msg = get_habit_message(habit)
                card_border = clr if habit['type'] == 'good' else "#ff4b4b"
                st.markdown(f'<div style="border:1px solid {card_border}66; padding:10px; border-radius:10px; background:rgba(0,0,0,0.3); margin-bottom:5px;"><b style="color:{card_border};">{habit["name"]}</b><br><small>{msg if msg else "⏳"}</small></div>', unsafe_allow_html=True)

# --- تبويب الدراسة (Pomodoro) ---
with tab_study:
    st.subheader("⏱️ مؤقت التركيز")
    col_in1, col_in2 = st.columns(2)
    s_mins = col_in1.number_input("دراسة:", 1, 120, 25)
    b_mins = col_in2.number_input("راحة:", 1, 30, 5)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        ph = st.empty()
        pb = st.progress(0)
        mode = st.radio("الوضع:", ["دراسة 📖", "راحة ☕"], horizontal=True)
        if st.button("ابدأ التوقيت 🚀"):
            total = (s_mins if "دراسة" in mode else b_mins) * 60
            curr = total
            while curr > 0:
                m, s = divmod(curr, 60)
                ph.markdown(f'<div class="timer-display">{m:02d}:{s:02d}</div>', unsafe_allow_html=True)
                pb.progress(1 - (curr / total))
                time.sleep(1)
                curr -= 1
            st.balloons()

# --- تبويب الجدول والصلوات ---
with tab_full:
    city = st.text_input("📍 المدينة:", "Muscat")
    @st.cache_data(ttl=3600)
    def get_p_times(c):
        try: return requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={c}&country=Oman&method=4").json()['data']['timings']
        except: return None
    t_data = get_p_times(city)
    if t_data:
        p_names = {"Fajr":"الفجر","Dhuhr":"الظهر","Asr":"العصر","Maghrib":"المغرب","Isha":"العشاء"}
        cols = st.columns(5)
        for i, (k, v) in enumerate(p_names.items()):
            azan = dt.strptime(t_data[k], "%H:%M")
            iqama = azan + timedelta(minutes=iqama_offset)
            cols[i].markdown(f"""<div class="p-box"><b style="color:{clr};">{v}</b><br>{azan.strftime("%I:%M")}<br><small>إقامة: {iqama.strftime("%I:%M")}</small></div>""", unsafe_allow_html=True)
    
    with st.expander("➕ إضافة مهمة"):
        with st.form("t_form", clear_on_submit=True):
            f1, f2 = st.columns(2)
            c_cat = f1.text_input("الفئة:", "عام")
            c_name = f2.text_input("المهمة:")
            t_s = f1.time_input("البداية")
            t_e = f2.time_input("النهاية")
            if st.form_submit_button("إضافة ✅") and c_name:
                st.session_state.tk.append({"id": str(dt.now().timestamp()), "category": c_cat, "name": c_name, "start": t_s.strftime("%I:%M %p"), "end": t_e.strftime("%I:%M %p"), "raw_time": t_s.strftime("%H:%M")})
                st.rerun()

# --- تبويب متتبع العادات ---
with tab_habits:
    st.subheader("🎯 متتبع العادات")
    with st.expander("➕ أضف عادة"):
        with st.form("h_form", clear_on_submit=True):
            h_n = st.text_input("الاسم:")
            h_t = st.radio("النوع:", ["جيدة ✨", "سيئة ⚠️"], horizontal=True)
            if st.form_submit_button("إضافة"):
                st.session_state.habits.append({"name": h_n, "type": "good" if "جيدة" in h_t else "bad", "status": None})
                st.rerun()
    for i, h in enumerate(st.session_state.habits):
        c_c = clr if h['type'] == 'good' else "#ff4b4b"
        st.markdown(f'<div class="note-card" style="border-right-color:{c_c}">{h["name"]}</div>', unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        if b1.button("✅", key=f"y{i}"): h['status']=True; st.rerun()
        if b2.button("❌", key=f"n{i}"): h['status']=False; st.rerun()
        if b3.button("🗑️", key=f"d{i}"): st.session_state.habits.pop(i); st.rerun()

# --- التبويب الجديد: الملاحظات ---
with tab_notes:
    st.subheader("📝 الملاحظات والخواطر")
    with st.form("note_form", clear_on_submit=True):
        note_text = st.text_area("اكتب ملاحظتك هنا:")
        is_pinned = st.checkbox("تثبيت في الرئيسية 📌")
        if st.form_submit_button("حفظ الملاحظة") and note_text:
            st.session_state.notes.append({"id": time.time(), "text": note_text, "pinned": is_pinned})
            st.rerun()
    
    st.divider()
    for i, n in enumerate(st.session_state.notes):
        with st.container():
            col_n1, col_n2 = st.columns([4, 1])
            with col_n1:
                st.markdown(f"""<div class="note-card">{'📌 ' if n['pinned'] else ''}{n['text']}</div>""", unsafe_allow_html=True)
            with col_n2:
                if st.button("حذف", key=f"del_n_{i}"):
                    st.session_state.notes.pop(i)
                    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align:center; color:{clr};'><b>FIRAS SCHEDULER v2.4</b></div>", unsafe_allow_html=True)
