import time


class MotorController:
    def __init__(self, arduino_communicator):
        self.arduino = arduino_communicator

    def move_to_face(self, x, y, frame_size):
        frame_width, frame_height = frame_size[1], frame_size[0]

        # Map the face coordinates to angles for the servo motors (Pan and Tilt)
        pan_angle = self.map_value(x + (frame_width / 2), 0, frame_width, 0, 180)
        tilt_angle = self.map_value(y + (frame_height / 2), 0, frame_height, 0, 180)

        print(f'Pan angle: {pan_angle} | Tilt angle: {tilt_angle}')
        # Send angles to Arduino for motor control
        # self.arduino.send_angles(pan_angle, tilt_angle)

    def map_value(self, value, from_low, from_high, to_low, to_high):
        # Map a value from one range to another (for converting pixel position to servo angle)
        return int(to_low + (float(value - from_low) / (from_high - from_low)) * (to_high - to_low))

    def nod_action(self):
        # Perform a nod action (move up and down briefly)
        self.arduino.send_angles(90, 30)
        time.sleep(0.5)
        self.arduino.send_angles(90, 150)
        time.sleep(0.5)
        self.arduino.send_angles(90, 90)
