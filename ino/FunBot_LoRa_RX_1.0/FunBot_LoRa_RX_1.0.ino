/*
      Programa Transmissor LoRa Simples

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

int counter = 0;

void setup() {
  Serial.begin(9600);

  while (!Serial);
  Serial.println("Transmissor LoRa");
  if (!LoRa.begin(915E6)) {           // Frequencia de operação (ou 915E6)
    Serial.println("Falha em iniciar o LoRa!");
    while (1);
  }
}

void loop() {
  counter++;
  LoRa.beginPacket();
  LoRa.print(counter);
  LoRa.endPacket();
  delay(1000);
}