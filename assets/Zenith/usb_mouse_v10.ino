/*This script uses the Teensy 4.0 to emulate a mouse

A rotary encoder mimicks the scroll function, two buttons mimick the Left and 
Right button clicks, and PSP joystick controls mouse movement.

From the Arduino IDE use the Teensy 4.0 as the Board and USB Type as "Serial,
Keyboard, Mouse, Joystick*/


#include <Bounce.h>

const int moveDistance = 5;  // how much to move the mouse on each button press

const int joyXPin = A0;  // Joystick X-axis input
const int joyYPin = A1;  // Joystick Y-axis input

int joyXValue, joyYValue;


const int encoderPinA = 1;
const int encoderPinB = 2;

volatile int encoderPosition = 0;
volatile int lastEncoded = 0;

const int grayCode[16] = {0, 1, 3, 2, 7, 6, 4, 5, 15, 14, 12, 13, 8, 9, 11, 10};


Bounce button6 = Bounce(6, 10);
Bounce button7 = Bounce(7, 10);



void setup() {

  Serial.begin(9600);

  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  
  Mouse.screenSize(1000, 600);

  pinMode(encoderPinA, INPUT);
  pinMode(encoderPinB, INPUT);

  attachInterrupt(digitalPinToInterrupt(encoderPinA), updateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPinB), updateEncoder, CHANGE);

}


void loop() {

  button6.update();
  button7.update();

  joyXValue = analogRead(joyXPin);
  joyYValue = analogRead(joyYPin);
  
  //Serial.println(joyXValue);
  //Serial.println(joyYValue);
  //Serial.println("------");


  /* PSP joystick values I was getting
  X - normal: 532-541
  - left:   842
  - right:  167

Y - normal: 457-490
  - up:     157
  - down:   840
  */


  /*Well, let's build a simplish range for this stuff
  
  512 is (or supposed to be) center / average
  375-512-649 will qualify as no movement - the 'normal' values fluctuate, so keep the range as is for now
  
  Anything above or below should return a value that will modify the mouse position
  */

  
  int threshold = 137;
  int base = 512; // 1024/2 = 
  int mouseMoveRate = 5;


  //int mouseX = map(joyXValue, 0, 1024, 0,255);
  int mouseX;
  if (joyXValue <= base-threshold) { //left
    mouseX = -1*mouseMoveRate;
  } else if (joyXValue > base+threshold && joyXValue != 1023) { //right
    mouseX = 1*mouseMoveRate;
  } else { //pass
    mouseX = 0;
  }

  int mouseY;
  if (joyYValue <= base-threshold) { //up
    mouseY = -1*mouseMoveRate;
  } else if (joyYValue > base+threshold && joyYValue != 1023) { //down
    mouseY = 1*mouseMoveRate;
  } else { //pass
    mouseY = 0;
  }


  Mouse.move(mouseX, mouseY, 0);

  if (button6.fallingEdge()) {
    Mouse.press(MOUSE_RIGHT);
  }
  if (button6.risingEdge()) {
    Mouse.release(MOUSE_RIGHT);
  }

  if (button7.fallingEdge()) {
    Mouse.press(MOUSE_LEFT);
  }
  if (button7.risingEdge()) {
    Mouse.release(MOUSE_LEFT);
  }

  delay(10);

}


void updateEncoder() {
  int MSB = digitalRead(encoderPinA);
  int LSB = digitalRead(encoderPinB);

  int encoded = (MSB << 1) | LSB;
  int sum = (lastEncoded << 2) | encoded;

  int state = grayCode[sum & 0b1111];

  if (state == 1 || state == 7 || state == 8 || state == 14) {
    encoderPosition++;
    Mouse.scroll(+3);
  } else if (state == 2 || state == 4 || state == 11 || state == 13) {
    encoderPosition--;
    Mouse.scroll(-3);
  }

  lastEncoded = encoded;

  Serial.println(encoderPosition);
}
