#include <Servo.h>             //Servo library
 
Servo servo_test;        //initialize a servo object for the connected servo  
                
int angle = 0;  

//pulselengths for different angles
int Deg0 = 500;
int Deg90 = 1100;
int Deg180 = 1650
int Deg270 = 2150;
 
void setup() 
{ 
  servo_test.attach(9);      // attach the signal pin of servo to pin9 of arduino
} 
  
void loop() 
{ 

  //forward: moves at ~90 deg/sec
  for(angle = Deg0; angle < Deg90; angle += 6)    // command to move from 0 degrees to 90 degrees 
  {                                  
    servo_test.writeMicroseconds(angle);                 //command to rotate the servo to the specified angle
    delay(10);                       
  } 
 
  delay(1000);
  
  for(angle = Deg90; angle<Deg180; angle+=6)     // command to move from 90 degrees to 180 degrees 
  {                                
    servo_test.writeMicroseconds(angle);              //command to rotate the servo to the specified angle
    delay(10);                       
  } 

    delay(1000);
    
     for(angle = Deg180; angle < Deg270; angle += 6)    // command to move from 180 degrees to 270 degrees 
  {                                  
    servo_test.writeMicroseconds(angle);                 //command to rotate the servo to the specified angle
    delay(10);                       
  } 
 
  delay(1000);



  //reverse: moves at ~90 deg/sec
    for(angle = Deg270; angle > Deg180; angle -= 6)    // command to move from 270 degrees to 180 degrees 
  {                                  
    servo_test.writeMicroseconds(angle);                 //command to rotate the servo to the specified angle
    delay(10);                       
  } 
 
  delay(1000);

      for(angle = Deg180; angle > Deg90; angle -= 6)    // command to move from 180 degrees to 90 degrees 
  {                                  
    servo_test.writeMicroseconds(angle);                 //command to rotate the servo to the specified angle
    delay(10);                       
  } 
 
  delay(1000);

      for(angle = Deg90; angle > Deg0; angle -= 6)    // command to move from 90 degrees to 0 degrees 
  {                                  
    servo_test.writeMicroseconds(angle);                 //command to rotate the servo to the specified angle
    delay(10);                       
  } 
 
  delay(1000);
}
