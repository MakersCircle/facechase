import cv2
import mediapipe as mp

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)

# Face detection with MediaPipe
with mp_face_detection.FaceDetection(min_detection_confidence=0.8) as face_detection:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the image horizontally (mirror image)
        frame = cv2.flip(frame, 1)  # 1 indicates horizontal flipping

        # Rotate the image by 90 degrees
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # Rotate 90 degrees clockwise

        # Convert the BGR image to RGB for face detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        # Draw face detection box if faces are detected
        if results.detections:
            for detection in results.detections:
                # Draw face detection bounding box
                mp_drawing.draw_detection(frame, detection)

                # Get face coordinates (bounding box)
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                # You can use these coordinates to control your pan-tilt mechanism if needed.

        # Show the modified frame
        cv2.imshow('Face Tracking - Flipped and Rotated', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Release the webcam and close windows
        cap.release()
        cv2.destroyAllWindows()
