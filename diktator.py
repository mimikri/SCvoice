#!./venv/bin/python3

#3 processes
#stt
#microphone
#main
import speech_recognition as sr
from pynput.keyboard import Key, Controller
import json
keyboard = Controller()
import multiprocessing
audiocount = 0
audioall = 0

r = sr.Recognizer()
r.energy_threshold = 1500  # minimum audio energy to consider for recording
r.dynamic_energy_threshold = True
r.dynamic_energy_adjustment_damping = 0.15
r.dynamic_energy_ratio = 1.5
r.pause_threshold = 0.05  # seconds of non-speaking audio before a phrase is considered complete
r.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
r.phrase_threshold = 0.05  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
r.non_speaking_duration = 0.05  # seconds of non-speaking audio to keep on both sides of the recording


#___command interpretation and execution process_____________________________________________________________________________________________

# Start the command execution process
commands_queue = multiprocessing.Queue()

def command_execution_process(commands_queue):

    while True:
        voicestring = commands_queue.get()  # Wait for a recognized voice command
        keyboard.type(voicestring + " ")

# Start the command execution process
command_execution_process = multiprocessing.Process(target=command_execution_process, args=(commands_queue,))
command_execution_process.start()

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
        
           

