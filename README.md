# 📡 Projeto de Transmissão de Áudio via Módulo LoRa SX1276 (915 MHz)

Este projeto investiga a **viabilidade da transmissão de áudio** utilizando módulos **LoRa SX1276** operando em 915 MHz. A proposta envolve compressão e envio segmentado de amostras de áudio por LoRa, com foco em **eficiência energética, longo alcance e baixo custo, o diagrama do projeto se encontra abaixo, mostrando o setup utilizado**.

---

## ⚙️ Setup



## ⚙️ Requisitos

- Python 3.10
- Módulos LoRa SX1276 conectados via SPI (Arduino) com interface python
- Microfone e alto-falante (para captura e reprodução do áudio - Notebook)
- `virtualenv` (opcional, mas recomendado)

---

## 🧪 Criação do Ambiente Virtual

Para garantir a compatibilidade, o ambiente Python deve ser 3.10. Você pode usar o `venv` para isolar o projeto:

```bash
python3.10 -m venv venv
source venv/bin/activate

## 📦 Instalação das Dependências

Certifique-se de estar com o ambiente ativado e execute:

```bash
pip install -r requirements.txt
```
---

## 🚀 Execução Automática via Script `.sh`

### 1. `install.sh` — Criar ambiente instalar dependências
Dê permissão de execução:

```bash
chmod +x install.sh
```

E então execute:

```bash
./install.sh
```
---

## 🔁 Pipeline de Execução

### Envio e Recepção (`main.py`)
1. Captura de áudio via microfone (streaming com `pyaudio`)
2. Compressão ou segmentação dos dados 
3. Envio dos dados por LoRa (UART)
4. Recebimento contínuo de pacotes de áudio via LoRa
5. Decodificação / reconstrução dos dados
6. Reprodução do áudio no alto-falante (streaming ou em buffer)

Ao executar a `main.py` um menu será exibido mostrando as opções de sender ou received. 
---

## 📌 Observações
- Deve-se ter dois arduinos disponivel, uma para funcionar como transmissor e outro como receptor. Os script de cada um está disponível no módulo em questão. Basta realizar o upload.

- O tempo de transmissão e a qualidade do áudio dependem fortemente do **Spreading Factor**, **BW**, e técnicas de compressão utilizadas.

- Este projeto é experimental e visa validar a **prova de conceito** de comunicação por voz sobre LoRa.

---

## 🧠 Futuro

- Implementação de **codec Speex** ou **Opus** com parâmetros ajustados para baixa taxa de bits.
- Transmissão full-duplex com canais alternados.
- Controle de retransmissão para melhorar robustez.

---

## 📄 Licença

MIT License

---

Desenvolvido com 💻 e 📡 por Rodrigo Santos Batista / Lucas Alexandre de Carvalho Paiva
```