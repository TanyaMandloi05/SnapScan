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


