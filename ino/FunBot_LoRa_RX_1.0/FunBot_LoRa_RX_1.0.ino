#include <SPI.h>
#include <LoRa.h>

#define LORA_FREQUENCY 915E6  
#define PAYLOAD_SIZE 102      

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
  while (Serial.available()==0){
  }  
  byte payload[PAYLOAD_SIZE];
  Serial.readBytes(payload, PAYLOAD_SIZE); // Read entire payload

  Serial.write("ACK");

  // 🔻 Uncomment if you want LoRa transmission 🔻
  // LoRa.beginPacket();
  // LoRa.write(index);
  // LoRa.write(sequence_number);
  // LoRa.write(payload, PAYLOAD_SIZE);
  // LoRa.endPacket();
}
