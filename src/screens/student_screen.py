import streamlit as st
from src.ui.base_layout import style_base_layout , style_dashboard_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
def student_screen():
    style_base_layout()
    style_dashboard_layout()
    col1, col2 = st.columns(2, vertical_alignment='center', gap="xxlarge")
    
    with col1:
        header_dashboard()
    
    with col2:
        if st.button("Go Back to Home", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = 'Go Back'
            st.rerun() #Without st.rerun(), the page won't immediately switch after changing the session state.
    
    st.header("Login using Face Id", text_alignment="center")
    
    st.space()
    st.space()

    st.camera_input("Position your face in center")

    footer_dashboard()

# student_screen()