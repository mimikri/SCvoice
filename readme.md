# SCvoice
<img src="https://raw.githubusercontent.com/mimikri/SCvoice/main/preview.jpg">
what it does.
<br>
microphone -> stt -> press keys on keyboard -> tts
<br>
it is a tiny py script wich, listens to the microphone.
if the user tells it an order, it turns the audio into text, fullfill the order and tell the user that it has done it.
<br>
there is a scconfig.py file, wich contains all the possible orders.
<br>
the string resulting from the spoken order is compared with the keywords of the orders in scconfig.py file.
if there is a match, a key is pressed or a key combination, and a successmessage is played.
<br>
so the user can tell an order, and the system does it an tells that it did do the order.
<br>
<br>

## warning speech recognition is only german at the moment, working on gui with lang change option<br>
you can change the vosk model to an english one, and replace all german and DE flags in scvoice.py<br>
and change the orderlist in scconfig.py - to make it english, will publish a version with language switch as soon as possible.<br>
<br>

# installation global:  <br>
download the repo and unzip it to a folder, or use git for it<br>
<br>
you can use python of your system, then you have to install: <br>
```
pip3 install speechrecognition pyttsx4 pyautogui pynput pyaudio vosk multiprocessing time
```
<br>
<br>

# installation local<br>
you can also open the terminal in the folder of scvoice and try to install a local python envirement for SCvoice only, to avoid dependency conflicts<br>
<br>
make the local python envirement(execute in scvoice folder): <br>
```
python3 -m venv venv
```
<br>
install the needed liberies to the local python envirement: <br>
```
venv/bin/pip3 install speechrecognition pyttsx4 pyautogui pynput pyaudio vosk multiprocessing time
```
<br>

# useage:<br>
```
python3 scvoice.py 
```
or with local SCvoice only envirement<br>
```
venv/bin/python3 scvoice.py 
```
<br>
speech recognition uses a german vosk model at the moment, wich is in /model/ folder.<br>
the model can be switched to an english one, and the scconfig.py file then has to be changed, to english keywords. <br>
also the tts voice needs to be changed to english in the mainscript. <br>

# known errors<br>
there are some errormessages under linux according to alsa and jackserver, this can be ingnored, <br>
since it's a problem alsa has, wich does not break the functionality, and is caused by speechrecognition libery when trying to find the right microphone.<br>
<br>

# additional thoughts<br>
since the speech recgnition model is very small, it has limited capacity and high speed.<br>
this makes it sutitable to drop ordes wich get fullfilles very fast, cause the tts needs less time.<br>
but therefore it can not understand all words, while it is very reliable on words it knows.<br>
<br>
multi orders are possible, if you for example tell 4 orders in a raw fast, they all are done.<br>
for example:<br>
"energy, engines, communication" -> would press "u" "i" "f11" and tell that it has done it.<br>
<br>
since the command-execution and the audio feedback loop are running in different processes, it can press all the buttons ,<br> 
while it is still expessing that it pressed the first one.  <br>
<br>
this prevents, that the second coman has to wait until the message is fully played.<br>
same for the recognition, it has its own loop, and while an audio order is processed. it is ready to take the next order.<br>
therefor<br>
microphon , stt , commandexecution and succesmessage, are running in 4 different processes. wich communitcate with queues.<br>
this parallel processing, enables it to react fast enought to be useful in game. as i tested it, <br>
it needs maybey 0.4sec from order spoken to fullfilles keypress. so it still has a delay, and you might could be faster with pressing keys.<br>
<br>

# used liberies <br>
speech_recognition<br>
vosk stt model<br>
pyttsx4 with espeak as tts<br>
pyautogui and pynput for button presses and hotkeys<br>
multiprocessing to make commandexecution faster, for multicommands<br>




