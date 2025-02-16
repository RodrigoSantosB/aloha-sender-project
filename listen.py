import  pyttsx3

speaker = pyttsx3.init()

text = "Olá, eu sou Jarvis, como posso te ajudar?"

voices = speaker.getProperty('voices')

for voice in voices:
    print(voice, voice.id)

rate = speaker.getProperty('rate')
speaker.setProperty('rate', rate-25)   
speaker.setProperty('voice', voices[83].id)
# speaker.setProperty('voice', voice.id)
speaker.say(text)
speaker.runAndWait()

# for i, voice in enumerate(voices):
#     print(voice, voice.id)    
#     if "Portuguese" in voice.id:
#         print(i)
        


# # print(text)
# speaker.say(text)
# speaker.runAndWait()