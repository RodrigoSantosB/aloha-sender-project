# Importing necessary libraries
import serial  # For serial communication
import time  # For time-related operations
import speech_recognition as sr  # For recording audio from the microphone
import sounddevice as sd  # For audio playback (not used in this code)
from pydub import AudioSegment  # For audio manipulation
import io  # For handling in-memory byte streams

# Constants for serial communication and audio processing
PAYLOAD_SIZE = 62  # Size of each packet to send
SERIAL_PORT = "/dev/ttyACM0"  # Serial port to communicate with
BAUD_RATE = 9600  # Baud rate for serial communication
AUDIO_PATH = "/home/lucas/ALOHA/aloha-sender-project/audios/alou_world.mp3"  # Path to the audio file

# Sender class to handle sending data and audio over serial communication
class Sender():
    def __init__(self):
        # Initialize the serial connection
        self.ser = serial.Serial(baudrate=BAUD_RATE, timeout=2)  # Set baud rate and timeout
        self.ser.port = SERIAL_PORT  # Set the serial port

    def send_string(self, text):
        # Send a string message over the serial connection
        self.ser.open()  # Open the serial port
        try:
            self.ser.write(text.encode())  # Send the text as bytes
            print(f"Message Sent: {text}")  # Debug message
            time.sleep(0.1)  # Short delay to allow the receiver to process
            ack_received = False  # Flag to track if an acknowledgment (ACK) is received
            start_time = time.time()  # Record the start time
            while time.time() - start_time < 5:  # Wait for up to 5 seconds for an ACK
                if self.ser.in_waiting > 0:  # Check if data is available in the serial buffer
                    ack = self.ser.readline().decode().strip()  # Read and decode the response
                    print(f"Received: {ack}")  # Debug message
                    if ack == "ACK":  # Check if the response is an acknowledgment
                        ack_received = True
                        break
        except serial.SerialException as e:
            print(f"Serial communication error: {str(e)}")  # Handle serial communication errors
        except Exception as e:
            print(f"An error occurred: {str(e)}")  # Handle other errors
        self.ser.close()  # Close the serial port

    def send_file_audio(self):
        # Send an audio file over the serial connection
        try:
            with open(AUDIO_PATH, "rb") as audio_file:  # Open the audio file in binary mode
                audio_bytes = audio_file.read()  # Read the entire file as bytes
                print(f"Sent {len(audio_bytes)} bytes")  # Debug message
        except Exception as e:
            print(f"Error: {e}")  # Handle file-related errors
            
        packets = self.packet_generator(audio_bytes)  # Split the audio into packets
        self.transmit_packets(packets)  # Transmit the packets

    def send_recorded_audio(self):
        # Record audio from the microphone and send it
        print("Recording audio...")  # Debug message
        mic = sr.Recognizer()  # Initialize the speech recognizer
        with sr.Microphone() as source:  # Use the microphone as the audio source
            mic.adjust_for_ambient_noise(source)  # Adjust for background noise
            print("Listening...")  # Debug message
            audio = mic.record(source, duration=2)  # Record 2 seconds of audio
            audio_bytes = audio.get_wav_data()  # Get the audio data as WAV bytes
            compressed_audio = self.compress_audio(audio_bytes)  # Compress the audio
            packets = self.packet_generator(compressed_audio)  # Split the audio into packets
            print(f"Total Packets: {len(packets)}")  # Debug message
            self.transmit_packets(packets)  # Transmit the packets
            self.ser.write(b"END")  # Send an "END" message to indicate completion

    def compress_audio(self, audio_bytes):
        # Compress the audio to reduce its size
        audio_bytes = io.BytesIO(audio_bytes)  # Convert the bytes to a BytesIO object
        audio = AudioSegment.from_raw(audio_bytes, sample_width=2, frame_rate=16000, channels=1)  # Load the raw audio
        audio = audio.set_frame_rate(4000).set_sample_width(1)  # Downsample to 4kHz, 8-bit PCM
        return audio.raw_data  # Return the compressed audio as raw bytes

    def packet_generator(self, audio_bytes):
        # Split the audio data into packets of PAYLOAD_SIZE
        packets = []
        num_packets = (len(audio_bytes) + PAYLOAD_SIZE - 1) // PAYLOAD_SIZE  # Calculate the number of packets

        for i in range(num_packets):
            # Extract a chunk of audio data for each packet
            packet_payload = audio_bytes[i * PAYLOAD_SIZE: (i + 1) * PAYLOAD_SIZE]
            packets.append(packet_payload)  # Add the packet to the list
            
        return packets  # Return the list of packets

    def send_packet(self, packet):
        # Send a single packet and wait for an acknowledgment
        self.ser.write(packet)  # Send the packet
        ack_received = False  # Flag to track if an acknowledgment is received
        start_time = time.time()  # Record the start time
        while time.time() - start_time < 5:  # Wait for up to 5 seconds for an ACK
            if self.ser.in_waiting > 0:  # Check if data is available in the serial buffer
                ack = self.ser.readline().decode().strip()  # Read and decode the response
                if ack == "ACK":  # Check if the response is an acknowledgment
                    print(f"Packet sent successfully")  # Debug message
                    ack_received = True
                    break
        if not ack_received:  # If no acknowledgment is received
            raise serial.SerialTimeoutException  # Raise a timeout exception

    def transmit_packets(self, packets):
        # Transmit a list of packets over the serial connection
        self.ser.open()  # Open the serial port
        try:
            print("Transmitting packets...")  # Debug message
            for i, packet in enumerate(packets):  # Loop through each packet
                try:
                    self.send_packet(packet)  # Send the packet
                except(serial.SerialTimeoutException) as e:  # Handle timeout errors
                    print(f"Error transmitting packet {i}: {str(e)}")  # Debug message
                    self.send_packet(packet)  # Retry sending the packet

            print("Transmission complete")  # Debug message
        except serial.SerialException as e:
            print(f"Serial communication error: {str(e)}")  # Handle serial communication errors
        except Exception as e:
            print(f"An error occurred during transmission: {str(e)}")  # Handle other errors
        self.ser.close()  # Close the serial port