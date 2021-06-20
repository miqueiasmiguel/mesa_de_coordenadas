int python_data = 1;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

}

void serialEvent() {
  while(Serial.available() > 0){
    python_data = Serial.readString().toInt();
    Serial.print(python_data + 1);
  }
}
