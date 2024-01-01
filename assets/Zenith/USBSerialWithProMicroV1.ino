void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
}

void loop() {
  byte b;
  if (Serial1.available() > 0) {
    b = Serial1.read();
    Serial.write(b);
  }
  if (Serial.available() > 0) {
    b = Serial.read();
    Serial1.write(b);
  }
}
