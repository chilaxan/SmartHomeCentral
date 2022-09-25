#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
int pos = 0;    // variable to store the servo position
char l;

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(115200);
  myservo.write(0);
  while (!Serial) (delay(100));
}

void loop() {
  while (!Serial.available());
  Serial.readBytes(&l, 1);
  switch(l) {
    case 0:
      if (pos != 180) {
        for (pos = 0; pos < 180; pos += 1) {
          myservo.write(pos);
          delay(7);
        }
      }
      break;
    case 1:
      if (pos != 0) {
        for (pos = 180; pos > 0; pos -= 1) {
          myservo.write(pos);
          delay(7);
        }
      }
      break;
  }
}
