#!/bin/bash

# Create a virtual environment
#python3 -m venv venv

# Install the required packages
venv/bin/pip3 install speechrecognition espeakng pyautogui pynput pyaudio vosk multiprocess 

venv/bin/python3 scvoice.py


