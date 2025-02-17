import speech_recognition as sr
import pyttsx3
import sounddevice as sd

jarvis = pyttsx3.init()

# Listen and recognize the speech
def listen_and_recognize():
    # Initialize recognizer
    mic = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        # chama um algoritmo de reducao de ruido
        mic.adjust_for_ambient_noise(source)
        
        # Frase para o usuario dizer algo
        print("Say something...")
        
        # Armazena o audio
        audio = mic.listen(source)
    
    try:
        # Recognize the speech default language is pt-BR
        text = mic.recognize_google(audio, language='pt-BR')
        text = text.lower()
        
        if "jarvis" in text:
            # Retirar comando Jarvis da frase
            text = text.replace("jarvis", "")
            jarvis.say(text)
            jarvis.runAndWait()
        return text
    
    except sr.UnknownValueError:
        print("Não entendi o que você disse")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    return None



def commands():
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
    except:
        jarvis.say("Não entendi o que você disse")
        jarvis.runAndWait()