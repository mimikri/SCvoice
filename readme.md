# SCvoice
<img src="https://raw.githubusercontent.com/mimikri/SCvoice/main/preview.jpg">
what it does.
<br>
microphone -> stt -> press keys on keyboard -> tts
<br>
it listens to the microphone.<br>
if the user tells it an order, <br>
it turns the audio into text, <br>
fullfill the order and <br>
tell the user that it has done it.<br>

<br>
the string resulting from the spoken order is compared with the keywords of the orders wich can be set in gui.<br>
if there is a match, a key is pressed or a key combination, and a successmessage is played. multi commands are possible.<br>
<br>
so the user can tell an order, and the system does it an tells that it did do the order.<br>
<br>
<br>


# installation <br>
terminal in the folder of scvoice and start installscript<br>
<br>
```
bash install_scvoice.sh
```
<br>
installs<br>
ffmpeg for audio<br>
espeak for text to speach<br>
local python envirement<br>
py libs in local envirement wicht are needed<br>
then starts scvoice<br>

<br>

# useage:<br>
start scvoice.sh<br>
-might need reightclick -> settings -> permission -> run file as a progamm , to be started per click<br>
<br>
or in terminal navigate to the folder and enter<br>
```
venv/bin/python3 scvoice.py 
```

<br>


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

# props go to

alphacephei https://alphacephei.com/<br>
they provide exellent small and fast regognitiion models open source <3<3<3<br>
all the models used here are made by them (VOSK)<br>
espeak-ng provide open source tts, wich we use here as main option for audio success message output <3<3<3<br>
and all the great python liberies:<br>
pyttsx4<br>
speech_recognition<br>
pynput<br>
...


