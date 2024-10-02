import serial
import time


class ArduinoCommunicator:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        time.sleep(2)  # Allow time for Arduino to reset after connection

    def send_angles(self, pan_angle, tilt_angle):
        # Send angles to Arduino as a string
        data = f"{pan_angle}\n{tilt_angle}\n"
        self.arduino.write(data.encode())

    def close(self):
        self.arduino.close()


if __name__ == '__main__':
    arduino = ArduinoCommunicator()
    arduino.send_angles(90, 60)