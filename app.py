import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
import requests
import time
from streamlit_drawable_canvas import st_canvas

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
    .note-card {{ background: rgba(212, 175, 55, 0.1); border: 1px dashed {clr}; padding: 15px; border-radius: 10px; margin-bottom: 20px; }}
    .stButton>button {{ background-color: {clr} !important; color: #000000 !important; font-weight: bold !important; border-radius: 10px !important; border: none !important; width: 100%; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; justify-content: center; }}
    .stTabs [data-baseweb="tab"] {{ background-color: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px 20px; color: white; }}
    .stTabs [aria-selected="true"] {{ background-color: {clr}33 !important; border-bottom: 2px solid {clr} !important; }}
</style>
""", unsafe_allow_html=True)

# 5. تهيئة مخزن البيانات
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []
if 'pinned_note' not in st.session_state: st.session_state.pinned_note = ""

# العنوان الرئيسي
st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:{clr}; letter-spacing: 2px;'>CREATED BY: FIRAS</p>", unsafe_allow_html=True)

# 6. نظام التبويبات
tab_home, tab_study, tab_notes, tab_full, tab_habits = st.tabs(["🏠 الرئيسية", "📚 جلسة الدراسة", "📝 الملاحظات والبورد", "📑 الجدول والصلوات", "🎯 متتبع العادات"])

# --- التبويب الأول: الرئيسية ---
with tab_home:
    # عرض الملاحظة المثبتة في الأعلى إذا وجدت
    if st.session_state.pinned_note:
        st.markdown(f"""
        <div class="note-card">
            <h4 style="margin:0; color:{clr}; text-align:right;">📌 ملاحظة مثبتة</h4>
            <p style="color:white; font-size:1.1rem; text-align:right; white-space: pre-wrap;">{st.session_state.pinned_note}</p>
        </div>
        """, unsafe_allow_html=True)

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
        else: st.info("لا توجد مهام.")

    with col_habit_mini:
        st.subheader("🎯 أهم العادات")
        if st.session_state.habits:
            for habit in st.session_state.habits[:2]:
                card_border = clr if habit['type'] == 'good' else "#ff4b4b"
                st.markdown(f'<div style="border: 1px solid {card_border}66; padding: 12px; border-radius: 12px; background: rgba(0,0,0,0.3); margin-bottom: 10px; color:white;">{habit["name"]}</div>', unsafe_allow_html=True)

# --- التبويب الجديد: الملاحظات والبورد ---
with tab_notes:
    st.subheader("📝 مساحة الأفكار")
    col_n1, col_n2 = st.columns([1, 1])
    
    with col_n1:
        note_input = st.text_area("اكتب ملاحظة جديدة:", placeholder="سجل أفكارك هنا...", height=200)
        c_p1, c_p2 = st.columns(2)
        if c_p1.button("📌 تثبيت في الرئيسية"):
            st.session_state.pinned_note = note_input
            st.success("تم تثبيت الملاحظة!")
            st.rerun()
        if c_p2.button("🗑️ مسح المثبت"):
            st.session_state.pinned_note = ""
            st.rerun()

    with col_n2:
        st.markdown(f"<b style='color:{clr}'>🎨 لوحة الرسم السريع:</b>", unsafe_allow_html=True)
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=3,
            stroke_color=clr,
            background_color="#1a1a1a",
            height=200,
            drawing_mode="freedraw",
            key="canvas_notes",
        )
        st.caption("الرسم مخصص للعصف الذهني السريع.")

# --- التبويب الثاني: جلسة الدراسة ---
with tab_study:
    st.subheader("⏱️ مؤقت التركيز")
    col_in1, col_in2 = st.columns(2)
    study_mins = col_in1.number_input("دقائق الدراسة:", 1, 120, 25)
    break_mins = col_input2 = col_in2.number_input("دقائق الراحة:", 1, 30, 5)
    
    placeholder = st.empty()
    if st.button("ابدأ التوقيت 🚀"):
        total = study_mins * 60
        for r in range(total, -1, -1):
            m, s = divmod(r, 60)
            placeholder.markdown(f'<h1 style="font-size:4rem; text-align:center; color:{clr}">{m:02d}:{s:02d}</h1>', unsafe_allow_html=True)
            time.sleep(1)
        st.balloons()

# --- التبويب الثالث: الجدول والصلوات ---
with tab_full:
    city = st.text_input("📍 المدينة:", "Muscat")
    # ... (نفس كود جلب الصلاة السابق الخاص بك)
    st.info("قسم الصلوات والجدول التفصيلي متاح هنا.")

# --- التبويب الرابع: متتبع العادات ---
with tab_habits:
    st.subheader("🎯 عاداتك اليومية")
    # ... (نفس كود العادات السابق الخاص بك)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align:center; color:{clr};'><b>FIRAS SCHEDULER v2.5</b></div>", unsafe_allow_html=True)
