# Face Authentication Attendance System

A real-time face authentication based attendance system using OpenCV.
The system includes spoof prevention using eye-blink detection and
random challenge-response instructions.

---

## Features
- Real-time face detection (Haar Cascade)
- Face recognition (LBPH)
- Eye-blink based liveness detection
- Random instruction (Blink / Turn Left) to prevent video spoofing
- Punch-In / Punch-Out attendance
- SQLite database

---

## Tech Stack
- Python
- OpenCV (opencv-contrib)
- SQLite

---

## Installation

```bash
git clone https://github.com/<your-username>/face-attendance-system.git
cd face-attendance-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Working 

# setup database
python database.py

#Register User
python register_face.py

#Run Attendance System

python recognize_attendance.py



