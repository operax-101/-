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
clr = st.sidebar.color_picker("اختر لون التميز (Accent Color):", "#D4AF37")
bg_key = st.sidebar.selectbox("اختر تدرج الخلفية:", list(gradients.keys()))
selected_gradient = gradients[bg_key]

# 4. التصميم المخصص (CSS)
st.markdown(f"""
<style>
    .stApp {{ background: {selected_gradient} !important; background-attachment: fixed !important; }}
    h1, h2, h3 {{ color: {clr} !important; text-align: center; }}
    .habit-card {{ background: rgba(0, 0, 0, 0.4); border-radius: 15px; border: 2px solid {clr}; margin-bottom: 20px; overflow: hidden; }}
    .habit-header {{ background: {clr}; padding: 10px; color: black !important; text-align: center; font-weight: bold; font-size: 1.2rem; }}
    .habit-body {{ padding: 20px; }}
    .stButton>button {{ background-color: {clr} !important; color: black !important; font-weight: bold; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

# 5. منطق تحليل العادات الذكي
def analyze_habit(name):
    # كلمات مفتاحية ذكية
    bad_keywords = ['سهر', 'تدخين', 'اكل سريع', 'غضب', 'تأجيل', 'تسويف', 'جوال', 'تلفون', 'حلويات', 'سكر', 'كسل']
    
    # تحليل هل هي عادة سيئة؟
    is_bad = any(word in name.lower() for word in bad_keywords)
    
    if is_bad:
        return {
            "type": "سيئة 👎",
            "on_success": f"انتصار كبير! تجنب ' {name} ' يقوي إرادتك ويحسن صحتك.",
            "on_fail": f"تذكر أن ' {name} ' يؤثر عليك سلباً. حاول غداً أن تقلل منها تدريجياً."
        }
    else:
        return {
            "type": "حسنة 👍",
            "on_success": f"استمر يا بطل! ' {name} ' هي طريقك للتميز والنجاح.",
            "on_fail": f"لا بأس، العثرات طبيعية. حاول القيام بـ ' {name} ' ولو بشكل بسيط الآن!"
        }

# --- إدارة الحالة وتجنب الـ KeyError ---
if 'tk' not in st.session_state: st.session_state.tk = []
if 'habits' not in st.session_state: st.session_state.habits = []

# حماية من البيانات القديمة (تصفير العادات إذا كانت بتنسيق قديم)
if st.session_state.habits and "info" not in st.session_state.habits[0]:
    st.session_state.habits = []
    st.rerun()

# --- واجهة المستخدم ---
st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:{clr};'>تطوير: FIRAS</p>", unsafe_allow_html=True)

tab_home, tab_full, tab_habits = st.tabs(["🏠 الرئيسية", "📑 الجدول والصلوات", "🚀 متتبع العادات الذكي"])

with tab_habits:
    st.subheader("🤖 محلل العادات بالذكاء الاصطناعي")
    
    with st.expander("➕ أضف عادة جديدة (اكتب اسمها فقط)"):
        with st.form("h_form", clear_on_submit=True):
            h_input = st.text_input("مثلاً: سهر، صلاة، برمجة، تدخين..")
            if st.form_submit_button("إضافة وتحليل ✨"):
                if h_input:
                    analysis = analyze_habit(h_input)
                    st.session_state.habits.append({
                        "id": str(dt.now().timestamp()),
                        "name": h_input,
                        "info": analysis, # هنا يتم تخزين التحليل
                        "status": None
                    })
                    st.rerun()

    if st.session_state.habits:
        for i, habit in enumerate(st.session_state.habits):
            st.markdown(f"""
                <div class="habit-card">
                    <div class="habit-header">{habit['name']} | نوعها: {habit['info']['type']}</div>
                    <div class="habit-body">
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            if c1.button("✅ تم / تجنبتها", key=f"y_{habit['id']}"): 
                habit['status'] = True
            if c2.button("❌ فشلت / وقعت فيها", key=f"n_{habit['id']}"): 
                habit['status'] = False
            
            if habit['status'] is True:
                st.success(habit['info']['on_success'])
            elif habit['status'] is False:
                st.warning(habit['info']['on_fail'])
            
            if st.button("🗑️ حذف العادة", key=f"d_{habit['id']}"):
                st.session_state.habits.pop(i)
                st.rerun()
                
            st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.info("اكتب أي عادة وسأقوم بتحليلها لك فوراً!")

# (باقي كود الجدولة والصلوات يوضع هنا كما هو في النسخ السابقة)
