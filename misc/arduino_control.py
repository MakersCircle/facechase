import serial
import time

# Set up serial communication with Arduino
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)  # Adjust 'COM3' to your port


def send_angles(pan_angle, tilt_angle):
    # Send angles to Arduino as a string
    data = f"{pan_angle}\n{tilt_angle}\n"
    arduino.write(data.encode())

pan = 10  # Example pan angle (0 to 180)
tilt = 10  # Example tilt angle (0 to 180)

send_angles(pan, tilt)
# Example of sending angles
while True:
    pan +=1  # Example pan angle (0 to 180)
    tilt  +=1  # Example tilt angle (0 to 180)
    print(pan, tilt)
    send_angles(pan, tilt)
    time.sleep(1)  # Wait 1 second before sending again
