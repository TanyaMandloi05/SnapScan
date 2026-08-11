import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subject")
    sub_code = st.text_input("Subject code", placeholder="MCADD-101")
    sub_name = st.text_input("Subject name", placeholder="Data Structures")
    sub_section = st.text_input("Section", placeholder="A")

    st.button("Create subject Now", width="stretch")
    if sub_code and sub_name and sub_section:
        try:
            create_subject(sub_code, sub_name, sub_section, teacher_id)
            st.toast("subject created")
            st.rerun()
        except Exception as e:
            st.error(f"Error creating subject : {e}")
    else:
        st.warning("please fill all the feilds")