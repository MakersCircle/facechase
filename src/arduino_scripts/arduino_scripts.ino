#include <Servo.h>

Servo panServo;  // create servo object for pan (horizontal)
Servo tiltServo; // create servo object for tilt (vertical)

void setup() {
  panServo.attach(6);  // attach pan servo to pin 6
  tiltServo.attach(5); // attach tilt servo to pin 5
  
  // Initialize servos to a middle position (90 degrees)
  panServo.write(90);  // Set pan servo to 90 degrees
  tiltServo.write(60); // Set tilt servo to 90 degrees
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    int panAngle = Serial.parseInt();  // read pan angle from serial input
    int tiltAngle = Serial.parseInt(); // read tilt angle from serial input
    
    panServo.write(panAngle);  // set pan servo to the desired angle
    tiltServo.write(tiltAngle); // set tilt servo to the desired angle
  }
}
