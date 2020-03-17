/* Code used to get calibration scale factor to use for weight sensor
 *  This scale factor will likely need to be changed any time the mechanical 
 *  configuration of the load cell is changed.
 *  
 *  Reference: https://www.brainy-bits.com/load-cell-and-hx711-with-arduino/
 *  
 *  Arsoja Green Solutions
 *  March 17, 2020
 */

#include "HX711.h"

#define DOUT 6 // Arduino pin 6 connect to HX711 DOUT
# define CLK 5 // Arduino pin 5 connect to HX711 CLK

HX711 scale; // Init of library 

void setup() {
   Serial.begin(9600);
   scale.begin(DOUT, CLK);
   scale.set_scale();   // Start scale
   scale.tare();        // Reset scale to zero
}

void loop() {
  float current_weight = scale.get_units(20);   // Get average of 20 scale readings
  float scale_factor=(current_weight/0.194);    // Divide the result by a known weight --> iPhone XR = 194g
  Serial.println(scale_factor);  // Print the scale factor to use --> for iPhone XR = -113861

}
