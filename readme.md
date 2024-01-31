# SCvoice

this is a proof of concept. may it will grow in time depening on the interesst.

what it does.

speech_recognition(mic) -> stt(vosk) -> press keys on keyboard -> tts(pyttsx4 with espeak)

it is a tiny py script wich, listens to the microphone.
if the user tells it an order, it uses vosk to turn the audio into text.

there is a scconfig.py file, wich contains all the possible orders.
the string resulting from the spoken order is compared with the keywords of the orders.
if there is a match, a key is pressed or a key combination, and a successmessage is played.

so the user can tell an order, and the system does it an tells that it did do the order.

# installation:  
download the repo and unzip it to a folder, or use git for it
you can use python of your system, then you have to install: 
```
pip3 install speechrecognition pyttsx4 pyautogui pynput pyaudio vosk multiprocessing time
```
you can also open the terminal in the folder of scvoice and try to install a local python envirement for SCvoice only, to avoid dependency conflicts

make the local python envirement(execute in scvoice folder): 
```
python3 -m venv venv
```
install the needed liberies to the local python envirement: 
```
venv/bin/pip3 install speechrecognition pyttsx4 pyautogui pynput pyaudio vosk multiprocessing time
```
# useage:
```
python3 scvoice.py 
```
or with local SCvoice only envirement
```
venv/bin/python3 scvoice.py 
```

speech recognition uses a german vosk model at the moment, wich is in /model/ folder.
the model can be switched to an english one, and the scconfig.py file then has to be changed, to english keywords. 
also the tts voice needs to be changed to english in the mainscript. 

there are some errormessages under linux according to alsa and jackserver, this can be ingnored, 
since it's a problem alsa has, wich does not break the functionality, and is caused by speachrecognition libery when trying to find the right microphone.

