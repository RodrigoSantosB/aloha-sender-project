#include <SPI.h>  // Include the SPI library for communication
#include <LoRa.h> // Include the LoRa library for LoRa communication

// Define the LoRa frequency (915 MHz for this example)
#define LORA_FREQUENCY 915E6  

// Define the payload size for the LoRa transmission
#define PAYLOAD_SIZE 62

// Setup function runs once when the program starts
void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  pinMode(LED_BUILTIN, OUTPUT); // Set the built-in LED pin as an output
  while (!Serial);  // Wait for the Serial port to be ready
  
  // Initialize LoRa communication
  if (!LoRa.begin(LORA_FREQUENCY)) {
    Serial.println("LoRa initialization failed!"); // Print error message if LoRa fails
    while (1); // Halt the program if initialization fails
  }
}

// Function to clear the serial buffer
void clearSerialBuffer(){
  while(Serial.available() > 0){ // While there is data in the serial buffer
    Serial.read(); // Read and discard the data
  }
}

// Main loop function runs repeatedly
void loop() {
  // Attempt to receive a data packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) { // If a packet is received
    uint8_t payload[PAYLOAD_SIZE];  // Array to store the payload

    // Read the payload byte by byte
    for (int i = 0; i < PAYLOAD_SIZE; i++) {
        if (LoRa.available()) { // Check if data is available in the LoRa buffer
            payload[i] = LoRa.read();  // Read one byte from the LoRa buffer
        }
    }

    // Get the signal strength (RSSI) of the received packet
    int SRssi = LoRa.packetRssi();

    // Print the payload as a comma-separated list
    Serial.print(",");
    for (int i = 0; i < PAYLOAD_SIZE; i++) {
        Serial.print(payload[i]); // Print each byte of the payload
        if (i < PAYLOAD_SIZE - 1) Serial.print(",");  // Add a comma between bytes
    }
    Serial.print(",");  
  }

  // Wait until data is available on the Serial port
  while (Serial.available() == 0){
  }  
  
  // Create a byte array to store the payload for transmission
  byte payload[PAYLOAD_SIZE];
  
  // Read PAYLOAD_SIZE bytes from the Serial input
  for (int i = 0; i < PAYLOAD_SIZE; i++) {
    Serial.println(i); // Print the current index for debugging
    while (!Serial.available());  // Wait until a byte is available
    payload[i] = Serial.read();   // Read one byte at a time
  }

  // Clear any remaining data in the Serial buffer
  clearSerialBuffer();

  // Send an acknowledgment message back via Serial
  Serial.write("ACK");

  // Begin a LoRa packet
  LoRa.beginPacket();
  LoRa.write(payload, PAYLOAD_SIZE); // Write the payload to the LoRa packet
  LoRa.endPacket(); // End and send the LoRa packet
}