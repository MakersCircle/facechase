import cv2
import mediapipe as mp
from matplotlib import pyplot as plt




mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


IMAGE_FILES = ['../test/test_image_1.jpg', '../test/test_image_2.jpg', '../test/test_image_3.jpg']

test_img = cv2.cvtColor(cv2.imread(IMAGE_FILES[2]), cv2.COLOR_BGR2RGB)

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    results = face_detection.process(test_img)
    if results.detections:
        for detection in results.detections:
            # Draw the bounding box around the detected face
            mp_drawing.draw_detection(test_img, detection)

    plt.imshow(test_img)
    plt.show()