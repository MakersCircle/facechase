#include <Servo.h>

Servo servoVer;  // Create a Servo object for vertical movement
Servo servoHor;  // Create a Servo object for horizontal movement

void setup() {
  Serial.begin(9600);
  servoVer.attach(5); // Attach Vertical Servo to Pin 5
  servoHor.attach(6); // Attach Horizontal Servo to Pin 6
  servoVer.write(50);  // Set vertical servo to 90 degrees
  servoHor.write(70);  // Set horizontal servo to 90 degrees
}

void loop() {
  // Your main code here
}
