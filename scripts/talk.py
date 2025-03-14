import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import pyaudio
import wave
import io
import serial


PAYLOAD_SIZE = 102
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

def talk():
    mic = sr.Recognizer()

    with sr.Microphone() as source:
        
        print(source)
        mic.adjust_for_ambient_noise(source)
        
        # Armazena o audio
        print("Escutando...")
        audio = mic.record(source, duration=8)
        print("1...")
        audio_bytes = audio.get_wav_data()
        print("2...")
        packets = packet_generator(audio_bytes)
        print("3...")
        transmit_packets(packets)
        print("4...")
        
    return None

        
def packet_generator(audio_bytes):
    packet_audio = []
    num_packets = (len(audio_bytes) + PAYLOAD_SIZE - 1)

    for i in range(num_packets):
        packet_payload = audio_bytes[i * PAYLOAD_SIZE: (i + 1) * PAYLOAD_SIZE]
        packet_audio.append(packet_payload)
        
    return packet_audio
        
def transmit_packets(packets):
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        print("Transmitting packets...")
        sequence_number = 0  # Initialize the sequence number
        for i, packet in enumerate(packets):
            sequence_number += 1  # Increment the sequence number
            index = i.to_bytes(1, byteorder='big')
            ser.write(index)  # Send the index
            ser.write(sequence_number.to_bytes(1, byteorder='big'))  # Send the sequence number
            ser.write(packet)
            # ...
            
            # Wait for acknowledgement
            while True:
                if ser.readable() and ser.in_waiting >= 2:  # Wait for index and sequence number
                    received_index = ord(ser.read())
                    received_sequence_number = ord(ser.read())
                    if received_index == i and received_sequence_number == sequence_number:
                        print(f"Acknowledged packet: Index={received_index}, Sequence Number={received_sequence_number}")
                        break  # Acknowledgement received, move to the next packet
                # ...
            
            # ...
        ser.close()
        print("Transmission complete")
    except serial.SerialException as e:
        print(f"Serial communication error: {str(e)}")
    except Exception as e:
        print(f"An error occurred during transmission: {str(e)}")