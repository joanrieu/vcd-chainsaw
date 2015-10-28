void setup()
{
  // start serial port at 115200 bps
  Serial.begin(115200);
  for(int i=0; i <8; ++i) {
    pinMode(i, INPUT);
  }
}

void loop()
{
  int sensor[8];
  int value = 0;
  for(int i=7; i>=0; --i) {
    value = (value<<1) | digitalRead(i);
  }
    Serial.print(value);
    Serial.print("\n");
}
