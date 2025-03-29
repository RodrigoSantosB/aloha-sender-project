#include <SPI.h>
#include <LoRa.h>

String inString = "";    // string de leitura
int dadoRecebido = 0;
int valorRssi = 0;
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
    // Lê pacote
    while (LoRa.available())
    {
      int inChar = LoRa.read();
      inString += (char)inChar;
      dadoRecebido = inString.toInt();  // Converte para Int
    }
    inString = "";
    valorRssi = LoRa.packetRssi();
  }
  Serial.print("Dado Recebido: ");
  Serial.print(dadoRecebido);  // Imprime na Serial o valor recebido
  Serial.print("; Sinal: ");
  Serial.println(valorRssi);  // Imprime na Serial a intensidade do sinal
  delay(10);
}