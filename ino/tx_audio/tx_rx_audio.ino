#include <SPI.h>
#include <LoRa.h>

#define LORA_FREQUENCY 915E6  
#define PAYLOAD_SIZE 62      

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  while (!Serial);  
  if (!LoRa.begin(LORA_FREQUENCY)) {
    Serial.println("LoRa initialization failed!");
    while (1);
  }
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    uint8_t payload[PAYLOAD_SIZE];  // Array to store payload
    for (int i = 0; i < PAYLOAD_SIZE; i++) {
        if (LoRa.available()) {
            payload[i] = LoRa.read();  // Read payload bytes
        }
    }
    int SRssi = LoRa.packetRssi();  // get signal intensity
    Serial.print(",");
    for (int i = 0; i < PAYLOAD_SIZE; i++) {
        Serial.print(payload[i]);
        if (i < PAYLOAD_SIZE - 1) Serial.print(",");  // Comma-separated
    }
    Serial.print(",");  
  }


  while (Serial.available()==0){
  }  
  byte payload[PAYLOAD_SIZE];
  
  for (int i = 0; i < PAYLOAD_SIZE; i++) {
    while (!Serial.available());  // Aguarda até que um byte esteja disponível
    payload[i] = Serial.read();   // Lê um byte por vez
  }

  Serial.write("ACK");

  // 🔻 Uncomment if you want LoRa transmission 🔻
  // LoRa.beginPacket();
  // LoRa.write(payload, PAYLOAD_SIZE);
  // LoRa.endPacket();
}
