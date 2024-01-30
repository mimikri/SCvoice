# -*- coding: utf-8 -*-
import speech_recognition as sr
import pyttsx3
import pyautogui
import time
import json
import keyboard
import os
from pynput.keyboard import Key, Controller

keyboard = Controller()
# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('voice', 'german')  # Use the appropriate voice for German language
os.system("setxkbmap -layout de_nodeadkeys")


while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ready for order")
        audio = r.listen(source)
    try:
        result = r.recognize_vosk(audio, language="de_DE")
        recognized_text = json.loads(result)["text"]
        print("Recognized:", recognized_text)
        keyboard.type(recognized_text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results")