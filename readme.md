# SCvoice

this is a proof of concept. may it will grow in time depening on the interesst.

what it does.

microphone -> stt -> press keys on keyboard -> tts

it is a tiny py script wich, listens to the microphone.
if the user tells it an order, it turns the audio into text, fullfill the order and tell the user that it has done it.

there is a scconfig.py file, wich contains all the possible orders.

the string resulting from the spoken order is compared with the keywords of the orders in scconfig.py file.
if there is a match, a key is pressed or a key combination, and a successmessage is played.

so the user can tell an order, and the system does it an tells that it did do the order.


## warning speech recognition is only german at the moment, working on gui with lang change option
you can change the vosk model to an english one, and replace all german and DE flags in scvoice.py
and change the orderlist in scconfig.py - to make it english, will publish a version with language switch as soon as possible.

# installation global:  
download the repo and unzip it to a folder, or use git for it

you can use python of your system, then you have to install: 
```
pip3 install speechrecognition pyttsx4 pyautogui pynput pyaudio vosk multiprocessing time
```


# installation local
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
# known errors
there are some errormessages under linux according to alsa and jackserver, this can be ingnored, 
since it's a problem alsa has, wich does not break the functionality, and is caused by speechrecognition libery when trying to find the right microphone.

# additional thoughts
since the speech recgnition model is very small, it has limited capacity and high speed.
this makes it sutitable to drop ordes wich get fullfilles very fast, cause the tts needs less time.
but therefore it can not understand all words, while it is very reliable on words it knows.

multi orders are possible, if you for example tell 4 orders in a raw fast, they all are done.
for example:
"energy, engines, communication" -> would press "u" "i" "f11" and tell that it has done it.

since the command-execution and the audio feedback loop are running in different processes, it can press all the buttons , 
while it is still expessing that it pressed the first one.  

this prevents, that the second coman has to wait until the message is fully played.
same for the recognition, it has its own loop, and while an audio order is processed. it is ready to take the next order.
therefor
microphon , stt , commandexecution and succesmessage, are running in 4 different processes. wich communitcate with queues.
this parallel processing, enables it to react fast enought to be useful in game. as i tested it, 
it needs maybey 0.4sec from order spoken to fullfilles keypress. so it still has a delay, and you might could be faster with pressing keys.

# used liberies 
speech_recognition
vosk stt model
pyttsx4 with espeak as tts
pyautogui and pynput for button presses and hotkeys
multiprocessing to make commandexecution faster, for multicommands




