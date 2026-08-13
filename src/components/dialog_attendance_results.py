import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time

from src.database.db import create_attendence

def show_attendence_result(df, logs):
    st.write("Please review attendence before confirming")
    st.dataframe(df, hide_index=True, width='stretch')
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Discard", width="stretch"):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button("Confirm and save", width="stretch", type='primary'):
            try:
                create_attendence(logs)
                st.toast("Attendence taken")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(e)


@st.dialog("Attendance Report")
def attendence_result_dialog(df, logs):
    show_attendence_result(df, logs)

