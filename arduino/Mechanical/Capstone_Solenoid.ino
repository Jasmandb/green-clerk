int relay_pin = 7;

void setup() {
  // put your setup code here, to run once:
  pinMode(relay_pin,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(relay_pin,HIGH);//lock out
  delay(5000);
  digitalWrite(relay_pin,LOW);//lock in
  delay(500);
}
