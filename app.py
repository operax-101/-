import streamlit as st
import pandas as pd
from datetime import datetime as dt
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منظم فراس - النسخة المتقدمة", layout="wide", page_icon="📅")

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

# 4. التصميم المخصص (CSS)
st.markdown(f"""
<style>
    .stApp {{ background: {selected_gradient} !important; background-attachment: fixed !important; }}
    [data-testid="stSidebar"] {{ background-color: rgba(0,0,0,0.5) !important; backdrop-filter: blur(10px); }}
    h1, h2, h3 {{ color: {clr} !important; text-align: center; text-shadow: 2px 2px 10px rgba(0,0,0,0.7); }}
    .category-header {{ background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; border-right: 5px solid {clr}; margin-top: 20px; text-align: right; color: white; }}
    .p-box {{ border: 2px solid {clr}; padding: 15px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); min-height: 80px; display: flex; flex-direction: column; justify-content: center; }}
    .stButton>button {{ background-color: {clr} !important; color: #000000 !important; font-weight: 900 !important; border-radius: 12px !important; width: 100%; }}
</style>
""", unsafe_allow_html=True)

# 5. الواجهة
st.title("📅 FERAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.4rem; color:{clr}; font-weight:bold;'>إبداع: فراس حمد المعمري</p>", unsafe_allow_html=True)

# 6. أوقات الصلاة
city = st.text_input("📍 اكتب المدينة هنا:", "Muscat")
@st.cache_data(ttl=3600)
def get_p(c):
    try:
        r = requests.get(f"http://api.aladhan.com/v1/timingsByCity?city={c}&country=Oman&method=4").json()
        return r['data']['timings']
    except: return None

t = get_p(city)
if t:
    cols = st.columns(5)
    p_names = {"Fajr":"الفجر","Dhuhr":"الظهر","Asr":"العصر","Maghrib":"المغرب","Isha":"العشاء"}
    for i, (k, v) in enumerate(p_names.items()):
        time_12 = dt.strptime(t[k], "%H:%M").strftime("%I:%M %p")
        cols[i].markdown(f'<div class="p-box"><b style="color:{clr};">{v}</b><br>{time_12}</div>', unsafe_allow_html=True)

st.divider()

# 7. إدارة المهام والمجموعات
if 'tk' not in st.session_state:
    st.session_state.tk = []

# --- كود الحماية المطور (تنظيف البيانات القديمة التي تسبب KeyError) ---
if st.session_state.tk:
    if not all("category" in task for task in st.session_state.tk):
        st.session_state.tk = []
        st.rerun()

st.subheader("📝 إضافة مهمة جديدة تحت عنوان رئيسي")
with st.form("task_form", clear_on_submit=True):
    category = st.text_input("العنوان الرئيسي (مثلاً: المذاكرة، الألعاب):", "عام")
    task_name = st.text_input("اسم المهمة:")
    c1, c2 = st.columns(2)
    t_start = c1.time_input("البداية")
    t_end = c2.time_input("النهاية")
    
    if st.form_submit_button("إضافة للمجموعة ✨") and task_name:
        st.session_state.tk.append({
            "id": str(dt.now().timestamp()), 
            "category": category if category else "عام",
            "name": task_name,
            "start": t_start.strftime("%I:%M %p"),
            "end": t_end.strftime("%I:%M %p"),
            "raw_time": t_start.strftime("%H:%M") 
        })
        st.rerun()

# 8. عرض الجدول بنظام المجموعات والبطاقات
if st.session_state.tk:
    # استخراج العناوين الفريدة
    categories = sorted(list(set([t['category'] for t in st.session_state.tk])))
    
    for cat in categories:
        st.markdown(f'<div class="category-header"><h3>📁 {cat}</h3></div>', unsafe_allow_html=True)
        
        cat_tasks = sorted([t for t in st.session_state.tk if t['category'] == cat], key=lambda x: x['raw_time'])
        
        n_cols = 4
        for i in range(0, len(cat_tasks), n_cols):
            batch = cat_tasks[i:i + n_cols]
            cols = st.columns(n_cols)
            for j, task in enumerate(batch):
                with cols[j]:
                    st.markdown(f"""
                    <div class="p-box" style="margin-top: 10px; margin-bottom: 5px;">
                        <b style="color:{clr}; font-size: 1.1rem;">{task['name']}</b>
                        <span style="font-size: 0.85rem; opacity: 0.9;">{task['start']} - {task['end']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("❌ حذف", key=f"btn_{task['id']}", use_container_width=True):
                        st.session_state.tk = [t for t in st.session_state.tk if t['id'] != task['id']]
                        st.rerun()
    
    st.write("---")
    if st.button("🗑️ مسح جميع العناوين والمهام"):
        st.session_state.tk = []
        st.rerun()
else:
    st.info("الجدول فارغ. ابدأ بكتابة عنوان رئيسي ثم أضف المهام تحته!")

st.sidebar.markdown("---")
st.sidebar.write(f"المبرمج: **فراس حمد المعمري**")
