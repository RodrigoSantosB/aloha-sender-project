#include <SPI.h>
#include <LoRa.h>

#define LORA_FREQUENCY 915E6  // Frequência LoRa
#define PAYLOAD_SIZE 102      // Tamanho do payload

int counter = 0;
byte expected_index = 0;
byte expected_sequence_number = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);  // Aguarda a Serial inicializar
  Serial.println("Transmissor LoRa");

  if (!LoRa.begin(LORA_FREQUENCY)) {
    Serial.println("Falha em iniciar o LoRa!");
    while (1);
  }
}

void loop() {
  Serial.println("Waiting for message...");
  if (Serial.available() >= (2 + PAYLOAD_SIZE)) {
    Serial.println("Received Message");

    byte index = Serial.read();
    byte sequence_number = Serial.read();
    byte payload[PAYLOAD_SIZE];

    for (int i = 0; i < PAYLOAD_SIZE; i++) {
      payload[i] = Serial.read();
    }

    if (index == expected_index && sequence_number == expected_sequence_number) {
      expected_index++;
      expected_sequence_number++;
      Serial.println("Transmitting...");

      LoRa.beginPacket();
      LoRa.write(index);
      LoRa.write(sequence_number);
      LoRa.write(payload, PAYLOAD_SIZE);
      LoRa.endPacket();

      Serial.println("Packet Sent!");

      // **Send ACK back via Serial**
      Serial.write(index);               // Send back the received index
      Serial.write(sequence_number);     // Send back the received sequence number
    } else {
      Serial.println("Erro: Índice ou sequência inválidos!");
    }
  }

  delay(1000);
}
