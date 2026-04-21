# --- إضافة هذه الأسطر في بداية الكود لتهيئة مخزن العادات ---
if 'habits' not in st.session_state:
    st.session_state.habits = []

# --- تحديث نظام التبويبات ليشمل المتتبع ---
tab_home, tab_full, tab_habits = st.tabs(["🏠 الرئيسية", "📑 إدارة الجدول", "🎯 متتبع العادات"])

with tab_habits:
    st.subheader("🚀 تحدي العادات اليومي")
    
    # 1. نموذج إضافة عادة جديدة
    with st.expander("➕ أضف عادة جديدة"):
        with st.form("habit_form"):
            h_name = st.text_input("اسم العادة (مثلاً: القراءة، التدخين، الرياضة):")
            h_type = st.radio("نوع العادة:", ["جيدة ✨", "سيئة ⚠️"], horizontal=True)
            if st.form_submit_button("إضافة"):
                if h_name:
                    st.session_state.habits.append({
                        "name": h_name,
                        "type": "good" if "جيدة" in h_type else "bad",
                        "status": None  # None = لم يتم الاختيار بعد
                    })
                    st.rerun()

    st.divider()

    # 2. عرض العادات للتقييم اليومي
    if st.session_state.habits:
        cols = st.columns(2)
        for i, habit in enumerate(st.session_state.habits):
            with cols[i % 2]:
                # تحديد لون البطاقة بناءً على النوع والحالة
                border_color = clr if habit['type'] == 'good' else "#ff4b4b"
                
                st.markdown(f"""
                <div style="border: 2px solid {border_color}; padding: 15px; border-radius: 15px; background: rgba(0,0,0,0.3); margin-bottom: 10px;">
                    <h4 style="margin:0; color:white;">{habit['name']}</h4>
                    <small style="color:{border_color};">{"عادة إيجابية" if habit['type'] == 'good' else "عادة سلبية"}</small>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                if c1.button("✅ فعلت", key=f"yes_{i}", use_container_width=True):
                    habit['status'] = True
                if c2.button("❌ لم أفعل", key=f"no_{i}", use_container_width=True):
                    habit['status'] = False

                # 3. نظام الرسائل التفاعلية (التشجيع والنصيحة)
                if habit['status'] is True:
                    if habit['type'] == 'good':
                        st.success("بطل! الاستمرار هو سر النجاح. 🔥")
                    else:
                        st.warning("انتبه! العادات السيئة تسحبك للخلف، حاول غداً مجدداً. 👊")
                
                elif habit['status'] is False:
                    if habit['type'] == 'good':
                        st.info("لا بأس، ابدأ بـ 5 دقائق فقط غداً لتسهيل المهمة. 💡")
                    else:
                        st.success("رائع! انتصارك على نفسك اليوم خطوة كبيرة. 🌟")
                
                if st.button(f"حذف العادة", key=f"del_h_{i}"):
                    st.session_state.habits.pop(i)
                    st.rerun()
    else:
        st.info("لم تقم بإضافة أي عادات بعد. ابدأ الآن!")

    if st.button("🔄 إعادة ضبط التتبع لليوم الجديد"):
        for h in st.session_state.habits:
            h['status'] = None
        st.rerun()
