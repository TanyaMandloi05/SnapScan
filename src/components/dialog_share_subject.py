import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def share_sub_dialog(subject_name, subject_code):


