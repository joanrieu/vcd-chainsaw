void setup()
{
  // start serial port at 115200 bps
  Serial.begin(115200);
  for(int i=2; i <10; ++i) {
    pinMode(i, INPUT);
  }
  digitalWrite(7, 1);
}

void loop()
{
  int value = 0;
  for(int i=7; i>=0; --i) {
    value = (value<<1) | digitalRead(i+2);
  }
    Serial.print(value);
    Serial.print("\n");
}
