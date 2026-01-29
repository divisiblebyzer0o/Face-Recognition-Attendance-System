import cv2
import os
import numpy as np

face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

def train_recognizer():
    faces = []
    labels = []
    label_map = {}

    current_label = 0

    for user in os.listdir("dataset"):
        user_path = os.path.join("dataset", user)
        label_map[current_label] = user

        for img_name in os.listdir(user_path):
            img_path = os.path.join(user_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            faces.append(img)
            labels.append(current_label)

        current_label += 1

    recognizer = cv2.face.LBPHFaceRecognizer_create(
        radius=1,
        neighbors=8,
        grid_x=8,
        grid_y=8
    )
    recognizer.train(faces, np.array(labels))

    return recognizer, label_map



