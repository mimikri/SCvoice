this is a proof of concept. may ith will grow in time depening on the interesst.

whta it does.

it is a tiny py script wich, listens to the microphone.
if the user tells it a order, it uses vosk to turn the audio into text.

ther is a scconfig.py file, wich contains all the possible orders.
the string resulting from the spoken order is compared with the keywords of the orders.
if there is a match, a key is pressed or a key combination, and a successmessage is played.

so the user can tell an order, and the system does it an tells that it did do the order.

use:

python3 stringinterpreter.py

there are some errormessages under linux according to jackserver, this can be ingnored, since it's a problem alsa has, wich is not related to the functionality, and is caused by speachrecognition libery.
