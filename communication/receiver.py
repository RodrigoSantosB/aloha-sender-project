# Import necessary libraries
import sounddevice as sd  # For audio playback (not used in this code)
import pyaudio  # For audio playback
import io  # For handling in-memory byte streams
import serial  # For serial communication
import time  # For time-related operations
from pydub import AudioSegment  # For audio manipulation

# Constants for serial communication and payload size
BAUD_RATE = 9600  # Baud rate for serial communication
SERIAL_PORT = "/dev/ttyACM0"  # Serial port to communicate with
PAYLOAD_SIZE = 62  # Size of the payload to read from the serial port

# Receiver class to handle receiving and playing audio data
class Receiver():
    def __init__(self):
        # Initialize the serial connection
        self.ser = serial.Serial(baudrate=BAUD_RATE, timeout=2)  # Set baud rate and timeout
        self.ser.port = SERIAL_PORT  # Set the serial port
        self.audio_bytes_array = []  # List to store received audio data as bytes
    
    def play(self):
        # Convert the list of bytes into a single bytes object
        audio_buffer = io.BytesIO(b"".join(self.audio_bytes_array))
        
        # Load the MP3 data into an AudioSegment object
        audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")

        # Convert the AudioSegment to raw PCM data
        raw_audio = audio_segment.raw_data

        # Initialize PyAudio for audio playback
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(audio_segment.sample_width),  # Set audio format
                        channels=audio_segment.channels,  # Set number of channels
                        rate=audio_segment.frame_rate,  # Set frame rate
                        output=True)  # Enable output mode

        # Play the raw audio data
        stream.write(raw_audio)

        # Cleanup the PyAudio stream and terminate
        stream.stop_stream()
        stream.close()
        p.terminate()

    def receive(self):
        # Clear the audio bytes array
        self.audio_bytes_array = []
        self.ser.open()  # Open the serial port
        count = 0  # Counter to track the number of payloads received
        try:
            start = time.time()  # Record the start time
            while True:
                if self.ser.in_waiting > 0:  # Check if data is available in the serial buffer
                    try:
                        print("Receiving data...")  # Debug message
                        data = self.ser.read(PAYLOAD_SIZE)  # Read a payload of size PAYLOAD_SIZE
                        count += 1  # Increment the counter
                        print(count)  # Print the current count
                        if count == 26:  # If 26 payloads are received
                            print("Playing audio...")  # Debug message
                            self.play()  # Play the received audio
                            break  # Exit the loop
                        self.audio_bytes_array.append(data)  # Append the received data to the array
                    except UnicodeDecodeError:  # Handle decoding errors
                        continue
        except KeyboardInterrupt: # Handle manual interruption (Ctrl+C)
            pass
        
        self.ser.close()  # Close the serial port

# Main function to initialize and start the receiver
def main():
    receiver = Receiver()  # Create an instance of the Receiver class
    receiver.receive()  # Start receiving data

# Entry point of the script
if __name__ == "__main__":
    main()  # Call the main function