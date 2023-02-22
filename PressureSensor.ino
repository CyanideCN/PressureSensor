#include <Wire.h>
#include <Adafruit_BMP085.h>

#define seaLevelPressure_hPa 1013.25

Adafruit_BMP085 bmp;
 
void setup() {
 Serial.begin(9600);
 if (!bmp.begin(BMP085_ULTRAHIGHRES))
 {
   Serial.println("Can't connect to sensor");
   while (1) {}
 }
}

void loop() {
   Serial.println(bmp.readPressure());
   //Serial.println(bmp.readTemperature());
   delay(80);
}
