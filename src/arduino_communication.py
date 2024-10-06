import serial
import time


class ArduinoCommunicator:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        time.sleep(0.5)  # Allow time for Arduino to reset after connection

    def send_angles(self, pan_angle, tilt_angle):

        data = f"{round(pan_angle)}\n{round(tilt_angle)}\n"
        print(f'Pan angle: {pan_angle}; Tilt angle: {tilt_angle}')
        self.arduino.write(data.encode())

    def close(self):
        self.arduino.close()


if __name__ == '__main__':
    arduino = ArduinoCommunicator()
    while True:
        arduino.send_angles(90, 40)
        time.sleep(1)