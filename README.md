# 📸 Snap-Scan

Snap-Scan is a smart attendance management system that uses **face and voice recognition** to automate classroom attendance. It provides separate features for teachers and students, making it easier to manage subjects, enrollment, attendance, and attendance records.

## 🚀 Features

### 👨‍🏫 Teacher
- Teacher registration and login
- Secure password hashing using **Bcrypt**
- Create and manage subjects
- Generate and share subject codes with students
- View enrolled students
- Take attendance using face and voice recognition
- Review detected attendance before confirming it
- View attendance records including:
  - Class date
  - Present students
  - Number of students present

### 👨‍🎓 Student
- Student registration and login
- Face recognition for student identification
- Voice registration for attendance
- Enroll in subjects using subject codes
- View enrolled subjects
- View attendance records for enrolled subjects

## 🛠️ Technologies Used

- **Python**
- **Streamlit** – User interface
- **Supabase** – Database
- **Bcrypt** – Password hashing
- **Face Recognition** – Face detection and recognition
- **dlib** – Face recognition processing
- **Librosa** – Audio processing
- **Resemblyzer** – Voice recognition
- **Pillow** – Image processing
- **Scikit-learn** – Machine learning utilities
- **Segno** – QR code generation
- **NumPy & Pandas** – Data processing

## 🔐 Authentication

Snap-Scan provides separate authentication for teachers and students.

Teacher passwords are securely hashed using **Bcrypt** instead of storing plain-text passwords.

Students can register their face and voice, which are later used for identification during attendance.

## 📚 Subject Enrollment

Teachers can create subjects and share a unique subject code with students.

Students can enter the subject code to enroll in the corresponding subject.

The relationship between students and subjects is managed through the `subject_student` table in Supabase.

## 📷 Attendance Workflow

1. Teacher selects a subject.
2. Teacher captures or uploads classroom photos.
3. Snap-Scan detects and recognizes students using face recognition.
4. Voice recognition can also be used for student identification.
5. The teacher reviews the detected students.
6. Attendance is confirmed and stored.
7. Teachers can later view attendance records.

## 🗄️ Database

The project uses **Supabase** for storing application data.

Main tables include:

- `students`
- `teachers`
- `subjects`
- `subject_student`
- `attendance_logs`

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/snap-scan.git
cd snap-scan

2. Create a virtual environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure Supabase

Create a Supabase project and add your required environment variables/configuration.

For example:

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
5. Run the application
streamlit run app.py

The application will be available at:

http://localhost:8501
📁 Project Structure
Snap-Scan/
│
├── app.py
├── requirements.txt
│
├── src/
│   ├── components/
│   ├── database/
│   ├── screens/
│   └── ...
│
└── README.md
🎯 Purpose

The goal of Snap-Scan is to reduce manual attendance work and provide a more convenient way for teachers to manage classroom attendance using face and voice-based identification.

👩‍💻 Author

Tanya Mandloi

## 🤝 Contributing

Contributions are welcome! If you'd like to improve Snap-Scan, follow these steps:

1. **Fork** the repository.
2. **Clone** your fork:
   ```bash
   git clone https://github.com/your-username/snap-scan.git
   Create a new branch:

git checkout -b feature/your-feature
Make your changes and test them locally.

Commit your changes:

git commit -m "Add your feature"

Push your branch:

git push origin feature/your-feature
Open a Pull Request and describe the changes you made.

Please make sure your changes are tested and follow the existing project structure and coding style.

For your project, I would keep it **simple like this** rather than making the contribution section too formal.
