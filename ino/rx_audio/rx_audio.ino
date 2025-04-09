#include <SPI.h>
#include <LoRa.h>

// byte message[62] = {}; // Armazena a string recebida
int valorRssi = 0;  // Intensidade do sinal
/*
  Received Signal Strength Indication
  RSSI=-30dBm: sinal forte.
  RSSI=-120dBm: sinal fraco.
*/

void setup() {
  Serial.begin(9600);

  while (!Serial);
  Serial.println("Receptor LoRa");
  if (!LoRa.begin(433E6)) {       // Frequencia de operação (ou 915E6)
    Serial.println("Falha em iniciar o LoRa!");
    while (1);
  }
}

void loop() {
  // Tenta receber pacote de dados
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    byte message[62] = {};;  // Limpa a string anterior
    
    // Lê pacote caractere por caractere
    int i = 0;
    while (LoRa.available()) {
      byte packet_byte = (byte)LoRa.read();
      message[i] = packet_byte;
      i += 1;
    }
    
    valorRssi = LoRa.packetRssi();  // Obtém a intensidade do sinal

    // Imprime os dados recebidose
    Serial.print("Mensagem Recebida: ");
    
    for (int i  = 0; i < sizeof(message); i++){
     Serial.print(message[i]);
    }

    Serial.write(message, i);

    Serial.print(" | Sinal: ");
    Serial.print(valorRssi);
    Serial.println(" dBm");
  }
  
  delay(10);  // Pequeno delay para evitar sobrecarga
}