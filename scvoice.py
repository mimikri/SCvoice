#!./venv/bin/python3
#venv/bin/pip3 install speechrecognition pyttsx4 pyautogui pynput pyaudio vosk multiprocessing time
#4 processes
#tts
#stt
#microphone
#main
import speech_recognition as sr
import pyttsx4
import pyautogui
import time
from pynput.keyboard import Key, Controller
import json
keyboard = Controller()
import multiprocessing
audiocount = 0
audioall = 0
# Define the array of dictionaries
import scconfig
commands = scconfig.commands
r = sr.Recognizer()
r.energy_threshold = 1500  # minimum audio energy to consider for recording
r.dynamic_energy_threshold = True
r.dynamic_energy_adjustment_damping = 0.15
r.dynamic_energy_ratio = 1.5
r.pause_threshold = 0.05  # seconds of non-speaking audio before a phrase is considered complete
r.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
r.phrase_threshold = 0.05  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
r.non_speaking_duration = 0.05  # seconds of non-speaking audio to keep on both sides of the recording

#___tts successmessage process_____________________________________________________________________________________________

def sound_process(sound_queue):
        # Initialize the speech engine
    engine = pyttsx4.init('espeak')
    engine.setProperty('voice', 'german')  # Use the appropriate voice for German language
    engine.setProperty('rate', 150)
    engine.setProperty('pitch', 0.5)
    engine.say("aktiviere sprachassistenten")
    engine.runAndWait()
    while True:
        sound_path = sound_queue.get()  # Wait for a sound path to play
        if sound_path:
            engine.say(sound_path)
            engine.runAndWait()          

# Start the sound process
recognition_sound_path = 'gotit.wav'
sound_queue = multiprocessing.Queue()
sound_process = multiprocessing.Process(target=sound_process, args=(sound_queue,))
sound_process.start()


#___command interpretation and execution process_____________________________________________________________________________________________

# Start the command execution process
commands_queue = multiprocessing.Queue()

def command_execution_process(sound_queue, commands_queue):

    while True:
        voicestring = commands_queue.get()  # Wait for a recognized voice command
        for command in commands:
            if command["order_string"] in voicestring.lower():
                print('command:', command["success_message"], ' key_to_press:', command["key_to_press"])
                try:
                    if "_" in command["key_to_press"]:
                        if command["key_to_press"] == "maus_left":
                            click_both_buttons(3)
                        keys = command["key_to_press"].split("_")
                        pyautogui.hotkey(*keys)
                        if command["order_string"] == "info":
                            pyautogui.typewrite("r_DisplayInfo 3")
                            pyautogui.hotkey("enter")
                            pyautogui.hotkey("shiftright", "^")
                    else:
                        if command["key_type"] == "special":
                            pyautogui.press(command["key_to_press"])
                        else:
                            keyboard.type(command["key_to_press"])
                    sound_queue.put(command['success_message'])
                except Exception as e:
                    print(e)
# Start the command execution process
command_execution_process = multiprocessing.Process(target=command_execution_process, args=(sound_queue, commands_queue))
command_execution_process.start()




#____fire function____________________________________________________________________________________________




def click_both_buttons(duration):
    initial_x, initial_y = pyautogui.position()
    pyautogui.mouseDown(button='left')
    pyautogui.mouseDown(button='right', x=initial_x, y=initial_y)
    time.sleep(duration)
    updated_x, updated_y = pyautogui.position()
    pyautogui.mouseUp(button='left', x=updated_x, y=updated_y)
    pyautogui.mouseUp(button='right', x=updated_x, y=updated_y)


#____microphone process____________________________________________________________________________________________

# Define a queue to pass the recognized voice strings from the microphone process to the processing process
audio_queue = multiprocessing.Queue()

# Function to handle microphone input and recognition
def microphone_recognition_process(audio_queue,r):
    with sr.Microphone(chunk_size=1024) as source:
        while True:
            
            audio_queue.put(r.listen(source))

# Start the microphone recognition process
microphone_process = multiprocessing.Process(target=microphone_recognition_process, args=(audio_queue,r))
microphone_process.start()


#____main loop____________________________________________________________________________________________

# Inside the processing logic
while True:
    # Check if there's a recognized voice string in the queue
    if not audio_queue.empty():
        audio = audio_queue.get()
        # Process the recognized voice string
        recognized_text = json.loads(r.recognize_vosk(audio, language="de"))["text"].strip()
        audioall = audioall +1
        if recognized_text != "":
            audiocount = audiocount +1
            print(f'[{audiocount}/{audioall}] {recognized_text}')
            commands_queue.put(recognized_text) 
        
           









