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

# 3. دالة صفحة تسجيل الدخول المعدلة
def login_page():
    # CSS لجعل العناصر في منتصف الشاشة تماماً وتنسيق الأزرار
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        }
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 70vh;
            text-align: center;
        }
        .login-box {
            background: rgba(255, 255, 255, 0.05);
            padding: 3rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            width: 100%;
            max-width: 450px;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            background-color: transparent !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            transition: 0.3s;
        }
        .stButton>button:hover {
            border-color: #D4AF37 !important;
            color: #D4AF37 !important;
            background: rgba(212, 175, 55, 0.1) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # إنشاء الحاوية المركزية
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom:0;'>🔐 تسجيل الدخول</h1>", unsafe_allow_html=True)
        st.markdown("<p style='opacity:0.8; margin-bottom:2rem;'>مرحباً بك في FIRAS SCHEDULER<br>يرجى اختيار وسيلة الدخول</p>", unsafe_allow_html=True)
        
        # أزرار تسجيل الدخول
        if st.button("Log in with Google 🌐"):
            st.session_state.logged_in = True
            st.session_state.user_type = "Google"
            st.rerun()

        st.write("") # مسافة صغيرة بين الأزرار

        if st.button("Log in with GitHub 🐙"):
            st.session_state.logged_in = True
            st.session_state.user_type = "GitHub"
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. دالة التطبيق الرئيسي (نفس كودك السابق)
def main_app():
    clr = st.sidebar.color_picker("اختر لون التميز (Accent Color):", "#D4AF37")
    bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
    selected_gradient = gradients[bg_key]

    st.sidebar.divider()
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    iqama_offset = st.sidebar.slider("دقائق الانتظار للإقامة:", 5, 30, 20)

    st.markdown(f"""
    <style>
        .stApp {{ background: {selected_gradient} !important; background-attachment: fixed !important; }}
        [data-testid="stSidebar"] {{ background-color: rgba(0,0,0,0.5) !important; backdrop-filter: blur(10px); }}
        h1, h2, h3 {{ color: {clr} !important; text-align: center; text-shadow: 2px 2px 10px rgba(0,0,0,0.7); }}
        .category-header {{ background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; border-right: 5px solid {clr}; margin-top: 20px; text-align: right; color: white; }}
        .p-box {{ border: 2px solid {clr}; padding: 10px; border-radius: 15px; text-align: center; background: rgba(0, 0, 0, 0.4); min-height: 120px; display: flex; flex-direction: column; justify-content: center; }}
    </style>
    """, unsafe_allow_html=True)

    st.title("📅 FIRAS SCHEDULER")
    st.markdown(f"<p style='text-align:center; font-size:1.1rem; color:{clr}; font-weight:bold;'>إعداد: FIRAS</p>", unsafe_allow_html=True)

    # ... باقي كود عرض أوقات الصلاة والمهام كما هو في النسخة السابقة ...
    st.info(f"مرحباً بك! أنت مسجل دخول عبر: {st.session_state.user_type}")

# --- التشغيل السليم ---
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
