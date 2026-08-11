from src.database.config import supabase
import bcrypt


def teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data)


def hash_pass(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 


def create_teacher(username, password, name):
    data = {"username": username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data 


def check_password(entered_pass , stored_pass):
    return bcrypt.checkpw(entered_pass.encode(), stored_pass.encode())


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if(check_password(password, teacher["password"])):
            return teacher
        return None

def create_student(name, face_embedding, voice_embedding = None):
    data = {"name":name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_subject(subject_code, subject_name, section, teacher_id):
    data = {"subject_code": subject_code, "name": subject_name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data


# Get all subjects, count enrolled students in each subject,
# and get attendance records for each subject/student.
def get_teacher_sub(teacher_id):
    response = supabase.table("subjects").select("* , subject_student(count), attendence_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        sub["total_students"] = sub['subject_student'][0]["count"]
        attendence = sub['attendence_logs']
        unique_session = set(log['timestamps'] for log in attendence)
        sub["total_classes"] = len(unique_session)
        sub.pop("subject_student", None)
        sub.pop("attendence_logs", None)

    return subjects
