// #include <SPI.h>
// #include <LoRa.h>

// int counter = 0;

// void setup() {
//   Serial.begin(9600);

//   while (!Serial);
//   Serial.println("Transmissor LoRa");
//   if (!LoRa.begin(433E6)) {           // Frequencia de operação (ou 915E6)
//     Serial.println("Falha em iniciar o LoRa!");
//     while (1);
//   }
// }

// void loop() {
//   counter++;
//   LoRa.beginPacket();
//   LoRa.print(counter);
//   LoRa.endPacket();
//   delay(1000);
// }