void setup() {
  Serial.begin(9600); // Inicializa a comunicação serial
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  while (Serial.available()==0){
  }
  String receivedMessage = Serial.readStringUntil('\r'); // Lê a string recebida
  if (receivedMessage == "ON"){
    Serial.write("ACK"); // Envia "ACK" sem nova linha
    digitalWrite(LED_BUILTIN,HIGH);
  }
  if (receivedMessage == "OFF"){
    Serial.write("ACK"); // Envia "ACK" sem nova linha
    digitalWrite(LED_BUILTIN,LOW);
  } 
}