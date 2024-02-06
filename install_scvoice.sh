#!/bin/bash

# Echo the welcome message
echo "Welcome to SCvoice installer"

# Check if ffmpeg is installed
if ! dpkg -s ffmpeg &> /dev/null; then
    echo "ffmpeg is not installed. Attempting to install..."
    sudo apt install ffmpeg
else
    echo "ffmpeg is already installed"
fi

# Check if espeak-ng is installed
if ! dpkg -s espeak-ng &> /dev/null; then
    echo "espeak-ng is not installed. Attempting to install..."
    sudo apt install espeak-ng
else
    echo "espeak-ng is already installed"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating virtual Python environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# List of required Python libraries
required_libraries=("speechrecognition" "espeakng" "pyautogui" "pynput" "pyaudio" "vosk" "multiprocess" "pyttsx4" "comtypes")

# Iterate through the list and check/install each library
for library in "${required_libraries[@]}"; do
    if ! venv/bin/pip3 show "$library" &> /dev/null; then
        echo "Installing $library..."
        venv/bin/pip3 install "$library"
    else
        echo "$library is already installed"
    fi
done

# Echo the process of starting SCvoice
echo "Trying to start SCvoice"
venv/bin/python3 scvoice.py