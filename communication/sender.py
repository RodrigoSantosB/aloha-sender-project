import serial
import time
import speech_recognition as sr
import sounddevice as sd
import pyaudio
from pydub import AudioSegment
import wave
import io

PAYLOAD_SIZE = 62
SERIAL_PORT = "/dev/ttyACM0" 
BAUD_RATE = 9600
AUDIO_PATH = "/home/lucas/ALOHA/aloha-sender-project/audios/alou_world.mp3"

class Sender():
    def __init__(self):
        self.ser = serial.Serial(baudrate=BAUD_RATE, timeout=2)
        self.ser.port = SERIAL_PORT

    def send_string(self, text):
        self.ser.open()
        try:
            self.ser.write(text.encode()) 
            print(f"Message Sent: {text}")
            time.sleep(0.1)  
            ack_received = False
            start_time = time.time()
            while time.time() - start_time < 5:  
                if self.ser.in_waiting > 0:  
                    ack = self.ser.readline().decode().strip()  
                    print(f"Received: {ack}")
                    if ack == "ACK":
                        ack_received = True
                        break
        except serial.SerialException as e:
            print(f"Serial communication error: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        self.ser.close()
        
    def send_file_audio(self):
        try:
            with open(AUDIO_PATH, "rb") as audio_file:
                audio_bytes = audio_file.read() 
                print(f"Sent {len(audio_bytes)} bytes")
        except Exception as e:
            print(f"Error: {e}")
            
        packets = self.packet_generator(audio_bytes)
        self.transmit_packets(packets)
        
    def send_recorded_audio(self):
        print("Recording audio...")
        mic = sr.Recognizer()
        with sr.Microphone() as source:
            mic.adjust_for_ambient_noise(source)
            print("Escutando...")
            audio = mic.record(source, duration=2)
            audio_bytes = audio.get_wav_data()
            compressed_audio = self.compress_audio(audio_bytes)
            packets = self.packet_generator(compressed_audio)
            print(f"Total Packets: {len(packets)}")
            self.transmit_packets(packets)
            self.ser.write(b"END")
            
    def compress_audio(self, audio_bytes):
        audio_bytes = io.BytesIO(audio_bytes)
        audio = AudioSegment.from_raw(audio_bytes, sample_width=2, frame_rate=16000, channels=1)
        audio = audio.set_frame_rate(4000).set_sample_width(1)  # 4kHz, 8-bit PCM
        return audio.raw_data

    def packet_generator(self, audio_bytes):
        packets = []
        num_packets = (len(audio_bytes) + PAYLOAD_SIZE - 1) // PAYLOAD_SIZE

        for i in range(num_packets):
            packet_payload = audio_bytes[i * PAYLOAD_SIZE: (i + 1) * PAYLOAD_SIZE]
            packets.append(packet_payload)
            
        return packets
    
    def send_packet(self, packet):
        self.ser.write(packet)
        # **Wait for ACK**
        ack_received = False
        start_time = time.time()
        while time.time() - start_time < 5:  
            if self.ser.in_waiting > 0:  
                ack = self.ser.readline().decode().strip()  
                if ack == "ACK":
                    print(f"Packet sent successfully")
                    ack_received = True
                    break
        if not ack_received:
            raise serial.SerialTimeoutException
        

    def transmit_packets(self, packets):
        self.ser.open()
        try:
            print("Transmitting packets...")
            for i, packet in enumerate(packets): 
                try:
                    self.send_packet(packet)
                except(serial.SerialTimeoutException) as e:
                    print(f"Error transmitting packet {i}: {str(e)}")
                    self.send_packet(packet)

            print("Transmission complete")
        except serial.SerialException as e:
            print(f"Serial communication error: {str(e)}")
        except Exception as e:
            print(f"An error occurred during transmission: {str(e)}")
        self.ser.close()
