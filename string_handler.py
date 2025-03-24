from communication.sender import Sender

sender = Sender()
while True:
    text = input('Please, Enter your command: ')
    text = text + '\r'
    sender.send_string(text)