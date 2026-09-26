import os
import json
import requests
import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مساعد الذكاء الاصطناعي السريع",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تنسيق الواجهة بلغة CSS
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

# 3. جلب مفتاح الـ API تلقائياً
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
        help="ضع مفتاح API هنا أو أضفه في Secrets"
    )
    
    # نماذج فائقة السرعة
    model_choice = st.selectbox(
        "اختر النموذج السريع:",
        ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-2.0-flash-exp"],
        index=0
    )
    
    if st.button("تصفير المحادثة 🗑️"):
        st.session_state.messages = []
        st.rerun()

# 5. الواجهة الرئيسية
st.title("⚡ مساعد الذكاء الاصطناعي السريع")
st.caption("مرحبًا بك! اسألني أي سؤال وسيتم توليد الإجابة فوراً وبسرعة فائقة.")

# 6. تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. استقبال مدخلات المستخدم ومعالجتها بأسلوب البث المباشر (Streaming)
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

        # توليد الرد السريع عبر البث المباشر (streamGenerateContent)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # استخدام رابط البث المباشر المباشر لتسريع النتيجة
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_choice}:streamGenerateContent?alt=sse&key={active_key}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [
                        {
                            "parts": [{"text": user_input}]
                        }
                    ]
                }

                response = requests.post(url, headers=headers, json=payload, stream=True)

                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            line_text = line.decode("utf-8")
                            if line_text.startswith("data: "):
                                json_str = line_text[6:]
                                try:
                                    data = json.loads(json_str)
                                    text_chunk = data["candidates"][0]["content"]["parts"][0].get("text", "")
                                    full_response += text_chunk
                                    # تحديث النص حياً فور وصول الحروف
                                    message_placeholder.markdown(full_response + " ▌")
                                except Exception:
                                    continue
                    # إزالة مؤشر الكتابة عند الانتهاء
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    res_data = response.json()
                    error_msg = res_data.get("error", {}).get("message", "حدث خطأ من السيرفر، يرجى إعادة المحاولة.")
                    st.error(f"تنبيه: {error_msg}")

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {str(e)}")
