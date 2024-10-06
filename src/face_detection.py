import cv2
import mediapipe as mp


class FaceDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.8)

    def detect_faces(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        faces = []
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                faces.append((x, y, w, h))
        return faces

    def draw_detections(self, frame, faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()

    ret, frame = cap.read()
    print(frame.shape)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)


        faces = detector.detect_faces(frame)

        # Draw the detections on the frame
        detector.draw_detections(frame, faces)

        print(faces)

        # Display the frame
        cv2.imshow('Face Detection Test', frame)

        # Press 'q' to exit the test
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

