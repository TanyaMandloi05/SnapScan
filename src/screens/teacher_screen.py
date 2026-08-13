import streamlit as st
from src.ui.base_layout import style_base_layout , style_dashboard_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.database.db import teacher_exists, create_teacher, teacher_login, get_teacher_sub, get_attendence_record
from src.components.dialog_share_subject import share_sub_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendence_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase
import pandas as pd
from datetime import datetime
import time
import numpy as np

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

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox(
            'select subjects',
            options=list(subject_options.keys())
        )

    with col2:
        if st.button(
            'Add Photos',
            type='primary',
            icon=':material/photo_prints:',
            width='stretch'
        ):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    # Show photos only if photos have been added
    if st.session_state.attendence_image:
        st.header("Added Photos")

        gallery_col = st.columns(4)

        for idx, image in enumerate(st.session_state.attendence_image):
            with gallery_col[idx % 4]:
                st.image(
                    image,
                    width="stretch",
                    caption=f"photo{idx + 1}"
                )

    # These buttons should ALWAYS be visible
    has_photos = bool(st.session_state.attendence_image)

    c1, c2, c3 = st.columns(3)

    # -------------------------------
    # Clear All Photos
    # -------------------------------
    with c1:
        if st.button(
            "Clear All Photos",
            disabled=not has_photos,
            width="stretch",
            type="tertiary",
            icon=':material/delete:'
        ):
            st.session_state.attendence_image = []
            st.rerun()

    # -------------------------------
    # Run Face Analysis
    # -------------------------------
    with c2:
        if st.button(
            "Run Face Analysis",
            disabled=not has_photos,
            width="stretch",
            type="tertiary",
            icon=':material/analytics:'
        ):
            with st.spinner('Deep Scanning classroom photos'):

                all_detected_ids = {}

                for idx, img in enumerate(
                    st.session_state.attendence_image
                ):
                    img_np = np.array(img.convert('RGB'))

                    detected_students, _, _ = predict_attendance(img_np)

                    if detected_students:
                        for sid in detected_students.keys():
                            student_id = int(sid)

                            # If student ID already exists,
                            # add the current photo to the list.
                            all_detected_ids.setdefault(
                                student_id, []
                            ).append(f"photo{idx + 1}")

                # Get enrolled students
                enrolled_res = (
                    supabase
                    .table("subject_student")
                    .select("*, students(*)")
                    .eq('subject_id', selected_subject_id)
                    .execute()
                )

                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning(
                        "No student enrolled in this course"
                    )

                else:
                    results = []
                    attendence_to_log = []

                    current_timestamp = datetime.now().strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )

                    for node in enrolled_students:
                        student = node['students']

                        sources = all_detected_ids.get(
                            int(student['student_id']),
                            []
                        )

                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Sources": (
                                ",".join(sources)
                                if is_present
                                else "-"
                            ),
                            "Status": (
                                "✅ Present"
                                if is_present
                                else "❌ Absent"
                            )
                        })

                        attendence_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendence_result_dialog(
                        pd.DataFrame(results),
                        attendence_to_log
                    )

    # -------------------------------
    # Voice Attendance
    # -------------------------------
    with c3:
        if st.button(
            'Use Voice Attendance',
            type='primary',
            width='stretch',
            icon=':material/mic:'
        ):
            voice_attendance_dialog(selected_subject_id)
                        

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
    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendence_record(teacher_id)
    if not records:
        return 
    data = []
    for r in records:
        ts = r.get("timestamp")
        if not ts:
            continue
        session_key = ts.split(".")[0]
        display_time = datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p")

        data.append({
        "ts_group": session_key,
        "Time": display_time,
        "Subject": r["subjects"]["name"],
        "Subject Code": r["subjects"]["subject_code"],
        "is_present": r.get("is_present")
        })

    df = pd.DataFrame(data)
    summary = (
    df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
    .agg(
        Present_Count=('is_present', 'sum'),
        Total_Count=('is_present', 'count')
    )
    .reset_index()
    )

    summary['Attendance Stats'] = (
    "✅ " + summary['Present_Count'].astype(str)
    + " / " + summary['Total_Count'].astype(str)
    + " Students"
    )

    display_df = summary[
    ['ts_group','Time', 'Subject', 'Subject Code', 'Attendance Stats']
    ]

    event = st.dataframe(
    display_df,
    width="stretch",
    hide_index=True,
     column_config={
        "ts_group": None
    },
    on_select="rerun",
    selection_mode="single-row"
    )
    if event.selection.rows:
        selected_row = event.selection.rows[0]
        selected_data = display_df.iloc[selected_row]
        selected_session = selected_data["ts_group"]
        session_records = []
        
        for r in records:
            if r.get("timestamp").split(".")[0] == selected_session:
                session_records.append(r)

        detail_data = []

        for r in session_records:
            student = r["students"]
            detail_data.append({
            "Student ID": student["student_id"],
            "Name": student["name"],
            "Status": "✅ Present" if r["is_present"] else "❌ Absent"
            })

        detail_df = pd.DataFrame(detail_data)
        st.dataframe(
        detail_df,
        width="stretch",
        hide_index=True
        )
    
    

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