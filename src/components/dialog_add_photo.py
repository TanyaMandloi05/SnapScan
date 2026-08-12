import streamlit as st
from PIL import Image

@st.dialog("Capture or upload photo")
def add_photos_dialog():
    st.write("add classroom photos to scan for attendence")

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1, t2 = st.columns(2)
    with t1:
        type_camera = 'primary' if st.session_state.photo_tab == "camera" else 'tertiary'
        if st.button("camera", type=type_camera, width="stretch"):
            st.session_state.photo_tab = "camera"

    with t2:
        type_upload = 'primary' if st.session_state.photo_tab == "upload" else 'tertiary'
        if st.button("upload photos", type=type_upload, width="stretch"):
            st.session_state.photo_tab = "upload"

    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input("Take snapshot", key='dialog_cam')
        if cam_photo:
            st.session_state.attendence_image.append(Image.open(cam_photo))
            st.toast("Photo captured")
            st.rerun()

    if st.session_state.photo_tab == "upload":
        uploaded_files = st.file_uploader("choose image file", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key='dialog_upload')
        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendence_image.append(Image.open(f))
            st.toast("Photos uploaded Successfully !!")
            st.rerun()

    st.divider()
    if st.button("Done", type='primary', width="stretch"):
        st.rerun()
