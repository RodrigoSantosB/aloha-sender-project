from scripts.sender import Sender

sender = Sender()
while True:
    input('Press ENTER to send audio...')
    sender.send_audio()