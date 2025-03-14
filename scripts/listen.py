import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import pyaudio
import wave
import io

# Listen and recognize the speech
def listen():
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