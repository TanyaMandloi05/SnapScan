import streamlit as st
from src.ui.base_layout import style_base_layout , style_dashboard_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.database.db import teacher_exists, create_teacher, teacher_login, get_teacher_sub
from src.components.dialog_share_subject import share_sub_dialog
from src.components.dialog_add_photo import add_photos_dialog
import time

def teacher_screen():
    style_base_layout()
    style_dashboard_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    col1, col2 = st.columns(2, vertical_alignment='center', gap="xxlarge")
    
    with col1:
        header_dashboard()
    
    with col2:
        st.header(f""" Welcome {teacher_data['name']}""")
        if st.button("Logout", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['is_Logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()
    st.space()


    tab1, tab2, tab3 = st.columns(3)
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendence'
    with tab1:
       type1 = 'primary' if st.session_state.current_teacher_tab == 'take_attendence' else "tertiary"
       if st.button("Take Attendance", type=type1, width='stretch', icon=':material/ar_on_you:'):
        st.session_state.current_teacher_tab = 'take_attendence'
        st.rerun()

    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subject' else "tertiary"
        if st.button("Manage Subjects", width='stretch', icon=':material/book_ribbon:', type=type2):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()

    with tab3:
        type3 ='primary' if st.session_state.current_teacher_tab == 'attendence_records' else "tertiary"
        if st.button("Attendance Records",width='stretch', icon=':material/cards_stack:', type=type3):
            st.session_state.current_teacher_tab = 'attendence_records'
            st.rerun()
    st.divider()

    if st.session_state.current_teacher_tab == 'take_attendence':
        teacher_tab_take_attendence()

    if st.session_state.current_teacher_tab == 'manage_subject':
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == 'attendence_records':
        teacher_tab_attendence_record()

    footer_dashboard()


def teacher_tab_take_attendence():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header("Take AI Attendance")

    if 'attendence_image' not in st.session_state:
        st.session_state.attendence_image = []

    subjects = get_teacher_sub(teacher_id)
    if not subjects:
        st.warning("You havent created any subject yet! Please create one")
        return 

    subject_options = {}
    for s in subjects:
        key = f"{s['name']} - {s['subject_code']}"
        value = s['subject_id']
        subject_options[key] = value

    col1, col2 = st.columns([3,1],  vertical_alignment='bottom')
    with col1:
        selected_subject_label = st.selectbox('select subjects', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]



def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2) 
    with col1:
        st.header("Manage subjects")
    with col2:
        if st.button("create New Subject", width="stretch"):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_sub(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                 ("👨‍🎓", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
            def sharebtn():
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_sub_dialog(sub['name'], sub['subject_code'])
                st.space()

            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = stats,
                footer_callback = sharebtn
            )

def teacher_tab_attendence_record():
    st.header("manage attendence")
    
    
    

def login_teacher(teacher_username, password):
    if not teacher_username or not password:
        return False
    teacher = teacher_login(teacher_username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False

def teacher_screen_login():
    col1, col2 = st.columns(2, vertical_alignment='center', gap="xxlarge")
    
    with col1:
        header_dashboard()

    with col2:
        if st.button("Go Back to Home", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = 'Go Back'
            st.rerun() #Without st.rerun(), the page won't immediately switch after changing the session state.

    st.header("Login using password", text_alignment="center")

    st.space()
    st.space()

    teacher_username = st.text_input("Enter your username", placeholder="Tanya")
    password = st.text_input("Enter your password", type="password", placeholder="********")

    st.divider()

    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("Login now", shortcut="Ctrl+Enter", icon=':material/passkey:', width="stretch"):
            if login_teacher(teacher_username, password):
                st.toast("Welcome back ", icon="👋")
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid username or password combo")

    with btn2:
        if st.button("Register Instead", type='primary', icon=':material/passkey:', width="stretch"):
            st.session_state.teacher_login_type="register"

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, password,  confirm_password):
    if not teacher_username or not teacher_name or not password:
        return False , "All Feilds are required"
    if teacher_exists(teacher_username):
        return False, "Username already taken"
    if confirm_password != password:
        return False, "Password dosen't match"
    
    try:
        create_teacher(teacher_username, password, teacher_name)
        return True, "Successfully registered"
    
    except Exception as e:
        return False , e



def teacher_screen_register():
    col1, col2 = st.columns(2, vertical_alignment='center', gap="xxlarge")
    
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go Back to Home", key="loginbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = 'Go Back'
            st.rerun() #Without st.rerun(), the page won't immediately switch after changing the session state.
    st.header("Register your teacher profile")
    st.space()
    st.space()
    
    teacher_username = st.text_input("Enter your username", placeholder="@tanya")
    teacher_name = st.text_input("Enter your name", placeholder="Tanya Mandloi")
    password = st.text_input("Enter your password", type="password", placeholder="********")
    confirm_password = st.text_input("Confirm your password", type="password", placeholder="********")
    
    st.divider()
    
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("Register Now", type='primary', icon=':material/passkey:', width="stretch", shortcut="Ctrl+Enter"):
            success, message = register_teacher(teacher_username, teacher_name, password,  confirm_password)
            if success:
                st.success(message)
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)
    
    with btn2:
         if st.button("Login", icon=':material/passkey:', width="stretch"):
             st.session_state.teacher_login_type="login"


        
    footer_dashboard()

    

# teacher_screen()