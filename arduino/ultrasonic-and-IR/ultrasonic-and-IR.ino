/* This code takes in information from ultrasonic and IR sensors to determine when an object
 *  has been placed in a bin.
 *  The code applies to a single bin (single bin is assumed to contain two ultrasonic sensors
 *  and one IR sensor) - when any of the three sensors go off, the code detects that an object
 *  has been placed in the bin.
 *  Initially, it is assumed the bin does not have an item in it (so a baseline reading can be taken
 *  to calibrate ultrasonic sensors).
 *  Basic ultrasonic sensor code obtained from https://www.tutorialspoint.com/arduino/arduino_ultrasonic_sensor.htm
 *  
 *  Arsoja Green Solutions
 *  Date: March 10, 2020
 */

const int pingPin1 = 9; // trigger pin of first ulrasonic sensor
const int echoPin1 = 8; // echo pin of first ultrasonic sensor
const int pingPin2 = 5; // trigger pin of second ultrasonic sensor
const int echoPin2 = 4; // echo pin of second ultrasonic sensor
const int irPin = 3; // pin connected to IR sensor
// Prior to calibration, we set our baseline readings to 0cm
long basecm1 = 0;
long basecm2 = 0;


void setup() {
  Serial.begin(9600); // Starting serial terminal

  // Setting pins for both ultrasonic sensors
  pinMode(pingPin1, OUTPUT);
  pinMode(pingPin2, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(echoPin2, INPUT);

  // Setting input pin for IR sensor
  pinMode(irPin, INPUT);
  digitalWrite(irPin, HIGH); // turn on the pullup
}

void loop() {
  long duration1, cm1, duration2, cm2; // Variables to record distance measured by both ultrasonic sensors 

  //Sensor 1
  digitalWrite(pingPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin1, LOW);
  duration1 = pulseIn(echoPin1, HIGH);

  delayMicroseconds(1000);
  
  //Sensor 2
  digitalWrite(pingPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin2, LOW);
  duration2 = pulseIn(echoPin2, HIGH);

  // Obtaining distance measured by both ultrasonic sensors. If first measurement, we set this as our baseline measurement
  if (basecm1 == 0)
  {
    basecm1 = microsecondsToCentimeters(duration1);
    basecm2 = microsecondsToCentimeters(duration2);
  }
  cm1 = microsecondsToCentimeters(duration1);
  cm2 = microsecondsToCentimeters(duration2);

  // If there has been a change in the distance measured by either sensor, we detect that object has been placed in bin
//  if (abs(cm1-basecm1) > 2)
//  {
//    Serial.print("Object is detect by ultrasonic sensor 1: new reading is ");
//    Serial.print(cm1);
//    Serial.println("cm.");
//  }
//  else if (abs(cm2-basecm2) > 2)
//  {
//    Serial.print("Object is detect by ultrasonic sensor 2: new reading is ");
//    Serial.print(cm2);
//    Serial.println("cm.");
//  }
  if (digitalRead(irPin) == LOW)
  {
    Serial.println("Object detected by IR sensor");
  }
  delay(1000);
}

long microsecondsToCentimeters(long microseconds) {
  return microseconds / 29 / 2;
}
