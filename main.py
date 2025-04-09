from communication.sender import Sender
import communication.receiver

sender = Sender()
while True:
    print("----------------")
    print("1. Send Audio")
    print("2. Receive Audio")
    print("----------------")
    option = int(input("Choose the option :"))
    if option == 1:
        input('Press ENTER to send audio...')
        sender.send_file_audio()
    else:
        communication.receiver.main()