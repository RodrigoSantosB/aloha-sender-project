from communication.sender import Sender
# from communication.receiver import Receiver

sender = Sender()
# receiver = Receiver()
while True:
    input('Press ENTER to send audio...')
    sender.send_file_audio()