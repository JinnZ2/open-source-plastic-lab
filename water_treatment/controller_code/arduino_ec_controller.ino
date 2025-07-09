// Electrocoagulation Controller - RaccoonForge Edition
// Controls DC voltage, switches polarity, monitors turbidity & pH

const int VOLTAGE_CONTROL = 9;      // PWM control pin
const int CURRENT_SENSOR = A0;
const int PH_SENSOR = A1;
const int TURBIDITY_SENSOR = A2;
const int RELAY_POLARITY = 7;

float targetCurrent = 2.0; // Amps
unsigned long polarityTimer = 0;
bool polarityState = false;

void setup() {
  pinMode(VOLTAGE_CONTROL, OUTPUT);
  pinMode(RELAY_POLARITY, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  float current = analogRead(CURRENT_SENSOR) * 0.0264;
  float ph = analogRead(PH_SENSOR) * 0.0137 + 3.5;
  float turbidity = analogRead(TURBIDITY_SENSOR);

  int pwmValue = constrain((targetCurrent - current) * 50 + 128, 0, 255);
  analogWrite(VOLTAGE_CONTROL, pwmValue);

  if (millis() - polarityTimer > 300000) {
    polarityState = !polarityState;
    digitalWrite(RELAY_POLARITY, polarityState);
    polarityTimer = millis();
  }

  if (turbidity < 100) {
    Serial.println("Treatment complete!");
  }

  delay(1000);
}
