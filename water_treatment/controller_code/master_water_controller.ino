// Master Water Treatment Controller - Forest Lab Edition
// Controls full water recovery train across 6 stages

#include <Wire.h>

#define I2C_ADDRESS 0x16

struct WaterData {
  float turbidity;
  float ph;
  float conductivity;
  float temperature;
  float flowRate;
  int treatmentStage;
  float microplasticsRecovered;
  float powerGenerated;
} waterData;

// Hardware Pin Mapping
const int PUMP_PINS[4] = {5, 6, 7, 8};
const int VALVE_PINS[6] = {22, 23, 24, 25, 26, 27};
const int UV_LAMP = 9;
const int H2O2_PUMP = 10;

// Sensors
const int TURBIDITY_PIN = A0;
const int PH_PIN = A1;
const int CONDUCTIVITY_PIN = A2;
const int FLOW_PIN = 2;

volatile int flowPulses = 0;
unsigned long lastFlowCheck = 0;

void setup() {
  Wire.begin(I2C_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);

  for (int i = 0; i < 4; i++) pinMode(PUMP_PINS[i], OUTPUT);
  for (int i = 0; i < 6; i++) pinMode(VALVE_PINS[i], OUTPUT);
  
  pinMode(UV_LAMP, OUTPUT);
  pinMode(H2O2_PUMP, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(FLOW_PIN), flowPulse, RISING);
  Serial.begin(9600);
}

void loop() {
  static int stage = 0;
  static unsigned long stageTimer = 0;
  
  updateSensors();

  switch(stage) {
    case 0: // Filling
      digitalWrite(VALVE_PINS[0], HIGH);
      if (waterData.flowRate < 0.1 && millis() - stageTimer > 5000) {
        digitalWrite(VALVE_PINS[0], LOW);
        stage = 1;
        stageTimer = millis();
      }
      break;

    case 1: // Electrocoagulation
      digitalWrite(PUMP_PINS[0], HIGH);
      if (millis() - stageTimer > 1800000) {
        digitalWrite(PUMP_PINS[0], LOW);
        stage = 2;
        stageTimer = millis();
      }
      break;

    case 2: // Settling
      if (millis() - stageTimer > 600000) {
        stage = 3;
        stageTimer = millis();
      }
      break;

    case 3: // Magnetic separation
      digitalWrite(PUMP_PINS[1], HIGH);
      digitalWrite(VALVE_PINS[1], HIGH);
      if (waterData.turbidity < 50) {
        digitalWrite(PUMP_PINS[1], LOW);
        digitalWrite(VALVE_PINS[1], LOW);
        stage = 4;
        stageTimer = millis();
      }
      break;

    case 4: // Bio-electrochemical cell
      digitalWrite(PUMP_PINS[2], HIGH);
      digitalWrite(VALVE_PINS[2], HIGH);
      if (millis() - stageTimer > 3600000) {
        stage = 5;
        stageTimer = millis();
      }
      break;

    case 5: // Advanced oxidation
      digitalWrite(UV_LAMP, HIGH);
      digitalWrite(H2O2_PUMP, HIGH);
      digitalWrite(PUMP_PINS[3], HIGH);
      if (millis() - stageTimer > 900000) {
        digitalWrite(UV_LAMP, LOW);
        digitalWrite(H2O2_PUMP, LOW);
        stage = 6;
        stageTimer = millis();
      }
      break;

    case 6: // Discharge
      digitalWrite(VALVE_PINS[5], HIGH);
      if (waterData.flowRate < 0.1) {
        digitalWrite(VALVE_PINS[5], LOW);
        stage = 0;
        waterData.microplasticsRecovered += 25;
      }
      break;
  }

  waterData.treatmentStage = stage;
  delay(100);
}

void updateSensors() {
  waterData.turbidity = analogRead(TURBIDITY_PIN);
  waterData.ph = analogRead(PH_PIN) * 0.0137 + 3.5;
  waterData.conductivity = analogRead(CONDUCTIVITY_PIN) * 2.0;

  if (millis() - lastFlowCheck > 1000) {
    waterData.flowRate = flowPulses * 2.25;
    flowPulses = 0;
    lastFlowCheck = millis();
  }
}

void flowPulse() {
  flowPulses++;
}

void requestEvent() {
  Wire.write((byte*)&waterData, sizeof(waterData));
}

void receiveEvent(int numBytes) {
  // Reserved for command receipt
}
