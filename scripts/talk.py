import serial
import time
import speech_recognition as sr

PAYLOAD_SIZE = 102
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

def talk():
    mic = sr.Recognizer()
    with sr.Microphone() as source:
        mic.adjust_for_ambient_noise(source)
        print("Escutando...")
        audio = mic.record(source, duration=8)
        audio_bytes = audio.get_wav_data()
        packets = packet_generator(audio_bytes)
        transmit_packets(packets)

def packet_generator(audio_bytes):
    packets = []
    num_packets = (len(audio_bytes) + PAYLOAD_SIZE - 1) // PAYLOAD_SIZE

    for i in range(num_packets):
        packet_payload = audio_bytes[i * PAYLOAD_SIZE: (i + 1) * PAYLOAD_SIZE]
        packets.append(packet_payload)
        
    return packets

def transmit_packets(packets):
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)  # Added timeout
        print("Transmitting packets...")

        sequence_number = 0  
        for i, packet in enumerate(packets):
            sequence_number += 1  
            index = i.to_bytes(1, byteorder='big')
            seq_number = sequence_number.to_bytes(1, byteorder='big')

            ser.write(index)  
            ser.write(seq_number)  
            ser.write(packet)

            # **Wait for Acknowledgment from Arduino**
            ack_received = False
            start_time = time.time()
            while time.time() - start_time < 2:  # Wait max 2 seconds
                if ser.in_waiting >= 2:
                    received_index = ord(ser.read())
                    received_sequence_number = ord(ser.read())

                    if received_index == i and received_sequence_number == sequence_number:
                        print(f"Acknowledged: Index={received_index}, Sequence Number={received_sequence_number}")
                        ack_received = True
                        break  

            if not ack_received:
                print(f"ACK Timeout: Packet {i} not acknowledged!")

        ser.close()
        print("Transmission complete")
    except serial.SerialException as e:
        print(f"Serial communication error: {str(e)}")
    except Exception as e:
        print(f"An error occurred during transmission: {str(e)}")
