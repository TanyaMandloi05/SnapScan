import streamlit as st
import pandas as pd
from datetime import datetime
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from src.components.dialog_attendance_results import show_attendence_result, attendence_result_dialog

@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write('Record audio of students saying I am present. Then AI will recognize the students')
    audio_data = None
    audio_data = st.audio_input("Record Classroom audio")
    if st.button('Analyze Audio', width='stretch', type='primary'):
        if audio_data is None:
            st.warning("⚠️ Please record the audio and press the Stop button before analyzing.")
            return

        with st.spinner('Processing Audio data'):
            enrolled_res = supabase.table('subject_student').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data
            candidates_dict = {}
            if not enrolled_students:
                st.warning('No students enrolled in this course')
                return
            
            for s in enrolled_students:
                student = s["students"]
                if student.get('voice_embedding'):
                    candidates_dict[student['student_id']] = student['voice_embedding']
            if not candidates_dict:
                st.error('No enrolled students have voice profiles registerd')
                return
        
            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)
            results, attendance_to_log = [], []

            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(student['student_id'], 0.0)
                is_present = bool(score > 0.0)
                results.append({
                    "Name": student['name'],
                    "ID": student['student_id'],
                    "Score": score if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })
                attendance_to_log.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })
            st.session_state.voice_attendance_results = (
                pd.DataFrame(results),
                attendance_to_log
            )

    
    if st.session_state.get('voice_attendance_results'):
        st.divider()

        df_results, logs = st.session_state.voice_attendance_results

        show_attendence_result(df_results, logs)
    


