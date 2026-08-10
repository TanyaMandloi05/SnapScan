import streamlit as st
from src.ui.base_layout import style_base_layout , style_dashboard_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image # Used to open and process images
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student
import time



def student_dashboard():
    st.header("DASHBOARD HERE !")

def student_screen():
    style_base_layout()
    style_dashboard_layout()
    if "student_data" in st.session_state:
        student_dashboard()
        return
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


    show_registration = False
    photo_source = st.camera_input("Position your face in center")
    if photo_source:
        image = np.array(Image.open(photo_source)) ## Open the captured image and convert it to a NumPy array
        with st.spinner('AI is scanning'):
            print("STARTING PREDICTION")
            detected, all_students, num_faces = predict_attendance(image) #identifies the person.
            print("PREDICTION FINISHED")
            print("Detected:", detected)
            print("All students:", all_students)
            print("Number of faces:", num_faces)

            if num_faces == 0:
                print("enter in zero condtion")
                st.warning("Face not found")
            elif num_faces > 1:
                print("enter in first condtion")
                st.warning("Multiple faces found")
            else:
                print("enter the last condtion")
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    print(all_students)
                    student = next((s for s in all_students if s['student_id'] == student_id), None) #matching current id with database id
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    print("NO STUDENT RECOGNIZED")
                    st.info('Face not found you might be a new student!')
                    show_registration = True
                    print("show_registration =", show_registration)
    if show_registration:
        with st.container(border=True):
            st.header("Register new Profile")
            name = st.text_input("Enter your name", placeholder="E.g. Tanya Mandloi")

            st.subheader("Optional: voice enrollement")
            st.info("Enroll for voice-only attendance")

            audio_data = None

            try:
                audio_data = st.audio_input("Record a short phrase..Like I am present My name is your name")
                print("audio captured")
            except Exception:
                st.error("Audio data failed")
            if st.button("create account", type='primary'):
                if name:
                    with st.spinner("Creating account"):

                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_embd = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                                response_data = create_student(name, face_embd, voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile created hi {name} !")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Could not capture your facial features for registration")


                else:
                    st.warning("Please enter your name first")


   
    

