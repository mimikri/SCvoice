#!./venv/bin/python3
#venv/bin/pip3 install speechrecognition pyttsx4 pyautogui pynput pyaudio vosk multiprocessing time

import speech_recognition as sr
import pyttsx4
import pyautogui
import time
from pynput.keyboard import Key, Controller
keyboard = Controller()
import pygame
import multiprocessing
# Initialize the speech engine
engine = pyttsx4.init('espeak')
engine.setProperty('voice', 'german')  # Use the appropriate voice for German language
engine.setProperty('rate', 150)
engine.setProperty('pitch', 0.5)
voices = engine.getProperty('voices')

#for voice in engine.getProperty('voices'):
#    print(voice)
engine.say("aktiviere sprachassistenten")
engine.runAndWait()
# Define the array of dictionaries
import scconfig
commands = scconfig.commands


def sound_process(sound_queue):
    pygame.mixer.init()  # Initialize Pygame's mixer
    recognition_sound_path = 'gotit.wav'
    sound_queue.put(recognition_sound_path)
    while True:
        sound_path = sound_queue.get()  # Wait for a sound path to play
        if sound_path:
            sound = pygame.mixer.Sound(sound_path)
            sound.play()

# Start the sound process
recognition_sound_path = 'gotit.wav'
sound_queue = multiprocessing.Queue()
sound_process = multiprocessing.Process(target=sound_process, args=(sound_queue,))
sound_process.start()

def command_execution_logic(command, voicestring, sound_queue):
    if command["order_string"] in voicestring.lower():
        print(command["key_to_press"])
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
            pyautogui.press(command["key_to_press"])
        sound_queue.put('gotit.wav')

# Start the command execution process
commands_queue = multiprocessing.Queue()

def command_execution_process(sound_queue, commands_queue):
    while True:
        voicestring = commands_queue.get()  # Wait for a recognized voice command
        for command in commands:
            command_execution_logic(command, voicestring, sound_queue)

# Start the command execution process
command_execution_process = multiprocessing.Process(target=command_execution_process, args=(sound_queue, commands_queue))
command_execution_process.start()








def click_both_buttons(duration):
    # Simulate pressing both left and right mouse buttons at the current mouse position
    initial_x, initial_y = pyautogui.position()

    # Simulate pressing both left and right mouse buttons at the initial position
    pyautogui.mouseDown(button='left')
    pyautogui.mouseDown(button='right', x=initial_x, y=initial_y)

    # Wait for the specified duration
    time.sleep(duration)

    # Capture the updated mouse position
    updated_x, updated_y = pyautogui.position()

    # Release both left and right mouse buttons at the updated position
    pyautogui.mouseUp(button='left', x=updated_x, y=updated_y)
    pyautogui.mouseUp(button='right', x=updated_x, y=updated_y)






while True:
    r = sr.Recognizer()
    r.energy_threshold = 300 # minimum audio energy to consider for recording
    r.dynamic_energy_threshold = True
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_ratio = 1.5
    r.pause_threshold = 0.2  # seconds of non-speaking audio before a phrase is considered complete
    r.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout

    r.phrase_threshold = 0.2  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
    r.non_speaking_duration = 0.2  # seconds of non-speaking audio to keep on both sides of the recording
    with sr.Microphone(chunk_size=8192) as source:
        print("ready for order")
        audio = r.listen(source)
    try:
        commands_queue.put(r.recognize_vosk(audio, language="de"))
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results")






