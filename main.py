import cv2
from src.face_detection import FaceDetector
from src.arduino_communication import ArduinoCommunicator
from src.motor_control import MotorControl


def main():
    # Initialize face detector, Arduino communicator, and motor controller
    face_detector = FaceDetector()
    arduino = ArduinoCommunicator('/dev/ttyACM0')  # Update the port as per your setup

    cap = cv2.VideoCapture(0)  # Open the webcam

    ret, frame = cap.read()
    motor_control = MotorControl(frame_size=(frame.shape[1], frame.shape[0]))
    pan_angle, tilt_angle = 90, 90

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


            # Continue tracking the first detected person
            x, y, w, h = faces[0]

            pan_angle, tilt_angle = motor_control.update_angles(x, y, w, h)
        arduino.send_angles(pan_angle, tilt_angle)

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
