import sounddevice as sd
import pyaudio
import wave
import io
import serial
import time
from pydub import AudioSegment


BAUD_RATE = 9600
SERIAL_PORT = "/dev/ttyACM0"
PAYLOAD_SIZE = 62

# Listen and recognize the speech

class Receiver():
    def __init__(self):
        self.ser = serial.Serial(baudrate=BAUD_RATE, timeout=2)
        self.ser.port = SERIAL_PORT
        self.audio_bytes_array = []
    
    def play(self):
        # Convert list of bytes to a single bytes object
        audio_buffer = io.BytesIO(b"".join(self.audio_bytes_array))
        
        # Load the MP3 data into an AudioSegment
        audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")

        # Convert AudioSegment to raw PCM data
        raw_audio = audio_segment.raw_data

        # Initialize PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(audio_segment.sample_width),
                        channels=audio_segment.channels,
                        rate=audio_segment.frame_rate,
                        output=True)

        # Play audio
        stream.write(raw_audio)

        # Cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()

        
    def receive(self):
        self.audio_bytes_array = []
        self.ser.open()
        try:
            start = time.time()
            while True:
                if self.ser.in_waiting > 0:
                    try:
                        print("Receiving data...")
                        data = self.ser.read(PAYLOAD_SIZE)
                        print("Received data:", data)
                        if time.time() - start > 40:
                            print("Playing audio...")
                            self.play()
                            break
                        self.audio_bytes_array.append(data)
                    except UnicodeDecodeError:
                        continue
        except KeyboardInterrupt:
            pass
        
        self.ser.close()
        
def main():
    receiver = Receiver()
    receiver.receive()
        
if __name__ == "__main__":
    main()