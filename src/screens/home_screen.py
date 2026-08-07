import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_home_layout, style_base_layout
def home_screen():
    header_home()
    style_home_layout()
    style_base_layout()
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.header("I am a teacher")
        # st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=120)
        st.image("src/images/teacher.png", width=120)
        if st.button("Teacher Portal", type="primary" , icon=":material/arrow_outward:", icon_position="right"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
    with col2:
        st.header("I am a Student")
        # st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        st.image("src/images/student.png", width=120)
        if st.button("Student Portal", type="primary", icon=":material/arrow_outward:", icon_position="right"):
            st.session_state['login_type'] = 'student'
            st.rerun()
    footer_home()

# home_screen()