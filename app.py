import os
import json
import requests
import streamlit as st

# 1. إعدادات الصفحة والتصميم
st.set_page_config(
    page_title="Vita - مساعد الذكاء الاصطناعي",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تنسيق الواجهة بالـ CSS (محاذاة وضبط خلفية الشريط الجانبي)
st.markdown("""
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* خلفية التطبيق الأساسية */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* تصميم وإبراز الشريط الجانبي لتفادي الشفافية */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-left: 1px solid #334155 !important;
    }
    
    /* تنسيق فقاعات المحادثة */
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

# 3. جلب المفتاح تلقائياً من Secrets أو البيئة الخاصة بالمالك
active_key = ""
if "GEMINI_API_KEY" in st.secrets:
    active_key = st.secrets["GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in os.environ:
    active_key = os.environ["GEMINI_API_KEY"]

# 4. الشريط الجانبي
with st.sidebar:
    st.title("⚙️ الخيارات")
    st.markdown("---")
    
    model_choice = "gemini-3.8-flash"
    
    st.info("🤖 **المساعد:** Vita")
    
    if st.button("تصفير المحادثة 🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# الواجهة الرئيسية
st.title("🤖 Vita - مساعد الذكاء الاصطناعي")
st.caption("مرحبًا بك! أنا Vita، مساعدك الذكي. اسألني أي سؤال وسيتم إجابتك فوراً.")

# 5. تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. استقبال وتوليد الردود باسم Vita
user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    if not active_key:
        st.error("لم يتم العثور على مفتاح API. يرجى إضافة GEMINI_API_KEY في قسم Secrets الخاص بالمشروع.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_choice}:streamGenerateContent?alt=sse&key={active_key}"
                headers = {"Content-Type": "application/json"}
                
                # توجيه النظام لتعريف المساعد باسم Vita
                payload = {
                    "systemInstruction": {
                        "parts": [
                            {"text": "اسمك هو Vita. أنت مساعد ذكاء اصطناعي ذكي ولطيف ومطور بواسطة تطبيق Vita. إذا سألك أحد عن اسمك أو من أنت، يجب أن تجيب دائماً بأن اسمك Vita."}
                        ]
                    },
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
                                    message_placeholder.markdown(full_response + " ▌")
                                except Exception:
                                    continue
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    res_data = response.json()
                    error_msg = res_data.get("error", {}).get("message", "حدث خطأ غير معروف")
                    st.error(f"خطأ: {error_msg}")

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {str(e)}")
