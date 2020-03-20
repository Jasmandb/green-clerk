/* Code to print load cell weight measurement in grams.
 *  To get an accurate reading, a calibration factor must be obtained from Scale_Calibration
 *  sketch.
 *  
 *  Reference: https://www.brainy-bits.com/load-cell-and-hx711-with-arduino/
 *  
 *  Arsoja Green Solutions
 *  March 17, 2020
 */

#include "HX711.h"

#define DOUT 6 // Arduino pin 6 connect to HX711 DOUT
#define CLK 5 // Arduino pin 5 connect to HX711 CLK

HX711 scale; // Init of library 

void setup() {
   Serial.begin(9600);
   scale.begin(DOUT, CLK);
   scale.set_scale();        // Start scale
   scale.set_scale(-113861); // Calibration Factor obtained from calibration sketch
   scale.tare();             // Reset the scale to 0  
}

void loop() {
  Serial.print(scale.get_units(20)*1000, 2); // Print average of 20 scale readings in grams
  Serial.println("g");
}
