import time
import numpy as np


class MotorControl:

    def __init__(self, frame_size, pan_initial=90.0, tilt_initial=75.0):


        # Frame dimensions
        self.cols = frame_size[1]
        self.rows = frame_size[0]

        # Servo initial angles
        self.pan_angle = pan_initial
        self.tilt_angle = tilt_initial

        # PID parameters for Pan and Tilt
        self.PAN_KP, self.PAN_KI, self.PAN_KD = 0.01, 0.0, 0.0  # Adjust as needed
        self.TILT_KP, self.TILT_KI, self.TILT_KD = 0.01, 0.0, 0.0

        # Pan and Tilt angle limits
        self.PAN_ANGLE_MIN, self.PAN_ANGLE_MAX = 5, 175
        self.TILT_ANGLE_MIN, self.TILT_ANGLE_MAX = 20, 120

        self.pan_output, self.tilt_output = 0, 0

        # Setpoint (dead zone) for acceptable error margin
        self.setpoint = 30  # May be adjusted depending on accuracy needs

        # PID variables initialization
        self.pan_integral = 0.0
        self.pan_last_time = time.time()
        self.pan_error_prior = 0.0

        self.tilt_integral = 0.0
        self.tilt_last_time = time.time()
        self.tilt_error_prior = 0.0

    def calculate_pid(self, error, kp, ki, kd, integral, last_time, error_prior):
        """General PID calculation for Pan and Tilt."""
        current_time = time.time()
        delta_time = current_time - last_time

        proportional = error
        integral += error * delta_time
        derivative = (error - error_prior) / delta_time if delta_time > 0 else 0

        output = kp * proportional + ki * integral + kd * derivative

        # print(f'Proportional: {proportional} | Output: {output}')

        return output, integral, current_time

    def update_angles(self, x, y, w, h):
        """Given the face bounding box, calculate the new Pan and Tilt angles."""
        # Calculate the center of the detected face
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        # Calculate the errors (distance of face center from frame center)
        pan_error = face_center_x - self.cols // 2
        tilt_error = face_center_y - self.rows // 2



        # Pan PID calculation if error is outside the setpoint range
        if abs(pan_error) > self.setpoint:
            self.pan_output, self.pan_integral, self.pan_last_time = self.calculate_pid(
                pan_error, self.PAN_KP, self.PAN_KI, self.PAN_KD,
                self.pan_integral, self.pan_last_time, self.pan_error_prior
            )
            self.pan_angle = np.clip(self.pan_angle + self.pan_output, self.PAN_ANGLE_MIN, self.PAN_ANGLE_MAX)

        # Tilt PID calculation if error is outside the setpoint range
        if abs(tilt_error) > self.setpoint:
            self.tilt_output, self.tilt_integral, self.tilt_last_time = self.calculate_pid(
                tilt_error, self.TILT_KP, self.TILT_KI, self.TILT_KD,
                self.tilt_integral, self.tilt_last_time, self.tilt_error_prior
            )
            self.tilt_angle = np.clip(self.tilt_angle + self.tilt_output, self.TILT_ANGLE_MIN, self.TILT_ANGLE_MAX)

        # Update prior error values for the next iteration
        self.pan_error_prior = pan_error
        self.tilt_error_prior = tilt_error

        # print(f'Pan angle:{self.pan_angle}, Tilt angle: {self.tilt_angle}')
        return self.pan_angle, self.tilt_angle
        # self.arduino.send_angles(self.pan_angle, self.tilt_angle)

    def nod_action(self):
        # Perform a nod action (move up and down briefly)
        self.arduino.send_angles(90, 30)
        time.sleep(0.5)
        self.arduino.send_angles(90, 150)
        time.sleep(0.5)
        self.arduino.send_angles(90, 90)
