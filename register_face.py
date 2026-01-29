import cv2
import os

face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

user_id = input("Enter User ID: ")
os.makedirs(f"dataset/{user_id}", exist_ok=True)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow("Register Face", cv2.WINDOW_NORMAL)

count = 0
MAX_IMAGES = 25

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]

        cv2.imwrite(f"dataset/{user_id}/{count}.jpg", face_img)
        count += 1

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(
            frame,
            f"Captured {count}/{MAX_IMAGES}",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

    cv2.imshow("Register Face", frame)

    if count >= MAX_IMAGES:
        break

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

print(" Face registration completed")


