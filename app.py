import os
import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والتصميم
st.set_page_config(
    page_title="مساعد الذكاء الاصطناعي",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تنسيق الواجهة بالـ CSS (محاذاة وتصميم داكن)
st.markdown("""
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stChatMessage {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. جلب المفتاح تلقائياً من Secrets أو البيئة
saved_key = ""
if "GEMINI_API_KEY" in st.secrets:
    saved_key = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
    saved_key = os.environ["GEMINI_API_KEY"]

# 4. الشريط الجانبي
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.markdown("---")
    
    api_key_input = st.text_input(
        "مفتاح Gemini API:",
        type="password",
        value=saved_key,
        help="ضع المفتاح هنا أو في Secrets"
    )
    
    if st.button("تصفير المحادثة 🗑️"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 مساعد الذكاء الاصطناعي")
st.caption("مرحبًا بك! اسألني أي سؤال وسيتم توليد الإجابة فوراً.")

# 5. تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. استقبال وتوليد الردود بسرعة
user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    active_key = api_key_input or saved_key
    
    if not active_key:
        st.error("يرجى إدخال مفتاح Gemini API في الشريط الجانبي أو إضافته إلى Secrets للبدء.")
    else:
        # عرض رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # توليد الرد السريع عبر المكتبة الرسمية
        with st.chat_message("assistant"):
            try:
                genai.configure(api_key=active_key)
                # استخدام النموذج الرسمي الشغال والسريع
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # كتابة البث المباشر للإجابة حياً
                response = model.generate_content(user_input, stream=True)
                
                def stream_generator():
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text

                bot_reply = st.write_stream(stream_generator)
                
                # حفظ الرد
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
