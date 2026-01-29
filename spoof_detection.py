from scipy.spatial import distance

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def detect_blink(landmarks):
    LEFT_EYE = landmarks[36:42]
    RIGHT_EYE = landmarks[42:48]

    leftEAR = eye_aspect_ratio(LEFT_EYE)
    rightEAR = eye_aspect_ratio(RIGHT_EYE)

    ear = (leftEAR + rightEAR) / 2.0
    return ear < 0.22   # blink threshold
