#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Install the required packages
venv/bin/pip3 install speechrecognition pyttsx4 pyautogui pynput pyaudio vosk

venv/bin/python3 scvoice.py


