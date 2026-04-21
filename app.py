import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="FIRAS SCHEDULER", layout="wide", page_icon="📅")

# --- إدارة حالة تسجيل الدخول ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 2. قائمة التدرجات
gradients = {
    "تدرج المحيط (Deep Ocean)": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
    "تدرج الغسق (Sunset Dusk)": "linear-gradient(135deg, #2c3e50 0%, #000000 100%)",
    "تدرج ملكي (Royal Gold)": "linear-gradient(135deg, #1a1a1a 0%, #434343 100%)",
    "تدرج الأرجواني (Midnight)": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
    "تدرج احترافي (Modern Grey)": "linear-gradient(135deg, #141e30 0%, #243b55 100%)"
}

# 3. دالة صفحة تسجيل الدخول
def login_page():
    st.markdown("""
    <style>
        .login-box {
            background: rgba(255, 255, 255, 0.05);
            padding: 50px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            backdrop-filter: blur(10px);
            max-width: 500px;
            margin: auto;
        }
        .stButton>button { width: 100% !important; height: 50px !important; }
    </style>
    """, unsafe_allow_html=True)

    st.write("#") # مسافة
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("🔐 تسجيل الدخول")
    st.write("مرحباً بك في FIRAS SCHEDULER، يرجى اختيار وسيلة الدخول")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Log in with Google 🌐"):
            # هنا يمكنك وضع رابط OAuth الفعلي
            st.session_state.logged_in = True
            st.session_state.user_type = "Google"
            st.rerun()

    with col2:
        if st.button("Log in with GitHub 🐙"):
            # هنا يمكنك وضع رابط OAuth الفعلي
            st.session_state.logged_in = True
            st.session_state.user_type = "GitHub"
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# 4. دالة التطبيق الرئيسي
def main_app():
    # استكمال إعدادات الثيم (التي كانت في كودك الأصلي)
    clr = st.sidebar.color_picker("اختر لون التميز (Accent Color):", "#D4AF37")
    bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
    selected_gradient = gradients[bg_key]

    st.sidebar.divider()
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    iqama_offset = st.sidebar.slider("دقائق الانتظار للإقامة:", 5, 30, 20)

    # تطبيق الـ CSS
    st.markdown(f"""
    <style>
        .stApp {{ background: {selected_gradient} !important; background-attachment: fixed !important; }}
        [data-testid="stSidebar"] {{ background-color: rgba(0,0,0,0.5) !important; backdrop-filter: blur(10px); }}
        h1, h2, h3 {{ color: {clr} !important; text-align: center; text-shadow: 2px 2px 10px rgba(0,0,0,0.7); }}
        .category-header {{ background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; border-right: 5px solid {clr}; margin-top: 20px; text-align: right; color: white; }}
        .p-box {{ border: 2px solid {clr}; padding: 10px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); min-height: 120px; display: flex; flex-direction: column; justify-content: center; }}
        .iqama-text {{ font-size: 0.85rem; color: #ffffff !important; font-weight: bold; margin-top: 5px; opacity: 0.9; }}
    </style>
    """, unsafe_allow_html=True)

    st.title("📅 FIRAS SCHEDULER")
    st.markdown(f"<p style='text-align:center; font-size:1.1rem; color:white;'>مرحباً بك، لقد سجلت الدخول عبر {st.session_state.user_type}</p>", unsafe_allow_html=True)

    # (بقية الكود الخاص بك لجلب أوقات الصلاة والمهام...)
    city = st.text_input("📍 أدخل مدينتك لجلب الأوقات الرسمية:", "Muscat")
    
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
            azan_dt = dt.strptime(t[k], "%H:%M")
            azan_str = azan_dt.strftime("%I:%M %p")
            iqama_dt = azan_dt + timedelta(minutes=iqama_offset)
            iqama_str = iqama_dt.strftime("%I:%M %p")
            cols[i].markdown(f'<div class="p-box"><b style="color:{clr}; font-size:1.2rem;">{v}</b><br><span style="color:white; font-size:1rem;">📢 {azan_str}</span><div class="iqama-text">⏳ الإقامة: {iqama_str}</div></div>', unsafe_allow_html=True)

    st.divider()
    
    # إدارة المهام
    if 'tk' not in st.session_state: st.session_state.tk = []
    
    st.subheader("📝 إضافة مهمة جديدة")
    with st.form("task_form", clear_on_submit=True):
        category = st.text_input("العنوان الرئيسي:", "عام")
        task_name = st.text_input("اسم المهمة:")
        c1, c2 = st.columns(2)
        t_start = c1.time_input("البداية")
        t_end = c2.time_input("النهاية")
        if st.form_submit_button("إضافة ✨") and task_name:
            st.session_state.tk.append({"id": str(dt.now().timestamp()), "category": category if category else "عام", "name": task_name, "start": t_start.strftime("%I:%M %p"), "end": t_end.strftime("%I:%M %p"), "raw_time": t_start.strftime("%H:%M")})
            st.rerun()

    # عرض المهام
    if st.session_state.tk:
        categories = sorted(list(set([t['category'] for t in st.session_state.tk])))
        for cat in categories:
            st.markdown(f'<div class="category-header"><h3>📁 {cat}</h3></div>', unsafe_allow_html=True)
            cat_tasks = sorted([t for t in st.session_state.tk if t['category'] == cat], key=lambda x: x['raw_time'])
            cols = st.columns(4)
            for i, task in enumerate(cat_tasks):
                with cols[i % 4]:
                    st.markdown(f'<div class="p-box" style="margin-top:10px;"><b style="color:{clr};">{task["name"]}</b><br><span style="color:white; font-size:0.8rem;">{task["start"]} - {task["end"]}</span></div>', unsafe_allow_html=True)
                    if st.button("❌ حذف", key=f"del_{task['id']}"):
                        st.session_state.tk = [t for t in st.session_state.tk if t['id'] != task['id']]
                        st.rerun()

# --- المنطق الرئيسي للتشغيل ---
if not st.session_state.logged_in:
    # تطبيق خلفية افتراضية لصفحة الدخول
    st.markdown(f"<style>.stApp {{ background: {gradients['تدرج المحيط (Deep Ocean)']} !important; }}</style>", unsafe_allow_html=True)
    login_page()
else:
    main_app()
