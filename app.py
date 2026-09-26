import os
import streamlit as st
from google import genai
from google.genai import types

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مساعد الذكاء الاصطناعي",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. حقن CSS للتنسيق بدون أخطاء SyntaxError
st.markdown("""
    <style>
    /* إعدادات الاتجاه العربي والتصميم الداكن */
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* خلفية التطبيق */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* تنسيق مربع الحوار والرسائل */
    .stChatMessage {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* إخفاء القوائم والترويسات غير الضرورية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. الشريط الجانبي للإعدادات
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.markdown("---")
    
    # الحصول على المفتاح من secrets أو إدخاله يدويًا
    api_key_input = st.text_input(
        "أدخل مفتاح Gemini API:",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="يمكنك الحصول على المفتاح من Google AI Studio"
    )
    
    model_choice = st.selectbox(
        "اختر النموذج:",
        ["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0
    )
    
    if st.button("تصفير المحادثة 🗑️"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 مساعد الذكاء الاصطناعي")
st.caption("مرحبًا بك! اسألني أي سؤال باللغة العربية أو باللغات البرمجية.")

# 4. تهيئة سجل المحادثة في الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. استقبال مدخلات المستخدم ومعالجتها
user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    # التحقق من وجود مفتاح الـ API
    if not api_key_input:
        st.error("الرجاء إدخال مفتاح Gemini API في الشريط الجانبي للبدء.")
    else:
        # عرض رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # توليد الرد من الذكاء الاصطناعي
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                try:
                    # إنشاء العميل باستخدام المكتبة الرسمية الجديدة
                    client = genai.Client(api_key=api_key_input)
                    
                    # إرسال الطلب للنموذج
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=user_input
                    )
                    
                    bot_reply = response.text
                    st.markdown(bot_reply)
                    
                    # حفظ رد البوت في الجلسة
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {str(e)}")
