import sounddevice as sd
from talk import listen_and_recognize
import pyttsx3


jarvis = pyttsx3.init()



if __name__ == "__main__":
    
    # text = listen_and_recognize()
    while True:
        # Listen and recognize the speech
        text = listen_and_recognize()
        jarvis.say("Ola, eu sou Jarvis, como posso te ajudar?")
        command = listen_and_recognize()
        
        try:
            if "tocar musica" in command:
                jarvis.say("Tocando música")
                jarvis.runAndWait()
                
            elif "proxima musica" in command:
                jarvis.say("Tocando próxima música")
                jarvis.runAndWait()
                
            elif "musica anterior" in command:
                jarvis.say("Tocando música anterior")
                jarvis.runAndWait()
                
            elif "parar musica" in command:
                jarvis.say("Até logo")
                jarvis.runAndWait()
                break
        except:
            jarvis.say("Não entendi o que você disse")
            jarvis.runAndWait()