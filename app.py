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

# 5. منطق تحليل العادات (الذكاء الاصطناعي المبسط)
def analyze_habit(name):
    bad_keywords = ['سهر', 'تدخين', 'اكل سريع', 'غضب', 'تأجيل', 'تسويف', 'جوال', 'تلفون', 'حلويات', 'سكر']
    good_keywords = ['صلاة', 'رياضة', 'قراءة', 'ماء', 'تعلم', 'برمجة', 'استيقاظ', 'مذاكرة', 'تطوير', 'نوم مبكر']
    
    # التحليل
    is_bad = any(word in name.lower() for word in bad_keywords)
    
    # نصائح وتشيجهات مخصصة
    if is_bad:
        return {
            "type": "سيئة 👎",
            "on_success": "انتصار كبير! تجنب هذه العادة يقوي إرادتك ويحسن صحتك النفسية.",
            "on_fail": f"تذكر أن ' {name} ' يستنزف طاقتك. حاول غداً تقليل الوقت الذي تقضيه فيها بمقدار 10 دقائق فقط كبداية."
        }
    else:
        return {
            "type": "حسنة 👍",
            "on_success": f"استمر! ' {name} ' هي استثمار في نفسك، والنتائج ستظهر قريباً جداً.",
            "on_fail": "لا بأس بالعثرات. السر في الاستمرارية وليس الكمال. حاول القيام بها ولو لدقيقة واحدة الآن!"
        }

# --- إدارة الحالة ---
if 'habits' not in st.session_state: st.session_state.habits = []

# --- واجهة المستخدم ---
st.title("📅 FIRAS SCHEDULER")
st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:{clr};'>تطوير: FIRAS</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏠 الرئيسية", "📑 الجدول", "🚀 متتبع العادات الذكي"])

with tab3:
    st.subheader("🤖 محلل العادات الذكي")
    with st.expander("➕ أضف عادة (سيقوم الذكاء الاصطناعي بتحليلها)"):
        with st.form("h_form", clear_on_submit=True):
            h_input = st.text_input("ما هي العادة التي تريد تتبعها؟")
            if st.form_submit_button("إضافة وتحليل"):
                if h_input:
                    analysis = analyze_habit(h_input)
                    st.session_state.habits.append({
                        "id": str(dt.now().timestamp()),
                        "name": h_input,
                        "info": analysis,
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
            if c1.button("✅ تم بنجاح", key=f"y_{habit['id']}"): habit['status'] = True
            if c2.button("❌ لم أنجح", key=f"n_{habit['id']}"): habit['status'] = False
            
            if habit['status'] is True:
                st.success(habit['info']['on_success'])
            elif habit['status'] is False:
                st.warning(habit['info']['on_fail'])
            
            if st.button("🗑️ حذف", key=f"d_{habit['id']}"):
                st.session_state.habits.pop(i); st.rerun()
                
            st.markdown('</div></div>', unsafe_allow_html=True)
    else:
        st.info("أضف عادة مثل 'قراءة' أو 'سهر' لترى تحليل الذكاء الاصطناعي.")
