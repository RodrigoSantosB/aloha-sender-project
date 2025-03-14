import keyboard
from scripts.talk import talk

if __name__ == "__main__":
    while True:
        # Wait for the space key to be pressed
        print("Pressione ESPAÇO para falar...")
        keyboard.wait("space")  # Blocks execution until space is pressed
        
        text = talk()  # Call the talk function when space is pressed