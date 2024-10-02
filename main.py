import cv2
from src.face_detection import FaceDetector
from src.arduino_communication import ArduinoCommunicator
from src.motor_control import MotorController


def main():
    # Initialize face detector, Arduino communicator, and motor controller
    face_detector = FaceDetector()
    # arduino = ArduinoCommunicator('/dev/ttyACM0')  # Update the port as per your setup
    motor_controller = MotorController('arduino')

    cap = cv2.VideoCapture(0)  # Open the webcam

    tracked_face = None  # Stores the first detected face coordinates

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the image horizontally (mirror image)
        frame = cv2.flip(frame, 1)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        # Detect faces in the frame
        faces = face_detector.detect_faces(frame)

        if faces:
            if not tracked_face:
                # If no face is currently tracked, start tracking the first detected face
                tracked_face = faces[0]

            # Continue tracking the first detected person
            x, y, w, h = tracked_face
            motor_controller.move_to_face(x, y, frame.shape)

        # Show the frame with detections
        face_detector.draw_detections(frame, faces)
        cv2.imshow('Smart Tracking Robot', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
