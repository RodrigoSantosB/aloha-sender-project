#include <SPI.h>
#include <LoRa.h>

String mensagem = ""; // Variável para armazenar a mensagem recebida

void setup() {
  Serial.begin(9600);
  
  // Inicializa comunicação serial com o Python
  while (!Serial);
  
  Serial.println("Transmissor LoRa");
  if (!LoRa.begin(433E6)) { // Frequência de operação (915E6 / 433E6)
    Serial.println("Falha em iniciar o LoRa!");
    while (1);
  }
}

void loop() {
  // Verifica se há dados disponíveis na serial
  if (Serial.available() > 0) {
    mensagem = Serial.readStringUntil('\n'); // Lê a string até encontrar quebra de linha
    mensagem.trim(); // Remove espaços em branco extras
    
    Serial.print("Mensagem recebida: ");
    Serial.println(mensagem);
  }

  // Se houver uma mensagem válida, envia via LoRa
  if (mensagem.length() > 0) {
    LoRa.beginPacket();
    LoRa.print(mensagem);
    LoRa.endPacket();
    
    Serial.print("Mensagem enviada via LoRa: ");
    Serial.println(mensagem);
    
    delay(1000); // Intervalo entre transmissões
  }
}