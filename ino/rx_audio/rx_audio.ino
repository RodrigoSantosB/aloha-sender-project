/*
      Programa Receptor LoRa Simples

      Componentes:
        - Arduino Uno;
        - Módulo LoRa XL1278-SMT;

      Versão 1.0 - Versão inicial - 09/Out/2021

 *    * Criado por Cleber Borges - FunBots - @cleber.funbots  *     *

      Instagram: https://www.instagram.com/cleber.funbots/
      Facebook: https://www.facebook.com/cleber.funbots
      YouTube: https://www.youtube.com/channel/UCKs2l5weIqgJQxiLj0A6Atw
      Telegram: https://t.me/cleberfunbots

*/

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
  if (!LoRa.begin(915E6)) {       // Frequencia de operação (ou 915E6)
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