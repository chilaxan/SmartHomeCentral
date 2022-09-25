#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
int pos = 0;    // variable to store the servo position
char l;

#define CLOSE 80
#define OPEN 200

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(115200);
  myservo.write(CLOSE);
  while (!Serial) (delay(100));
}

void loop() {
  while (!Serial.available());
  Serial.readBytes(&l, 1);
  switch(l) {
    case 0:
      if (pos != CLOSE) {
        myservo.write(CLOSE);
      }
      break;
    case 1:
      if (pos != OPEN) {
        myservo.write(OPEN);
      }
      break;
  }
}
