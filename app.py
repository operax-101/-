import os
import requests
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مساعد الذكاء الاصطناعي",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تنسيق الواجهة بلغة CSS
st.markdown("""
    <style>
    /* إعدادات اتجاه النص والتصميم */
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

# 3. جلب مفتاح الـ API تلقائياً من Secrets أو البيئة
API_KEY = ""
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
    API_KEY = os.environ["GEMINI_API_KEY"]

# 4. الشريط الجانبي (للخيارات المتبقية فقط)
with st.sidebar:
    st.title("⚙️ الخيارات")
    st.markdown("---")
    
    model_choice = st.selectbox(
        "اختر النموذج:",
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )
    
    if st.button("تصفير المحادثة 🗑️"):
        st.session_state.messages = []
        st.rerun()

# 5. واجهة التطبيق الرئيسية
st.title("🤖 مساعد الذكاء الاصطناعي")
st.caption("مرحبًا بك! اسألني أي سؤال باللغة العربية أو بأسئلة البرمجة.")

# 6. تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. استقبال مدخلات المستخدم ومعالجتها
user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    if not API_KEY:
        st.error("مفتاح API غير معرف في Streamlit Secrets. يرجى إضافة GEMINI_API_KEY في إعدادات Secrets لموقعك.")
    else:
        # عرض رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # توليد الرد من الذكاء الاصطناعي عبر طلب REST API مباشر
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_choice}:generateContent?key={API_KEY}"
                    headers = {"Content-Type": "application/json"}
                    payload = {
                        "contents": [
                            {
                                "parts": [{"text": user_input}]
                            }
                        ]
                    }

                    response = requests.post(url, headers=headers, json=payload)
                    res_data = response.json()

                    if response.status_code == 200:
                        bot_reply = res_data["candidates"][0]["content"]["parts"][0]["text"]
                        st.markdown(bot_reply)
                        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    else:
                        error_msg = res_data.get("error", {}).get("message", "حدث خطأ غير معروف")
                        st.error(f"خطأ من الـ API: {error_msg}")

                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {str(e)}")
