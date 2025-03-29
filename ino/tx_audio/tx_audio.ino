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
  while (Serial.available()==0){
  }  
  byte payload[PAYLOAD_SIZE];
  
  Serial.read(payload, PAYLOAD_SIZE); // Read entire payload

  Serial.write("ACK");

  LoRa.beginPacket();
  LoRa.write(payload, PAYLOAD_SIZE);
  LoRa.endPacket();
}
