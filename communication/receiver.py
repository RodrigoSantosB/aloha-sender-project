import speech_recognition as sr
import sounddevice as sd
import pyaudio
import wave
import io
import serial

BAUD_RATE = 9600
SERIAL_PORT = "/dev/ttyACM0"

# Listen and recognize the speech

class Receiver():
    def __init__(self):
        self.ser = serial.Serial(baudrate=BAUD_RATE, timeout=2)
        self.ser.port = SERIAL_PORT
    
    def play():
        # Initialize recognizer
        mic = sr.Recognizer()
        chunk = 1024  
        audio_wav = None
        
        p = pyaudio.PyAudio()  

        # Use the microphone as the audio source
        audio_bytes = receive()
        audio_buffer = io.BytesIO(audio_bytes)
        audio_wav = wave.open(audio_buffer, "rb")
            
        stream = p.open(format = p.get_format_from_width(audio_wav.getsampwidth()),  
                    channels = audio_wav.getnchannels(),  
                    rate = audio_wav.getframerate(),  
                    output = True)
        
        data = audio_wav.readframes(chunk)  
        
        while data:  
            stream.write(data)  
            data = audio_wav.readframes(chunk)  
            
        stream.stop_stream()  
        stream.close()  
        
        #close PyAudio  
        p.terminate() 
        
    def receive():
        