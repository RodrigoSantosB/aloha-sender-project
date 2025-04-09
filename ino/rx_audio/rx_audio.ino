#include <SPI.h>  // Include the SPI library for communication
#include <LoRa.h> // Include the LoRa library for LoRa communication

int valorRssi = 0;  // Signal strength (RSSI)
/*
  Received Signal Strength Indication (RSSI)
  RSSI = -30dBm: strong signal.
  RSSI = -120dBm: weak signal.
*/

int count = 0; // Counter variable (currently unused)

// Setup function runs once when the program starts
void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate

  while (!Serial); // Wait for the Serial port to be ready
  if (!LoRa.begin(915E6)) { // Initialize LoRa communication at 915 MHz
    Serial.println("Falha em iniciar o LoRa!"); // Print error message if LoRa fails
    while (1); // Halt the program if initialization fails
  }
}

// Main loop function runs repeatedly
void loop() {
  // Attempt to receive a data packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) { // If a packet is received
    byte message[62] = {}; // Clear the previous message buffer

    // Read the packet byte by byte
    int i = 0; // Index for the message array
    while (LoRa.available()) { // While there is data in the LoRa buffer
      byte packet_byte = (byte)LoRa.read(); // Read one byte from the LoRa buffer
      message[i] = packet_byte; // Store the byte in the message array
      i += 1; // Increment the index
    }

    // Get the signal strength (RSSI) of the received packet
    valorRssi = LoRa.packetRssi();

    // Send the received message back via Serial
    Serial.write(message, i);
  }
}