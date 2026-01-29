import cv2
import sqlite3
import random
from datetime import datetime
from utils import train_recognizer

# ---------------- LOAD CASCADES ----------------
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

# ---------------- TRAIN MODEL ----------------
recognizer, label_map = train_recognizer()

# ---------------- RANDOM INSTRUCTION ----------------
instruction = random.choice(["BLINK", "TURN LEFT"])
instruction_done = False

# ---------------- RUNTIME CONTROLS ----------------
marked_users = set()
blink_detected = False
eyes_open_prev = True
face_x_prev = None
turn_left_detected = False

# ---------------- CAMERA INIT (FIX) ----------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print(" Camera not opened")
    exit()

cv2.namedWindow("Face Attendance System", cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # -------- PREPROCESS --------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # -------- FACE DETECTION --------
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=4,
        minSize=(80, 80)
    )

    # Instruction text (ALWAYS shown)
    cv2.putText(
        frame,
        f"Instruction: {instruction}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 0, 0),
        2
    )

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]

        # ---------- BLINK DETECTION ----------
        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=3
        )

        eyes_open = len(eyes) > 0

        if eyes_open_prev and not eyes_open:
            eyes_open_prev = False
        elif not eyes_open_prev and eyes_open:
            blink_detected = True
            eyes_open_prev = True

        # ---------- TURN LEFT DETECTION ----------
        if face_x_prev is None:
            face_x_prev = x
        elif x < face_x_prev - 15:
            turn_left_detected = True
        face_x_prev = x

        # ---------- CHECK INSTRUCTION ----------
        if instruction == "BLINK" and blink_detected:
            instruction_done = True
        elif instruction == "TURN LEFT" and turn_left_detected:
            instruction_done = True

        # ---------- FACE RECOGNITION ----------
        label, confidence = recognizer.predict(roi_gray)
        name = "Unknown"

        if confidence < 70 and instruction_done:
            user_id = label_map[label]
            name = user_id

            if user_id not in marked_users:
                date = datetime.now().strftime("%Y-%m-%d")
                time = datetime.now().strftime("%H:%M:%S")

                conn = sqlite3.connect("attendance.db")
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT * FROM attendance WHERE user_id=? AND date=?",
                    (user_id, date)
                )
                record = cursor.fetchone()

                if record is None:
                    cursor.execute(
                        "INSERT INTO attendance VALUES (?,?,?,?)",
                        (user_id, date, time, None)
                    )
                    print(" Punch IN:", user_id)

                elif record[3] is None:
                    cursor.execute(
                        "UPDATE attendance SET punch_out=? WHERE user_id=? AND date=?",
                        (time, user_id, date)
                    )
                    print(" Punch OUT:", user_id)

                conn.commit()
                conn.close()
                marked_users.add(user_id)

        # ---------- UI ----------
        color = (0, 255, 0) if instruction_done else (0, 0, 255)
        status = "Verified" if instruction_done else "Do Instruction"

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(
            frame,
            status,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.imshow("Face Attendance System", frame)

    # -------- EXIT KEY --------
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


