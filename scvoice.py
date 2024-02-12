import time
#___________________________________for mainprocess only__________________________________________________________
if __name__ == '__main__':#avoid that multiprocesses load unnessesary modules
#___________________________________multiprocess functions__________________________________________________________

    #___tts successmessage process_____________________________________________________________________________________________

    def sound_process(sound_queue,loopdelay,LNG,operatingsystem,wavfiles,audio_device):
     
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'starting soundprocess')
        import pyaudio
        import wave
        pa = pyaudio.PyAudio()
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],audio_device)
        default_output_index = pa.get_default_output_device_info()["index"]
        desired_output_device_index = default_output_index if audio_device == 'None' or audio_device == '' else audio_device
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],f"Using output device index {desired_output_device_index} for audio output")
        device_list = [pa.get_device_info_by_index(i) for i in range(pa.get_device_count())]
        output_devices = device_list
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],output_devices)
        while True:
            time.sleep(loopdelay)
            sound_path = sound_queue.get()  # Wait for a sound path to play
            if sound_path:
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],"playing", wavfiles[sound_path])
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],f"Using output device index {desired_output_device_index} for audio output")
                with wave.open(wavfiles[sound_path], 'rb') as wave_file:
                    stream_params = {
                        'format': pa.get_format_from_width(wave_file.getsampwidth()),
                        'channels': wave_file.getnchannels(),
                        'rate': 44100,
                        'output': True,
                        'output_device_index': desired_output_device_index
                    }

                    stream = pa.open(**stream_params)
                    data = wave_file.readframes(1024)
                    while data:
                        stream.write(data)
                        data = wave_file.readframes(1024)

                    stream.stop_stream()
                    stream.close()
        

                    #if operatingsystem == 'windows':
                #    call(["espeak/espeak","-s140 -ven+18 -z",sound_path])
                #else:
                #    engine.say(sound_path, wait4prev=True)
                #engine.runAndWait()  
               
          #from subprocess import call #call exefile with args in folder, so user don't has to install espeak-ng
        #import espeakng
        # Initialize the speech engine
        #engine = espeakng.Speaker('espeak')
        #voices = engine.getProperty('voices')
        #print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],voices)
        #engine.setProperty('voice', voices[11].id)  # Use the appropriate voice for German language
        #engine.setProperty('rate', 150)
        #engine.setProperty('pitch', 0.5)
        #engine.voice = LNGshort
        #engine.pitch = 0.5
        #engine.wpm = 150
        #if LNG == "German":
        #    if operatingsystem == 'windows':
        #        call(["espeak/espeak","-s140 -ven+18 -z","aktiviere sprachassistenten"])
        #    else:
        #        engine.say("aktiviere sprachassistenten", wait4prev=True)
        #else:
        #    engine.say("activating speech assistant", wait4prev=True)
        #engine.runAndWait()

        """
        import ctypes

        # Load the libespeak-ng.dll library
        espeak = ctypes.CDLL("path_to_libespeak-ng.dll")

        # Define the function prototypes
        espeak.espeak_Initialize.restype = ctypes.c_int
        espeak.espeak_Initialize.argtypes = []

        espeak.espeak_SetParameter.restype = ctypes.c_int
        espeak.espeak_SetParameter.argtypes = [ctypes.c_int, ctypes.c_int]

        # Initialize espeak
        espeak.espeak_Initialize()

        # Set parameters
        parameter_voice = 1  # Example voice parameter ID
        parameter_wpm = 80  # Example words per minute (WPM) value
        parameter_pitch = 50  # Example pitch value
        parameter_amplitude = 100  # Example amplitude value

        espeak.espeak_SetParameter(parameter_voice, 1)  # Set the voice parameter
        espeak.espeak_SetParameter(parameter_wpm, 200)  # Set the WPM parameter
        espeak.espeak_SetParameter(parameter_pitch, 70)  # Set the pitch parameter
        espeak.espeak_SetParameter(parameter_amplitude, 150)  # Set the amplitude parameter
        text = "Hello, World! aktiviere sprachassistenten"
        espeak.espeak_Synth(text.encode('utf-8'), len(text), 0, 0)

        #other aproach
        #if platform.system() == "Windows":
        #    self.executable = "path_to_libespeak-ng.dll"  # Update with the actual path to the libespeak-ng.dll file
        # insert into init function for windows to use local dll instead of system installed one
        """
    #___command interpretation and execution process_____________________________________________________________________________________________

    def command_execution_process(sound_queue, commands_queue,loopdelay,commands):
        from pynput.keyboard import Key, Controller
        from pynput.mouse import Button, Controller as MouseController
        last_order = [0,'last order']#[0] a timstamp, when the last command was executed, [1] the last command
        keyboard = Controller()
        listen_state = 'on'

        while True:
            time.sleep(loopdelay)
            voicestring = commands_queue.get()  # Wait for a recognized voice command
            for command in commands:
                if command["order_string"] in voicestring.lower():
                    print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'command:', command["success_message"], ' key_to_press:', command["key_to_press"])
                    try:
                        if command["key_to_press"] == 'on':
                            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'turn on')
                            listen_state = 'on'
                            continue
                        elif command["key_to_press"] == 'off':
                            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'turn off')
                            listen_state = 'off'
                            continue
                        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'status:', listen_state)
                        if listen_state == 'on':
                            keys = command["key_to_press"].split(" ")
                            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],keys)
                            for key_sequence in keys:
                                if "++" in key_sequence:#hotkey blocks
                                    presstime = 0.15
                                    explode = key_sequence.split(":") if ":" in key_sequence else [key_sequence]
                                    if len(explode) > 1:
                                        print('set presstime to',explode[1])
                                        presstime = int(explode[1])/1000
                                    key_sequence = explode[0]
                                    key_sequence_hotkey = key_sequence.split("++")
                                    for i, key in enumerate(key_sequence_hotkey):
                                        
                                        if len(key) > 1:
                                            key = Key[key].value
                                        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'hot key down', key,i)
                                        keyboard.press(key)
                                        time.sleep(0.15)
                                    time.sleep(presstime)
                                    for i, key in enumerate(key_sequence_hotkey):
                                        
                                        if len(key) > 1:
                                            key = Key[key].value
                                        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'hot key up', key,i)
                                        keyboard.release(key)
                                        time.sleep(0.15)

                                else:
                                    if key_sequence == "write":#type spoken text 
                                        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'type keys')
                                        keyboard.type(voicestring.replace(command["order_string"],''))
                                    elif key_sequence == "on":
                                        print('turn on')
                                    elif key_sequence == "off":
                                        print('turn off')
                                    

                                    else:
                                        #normal keys
                                        presstime = 0.15
                                        if len(key_sequence) > 1:
                                            explode = key_sequence.split(":") if ":" in key_sequence else [key_sequence]
                                            if len(explode) > 1:
                                                if explode[0] == '':# get the ":" right
                                                    explode[0] = ':'
                                                    if len(explode) > 2:
                                                        explode[1] = explode[2]
                                                print('set presstime to',explode[1])
                                                presstime = int(explode[1])/1000
                                            key_sequence = explode[0]
                                            if key_sequence == 'pause':
                                                time.sleep(presstime if presstime > 0.15 else 0.5)
                                                continue
                                            if len(key_sequence) > 1:
                                                key_sequence = Key[key_sequence].value
                                        
                                        keyboard.press(key_sequence)
                                        time.sleep(presstime)
                                        keyboard.release(key_sequence)
    
                            sound_queue.put(command['success_message'])
                    except Exception as e:
                        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'error' ,str(e))



    #____microphone process____________________________________________________________________________________________

    def microphone_recognition_process(audio_queue,r,sr):
        
        #list mics
        #print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],sr.Microphone.list_microphone_names())
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'start microphone process. ajusting listener')
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            while True:
                audio = r.listen(source)
                audio_queue.put(audio)




    #____stt process____________________________________________________________________________________________

    def recognito(audio_queue,r,commands_queue,loopdelay,LNG):
        import json
        audiocount = 0
        audioall = 0
        while True:
            time.sleep(loopdelay)
            # Check if there's a recognized voice string in the queue
            if not audio_queue.empty():
                audio = audio_queue.get()
                # Process the recognized voice string
                recognized_text = json.loads(r.recognize_vosk(audio, language=LNG))["text"].strip()
                audioall = audioall +1
                if recognized_text != "":
                    audiocount = audiocount +1
                    print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],f'[{audiocount}/{audioall}] {recognized_text}')
                    commands_queue.put(recognized_text) 
            
            



















#______________________________gui__________________________________________________________________________________

    process = 0
    loopdelay = 0.02
    print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'starting a main process') 
    import tkinter as tk
    from tkinter import ttk , messagebox , simpledialog
    import speech_recognition as sr
    import sys  
    import multiprocess
    import os
    import wave
    import copy
    multiprocess.freeze_support()#for windows, else would open new windows for multiprocesses
    operatingsystem = 'linux'
    if os.name == 'nt':
        operatingsystem = 'windows'
   
    import json
    global settings
    global wavfiles
    specialkeys = ['alt', 'alt_gr', 'alt_r', 'backspace', 'caps_lock', 'cmd', 'cmd_r', 'ctrl', 'ctrl_r', 'delete', 'down', 'end', 'enter', 'esc', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'home', 'insert', 'left', 'media_next', 'media_play_pause', 'media_previous', 'media_volume_down', 'media_volume_mute', 'media_volume_up', 'menu', 'num_lock', 'page_down', 'page_up', 'pause', 'print_screen', 'right', 'scroll_lock', 'shift', 'shift_r', 'space', 'tab', 'up']
    mousebuttons = ['button10', 'button11', 'button12', 'button13', 'button14', 'button15', 'button16', 'button17', 'button18', 'button19', 'button20', 'button21', 'button22', 'button23', 'button24', 'button25', 'button26', 'button27', 'button28', 'button29', 'button30', 'button8', 'button9', 'left', 'middle', 'right', 'scroll_down', 'scroll_left', 'scroll_right', 'scroll_up']
    def getconfig(): 
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'get config from','scconfig.json')
        with open('scconfig.json', 'r', encoding='utf-8') as file:
            settings = json.load(file)
        return settings

    
    settings = getconfig()

    

    def get_commandlist(commandlist_name = settings['commandlist']):
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'get commands from' ,'commandlists/'+ commandlist_name + '.json')
        if not os.path.exists('commandlists/' + commandlist_name + '.json'):
            commands = [{'order_string':'example', 'key_to_press': 'n', 'success_message': 'test 1 2 3 4 5 6 7 8 9 10 test' }]
        else:
            with open('commandlists/' + commandlist_name + '.json', 'r', encoding='utf-8') as file:
                commands = json.load(file)
        #print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'get commandlist',settings)
        if not commands:
            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'no commands found in','commandlists/' + settings['commandlist'] + '.json' , 'therefor setting exalmple list')
            commands = [{'order_string':'example', 'key_to_press': 'n', 'success_message': 'test 1 2 3 4 5 6 7 8 9 10 test' }]

        return commands

    
    settings['commands'] = get_commandlist()


    #____regognizer vosk_______________________________________________________________________________________________________
    #this is a dump workaround since speech recognitions vosk loader has a hardcoded path to the model, sry, for updateabilite i didn't wanted to change it
    #injecting a changed function, i tryed but didn't work. had problems to access class items from function, so this is ugly but seems to be the cleanest solution so far
    #when stying with vosk only KaldiRecognizer is an option
    def set_tts_model_path(LNG, oldlng="English"):
        if os.path.exists('model'):
            os.rename('model', oldlng + 'model')
            os.rename(LNG + 'model', 'model')
        else:
            os.rename(LNG + 'model', 'model')

    print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'rename models')
    set_tts_model_path(settings['LNG'],settings['LNG'])
    print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'done')




    #____gui functions____________________________________________________________________________________________________
    def start_process(sound_process,command_execution_process,microphone_recognition_process,recognito,operatingsystem,loopdelay,settings):
        
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],"start processes")
        #if operatingsystem == 'windows':
        #    multiprocess.set_start_method('spawn')  # Set the start method before creating processes, for win cause it handels multiprocesses different from linux
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'generate new success messages')
        
       
        wavfiles = generate_wav_files('success_messages',[obj['success_message'] for obj in settings['commands']])
        
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'register recognizer')
        r = sr.Recognizer() #  `r` is the speech recognition object
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'set recognizer config')
        r.energy_threshold = float(settings['micsettings']['energy_threshold'])  # minimum audio energy to consider for recording
        r.dynamic_energy_threshold = bool(settings['micsettings']['dynamic_energy_threshold'])
        r.dynamic_energy_adjustment_damping = float(settings['micsettings']['dynamic_energy_adjustment_damping'])
        r.dynamic_energy_ratio = float(settings['micsettings']['dynamic_energy_ratio'])
        r.pause_threshold = float(settings['micsettings']['pause_threshold'] ) # seconds of non-speaking audio before a phrase is considered complete
        r.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
        r.phrase_threshold = float(settings['micsettings']['phrase_threshold'] ) # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
        r.non_speaking_duration = float(settings['micsettings']['non_speaking_duration'] ) # seconds of non-speaking audio to keep on both sides of the recording
        
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'stop already running processes')
        stop_process()#if there are processes running, stop them
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'start new processes')
        
        global command_execution_processo
        global microphone_processo
        global recognito_process
        global sound_processo

       
        sound_queue = multiprocess.Queue()
        sound_processo = multiprocess.Process(target=sound_process, args=(sound_queue,loopdelay,settings['LNG'],operatingsystem,wavfiles,settings['audio_device']), name='sound_process')
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'---start sound process')
        sound_processo.start()
     

      
        commands_queue = multiprocess.Queue()
        command_execution_processo = multiprocess.Process(target=command_execution_process, args=(sound_queue, commands_queue,loopdelay,settings['commands']), name='command_process')
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'---start command process')
        command_execution_processo.start()
        

        audio_queue = multiprocess.Queue()
        microphone_processo = multiprocess.Process(target=microphone_recognition_process, args=(audio_queue,r,sr), name='microphone_process')
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'---start microphone process')
        microphone_processo.start()


        
        recognito_process = multiprocess.Process(target=recognito, args=(audio_queue,r,commands_queue,loopdelay,settings['LNG']), name='recognito_process')
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'---start speech to text process')
        recognito_process.start()



#____must be in seperat threads cause using pyaudio, 
# if pyaudio is not terminated sr.microphone does not work, and if it is terminated multithreads can not access default audio output device anymore
#therefor functions wich need pyaudio have to run in seprerate threads, to ensure mich access and audio output access in multiprocesses


    def audiofunctions(function_name, *args):
        queue = multiprocess.Queue()

        audio_multiprocess = multiprocess.Process(target=function_name, args=(queue, *args))
        audio_multiprocess.start()
        result = queue.get()
        audio_multiprocess.terminate()
        return result
    

    

    



    def test_output_device(queue,output_index):
        import pyaudio
        import wave
        try:
            pa = pyaudio.PyAudio()
            if 0 <= output_index < pa.get_device_count():
                output_stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, output_device_index=output_index)

                # Test the selected audio output device by playing an audio file
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],"Testing audio output... Playing test sound")
                with wave.open('test.wav', 'rb') as wf:
                    test_signal = wf.readframes(wf.getnframes())
                    output_stream.write(test_signal)

                # Close the output stream
                output_stream.stop_stream()
                output_stream.close()
            else:
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],"Invalid audio output device index selected.")
        except:
            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'bad device')
        queue.put('done')



    def get_output_device_list(queue, id_activ):
        import pyaudio
        pa = pyaudio.PyAudio()
        output_devices = []
        for i in range(pa.get_device_count()):
            device_info = pa.get_device_info_by_index(i)
            try:

                if device_info["maxOutputChannels"] > 0 and device_info["maxInputChannels"] == 0:
                    # Handle potential encoding issues
                    output_stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, output_device_index=device_info["index"])
                    output_stream.stop_stream()
                    output_stream.close()

                    device_name = device_info["name"].encode('latin1', errors='replace').decode('utf-8', errors='replace')
                    device_info["name"] = device_name
                    output_devices.append(device_info)

            except:
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'bad device:' + str(i) + ' ' + device_info["name"])
            
        if isinstance(id_activ, int) and 0 <= id_activ < len(output_devices):
            active_output = output_devices[id_activ]
        else:
            active_output = pa.get_default_output_device_info()
            active_output["name"] = active_output["name"].encode('latin1', errors='replace').decode('utf-8', errors='replace')

        queue.put({'output_devices': output_devices, 'active_output': active_output})


    def select_output_device():
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'collect output devices')
        output_devices = audiofunctions(get_output_device_list, settings['audio_device'])
        output_menu['menu'].delete(0, 'end')
        output_var.set(f"{output_devices['active_output']['index']}: {output_devices['active_output']['name']}")
        output_devices = output_devices['output_devices']
        for i, device in enumerate(output_devices):
            output_menu['menu'].add_command(label=f"{device['index']}. {device['name']}", command=lambda index=device['index'], name=device['name']: set_output_device(index, name))
        
       



        

















#________________normal ui functions_____________________

    def get_microphones():
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'start mic search')
        #for index, name in enumerate(sr.Microphone.list_microphone_names()):
        #    try:
        #        with sr.Microphone(device_index=48,chunk_size=4000) as source:
        #            audio = r.listen(source)
        #            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],"Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
        #    except Exception as e:
        #        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'nope')

    def stop_process():#stop all if not specified
        processes = multiprocess.active_children()
       
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],processes)
        for processo in processes:
                processo.terminate()
        for processo in processes:
                processo.kill()

    def update_status():
        status_text.delete('1.0', tk.END)
        try:
            if command_execution_processo.is_alive():
                status_text.insert(tk.END, 'command execution process up' + "\n")
            else:
                status_text.insert(tk.END, 'command execution process down' + "\n")
            if microphone_processo.is_alive():
                status_text.insert(tk.END, 'microphone process up' + "\n")
            else:
                status_text.insert(tk.END, 'microphone process down' + "\n")
            if recognito_process.is_alive():
                status_text.insert(tk.END, 'stt process up' + "\n")
            else:
                status_text.insert(tk.END, 'stt process down' + "\n")   
            if sound_processo.is_alive():
                status_text.insert(tk.END, 'tts process up' + "\n")
            else:
                status_text.insert(tk.END, 'tts process down' + "\n")     
        except Exception as e:
            status_text.insert(tk.END, 'no processes to track' + "\n")
        root.after(1000, update_status) 

    def close_window():
        root.destroy()
        sys.exit()

    def delete_row(index):
        del settings['commands'][index]
        refresh_display()
        save_commands()

    def add_row():
        settings['commands'].append({"order_string": "", "key_to_press": "", "success_message": "", "key_type": ""})
        refresh_display()


    def update_micset(event, key):
        settings['micsettings'][key] = event.widget.get()
        
        save_config()

    def update_data(event, i, key):
        settings['commands'][i][key] = event.widget.get()
        
        save_commands()

    def change_language(event):
        oldlng = settings['LNG']
        settings['LNG'] = language_switch.get()
        #if (settings['LNG'] + 'commands') not in settings:
        #    settings[settings['LNG'] + 'commands'] = settings[oldlng + 'commands']
        set_tts_model_path(settings['LNG'],oldlng)
        refresh_display()

        save_config()
        


 
    def change_commandlist(event):
        
        selected_file = commandlist_select.get()
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'change commandlist to', selected_file)
        settings['commandlist'] = selected_file
        #print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'---------------------------',settings)
        
        try:
            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'get commands from','commandlists/' + selected_file + '.json')
            with open('commandlists/' + selected_file + '.json', 'r', encoding='utf-8') as file:
                settings['commands'] = json.load(file)
                #print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'---------------------',settings)
        except FileNotFoundError:
            # Handle the case where the file does not exist
            settings['commands'] = []  # Assign an empty list if the file does not exist
            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],f"File 'commandlists/{selected_file}.json' not found. Initializing 'commands' as an empty list.")
        
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],f"Selected file: {selected_file}")
        save_config()
        refresh_display()





    def save_config():
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'saving config')
        
        # Save settings['commands'] to 'commandlists/{selected_file}.json'
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'write to file:','commandlists/' + settings['commandlist'] + '.json')
        with open('commandlists/' + settings['commandlist'] + '.json', 'w') as file:
            json.dump(settings['commands'], file, indent=4)
        
        # Create a deep copy of the settings dictionary
        tempsettings = copy.deepcopy(settings)
        
        # Remove the 'commands' key from the temporary settings
        if 'commands' in tempsettings:
            del tempsettings['commands']
        
        # Save the modified settings to 'scconfig.json'
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'write to file:','scconfig.json')
        with open('scconfig.json', 'w') as file:
            json.dump(tempsettings, file, indent=4)
        
    def save_commands():
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'saving commands')
        
        # Save settings['commands'] to 'commandlists/{selected_file}.json'
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'write to file:','commandlists/' + settings['commandlist'] + '.json')
        with open('commandlists/' + settings['commandlist'] + '.json', 'w') as file:
            json.dump(settings['commands'], file, indent=4)
     
    
    def delete_commandlist():
        global settings
        #print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'settings in delete command function:',settings)
        #print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'try to delete commandlist:', settings['commandlist'])
        file_path = 'commandlists/' + settings['commandlist'] + '.json'  # Replace with the actual file path
        if os.path.exists(file_path):
            overwrite = messagebox.askyesno("Commandlist delete!", "do you really want to delete the commandlist(" + settings['commandlist'] + ")?")
            if overwrite:
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'delete commandlist:',file_path)
                os.remove(file_path)
               
                values = list(commandlist_select['values'])  # Convert values to a list
                values.remove(settings['commandlist'])  # Remove the value
                commandlist_select['values'] = values  # Update the values of the combobox

                settings['commandlist'] = values[0]
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'activate commandlist',settings['commandlist'])
                commandlist_select.set(settings['commandlist'])
                settings['commands'] = get_commandlist(settings['commandlist'])
                save_config()
                refresh_display()
            else:
                pass  
        else:
            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],f"The file {file_path} does not exist.")

    def add_commandlist():
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'add commandlist')
        if new_commandlist_entry.get() == "":
            print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'no comandlist name entered.')
            return
        settings['commandlist'] = new_commandlist_entry.get()
        settings['commands'] = [{'order_string':'example', 'key_to_press': 'n', 'success_message': 'test 1 2 3 4 5 6 7 8 9 10 test' }]
        file_path = 'commandlists/' + settings['commandlist'] + '.json'
        if os.path.exists(file_path):
            if overwrite_prompt():
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'commandlist creation confirmed')
                pass
            else:
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'comandlist creation canceld')
                return
            
        else:
            commandlist_select['values'] = (commandlist_select['values']) + (settings['commandlist'],)
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'write to file:','commandlists/' + settings['commandlist'] + '.json')    
        with open('commandlists/' + settings['commandlist'] + '.json', 'w') as file:
            json.dump(settings['commands'], file, indent=4)

        commandlist_select.set(settings['commandlist'])
        save_config()
        refresh_display()

    def overwrite_prompt():
        overwrite = messagebox.askyesno("Commandlist Overwrite", "The file already exists. Do you reaaly want to overwrite it, by makeing a new commandlist with the same name?")
        if overwrite:
            return True
        else:
            return False


    def set_output_device(index, device_name):
        output_var.set(f"{index}: {device_name}")
        settings['audio_device'] = index
        save_config()
        



    def test_devices():
            output_index = output_var.get()
            output_index = int(output_index.split(":")[0])
            audiofunctions(test_output_device,output_index)

    def help_function():
        text = "special keys:\n" + "\n".join(specialkeys)
        top = tk.Toplevel(root)  # Use the existing root window for the Toplevel
        top.geometry("800x600")
        top.title("SCvoice Help")

        canvas = tk.Canvas(top)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        frame1 = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame1, anchor='nw')
        label0_text = """SCvoice Help
        ____________________________________________________________
        hotkeys:

        hotkeys are buttons wich are pressed togethe. 
        to use hotkeys you can conntect the keys as follows
        "shift++a" = "A"
        
        ------------------------------------------------------------

        pressing mutlible keys:

        "a b c" = "abc"
        
        ------------------------------------------------------------
        
        write text:

        the "write" key writes the text sayed after the command.
        if command is "order" and keyboard press is "write"
        and you say: "odrer this is a test" 
        the output will be:"this is a test"
        write can be combined too.

        ------------------------------------------------------------
        
        press time:

        each key can be augmented with a time in ms to press.
        "a:1000" = presses "a" for 1 second.
        "shift++a:1000" = presses "shift+a" for 1 second. 

        ------------------------------------------------------------
        
        pause command:

        the "pause" command waits for the given time in ms, before going on.
        "a pause:1000 shift+a" = "a" waits 1 second, then "shift+a"
        default pause is 500ms
        "a pause shift++a" = "a" waits 500ms, then "shift++a"

        ------------------------------------------------------------
        
        on and off:

        the "on" command and "off" commands can be used to turn the command execution on and off.
        "on" = when keywords are triggert a command is executed.
        "off" = when keywords are triggert a command is nothing is done, exept the keyword is "on". 

        ------------------------------------------------------------
        combination:

        "a b c shift++a a b c" = "abcAabc"
        ____________________________________________________________

        custom soundfiles:

        custom commandlists:

        adding recognition models:
        ____________________________________________________________
        
        Keyboard special keys"""
        label0 = tk.Label(frame1, text=label0_text)
        label0.pack()

        # First table for keyboard special keys
        table1 = ttk.Treeview(frame1, columns=('col1', 'col2', 'col3', 'col4'), show='', style="TLabel", height=len(specialkeys)//4)

        for i in range(0, len(specialkeys), 4):
            table1.insert('', tk.END, values=specialkeys[i:i+4])

        table1.pack(fill="both", expand=True)

        label = tk.Label(frame1, text="Mouse Functions")
        label.pack()

        # Second table for mouse functions
        table2 = ttk.Treeview(frame1, columns=('col1', 'col2', 'col3', 'col4'), show='', style="TLabel", height=len(mousebuttons)//4)

        for i in range(0, len(mousebuttons), 4):
            table2.insert('', tk.END, values=mousebuttons[i:i+4])

        table2.pack(fill="both", expand=True)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame1.bind("<Configure>", on_configure)
        def _bound_to_mousewheel(event):
            print('bind wheel')
            top.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbound_to_mousewheel(event):
            print('unbind wheel')
            top.unbind_all("<MouseWheel>")

        def on_mousewheel(event):
            
            print(event)
            if event.delta == 0:
                steps = -1 if event.num == 5 else 1
            else:
                steps = int(event.delta/120)
            
            print('mousewheel')
            canvas.yview_scroll(int(-1*(steps)), "units")

        if operatingsystem == 'windows':
            # with Windows OS
            canvas.bind_all("<MouseWheel>", on_mousewheel)
        else:
            # with Linux OS
            canvas.bind_all("<Button-4>", on_mousewheel)
            canvas.bind_all("<Button-5>", on_mousewheel)
            


    def generate_wav_files(folder_path, messages):
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'generating wav files')
        import array
        import pyttsx4
        print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'jo')
 
        from pydub import AudioSegment
        AudioSegment.ffmpeg = os.path.abspath("ffmpegwin64/bin/ffmpeg.exe") 
        wavfiles = {}
        engine = pyttsx4.init()
        for message in messages:
            
            sanitized_message = sanitize_message(message)
            if sanitized_message == "":
                continue
            wav_file_name = sanitized_message + ".wav"
            wav_file_path = os.path.abspath(os.path.join(folder_path, wav_file_name))
            wavfiles[message] = wav_file_path #maybe bad when message is not suitable for index
            
            if not os.path.exists(wav_file_path):
                # WAV file does not exist, generate it using pyttsx3
                print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],wav_file_path)
                engine.setProperty('rate', 140) 
                engine.save_to_file(message, wav_file_path)
                engine.runAndWait()
                
                # Load the WAV file
                audio = AudioSegment.from_wav(wav_file_path)
                # Resample the audio to the target sample rate (e.g., 44100)
                resampled_audio = audio.set_frame_rate(44100)
                # Save the resampled audio to a new WAV file
                resampled_audio.export(wav_file_path, format="wav")
        engine.stop()
        return wavfiles
                

        
    def sanitize_message(message):
        import re
        sanitized_message = re.sub(r'[^a-zA-Z0-9]', '_', message)
        return sanitized_message

    # Example usage
   
   

    #____start gui_______________________________________________________________________________________________________

    print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'start gui: set tk root')
    root = tk.Tk()
    root.title("SCvoice settings")

    root.geometry("800x650")
    root.configure(background='#222')

    print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'set tabs')
    tab_control = ttk.Notebook(root, style="TNotebook")

    tab1 = ttk.Frame(tab_control,padding=20)
    tab_control.add(tab1, text='commands')


    tab2 = ttk.Frame(tab_control, padding=20)
    tab2.grid(row=0, column=0, sticky="nsew")
    tab_control.add(tab2, text='language')

    tab3 = ttk.Frame(tab_control,padding=20)
    tab_control.add(tab3, text='start')

    tab_control.pack(expand=1, fill="both")
    print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],'set tab content')

    start_button = tk.Button(tab3, text="Start Process", command=lambda: start_process(sound_process, command_execution_process, microphone_recognition_process, recognito,operatingsystem,loopdelay,settings))
    start_button.grid(row=0, column=0)

    stop_button = tk.Button(tab3, text="Stop Process", command=stop_process)
    stop_button.grid(row=1, column=0)

    status_text = tk.Text(tab3, height=10, width=50)
    status_text.grid(row=2, column=0)
    help_button = ttk.Button(root, text="help", command=help_function, width=6)
    help_button.place(relx=1.0, rely=0.0, anchor="ne")
    def refresh_display(settings = settings):
        #print(time.strftime("%H:%M:%S ") + str(round(time.time() * 1000))[-3:],settings)
        for widget in frame.winfo_children():
            widget.destroy()
        # Table header
        header_labels = ['Num', 'Command', 'Keyboard Press', 'Success Message']
        widths = [15,15,35]
        for i, label in enumerate(header_labels):
            header_label = ttk.Label(frame, text=label)
            header_label.grid(row=1, column=i)

        for i, row in enumerate(settings['commands']):
            num = ttk.Label(frame, text=i+1)
            num.grid(row=i+2, column=0)
            for j, (key, value) in enumerate(row.items()):
                
                if key != 'key_type':
                    entry = ttk.Entry(frame, width=widths[j], style='Custom.TEntry')
                    entry.grid(row=i+2, column=j+1)
                    entry.insert(0, value)
                    entry.bind('<KeyRelease>', lambda event, i=i, j=key: update_data(event, i, j))



            delete_button = ttk.Button(frame, text="Delete", command=lambda i=i: delete_row(i))
            delete_button.grid(row=i+2, column=len(header_labels)+1,sticky="e")
            lable_mic = ttk.Label(tab2, text="Mic settings:")
            lable_mic.grid(row=8, column=0,columnspan=2,sticky="w")
        for i, (key, value) in enumerate(settings['micsettings'].items()):
            label = ttk.Label(tab2, text=key)
            label.grid(row=i+9, column=0,sticky="e")
            entry = ttk.Entry(tab2, width=10, style='Custom.TEntry')
            entry.grid(row=i+9, column=1)
            entry.insert(0, str(value))
            entry.bind('<KeyRelease>', lambda event, key=key: update_micset(event, key))
        blank_label_before = ttk.Label(tab2, text="")
        blank_label_before.grid(row=2, column=0)
            # Create the horizontal line spanning the width of tab2
        separator = ttk.Separator(tab2, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, sticky="ew")  # Assuming there are 2 columns in tab2

        blank = ttk.Label(frame, text="  ")
        blank.grid(row=1, column=len(header_labels))
        add_button = ttk.Button(frame, text="Add", command=add_row)
        add_button.grid(row=len(settings['commands'])+2, column=len(header_labels)+1)


    language_label = ttk.Label(tab2, text="Select Language:")
    language_label.grid(row=0, column=0, sticky="w")


    path_to_search = './'
    directories = [d for d in os.listdir(path_to_search) if os.path.isdir(os.path.join(path_to_search, d))]
    languages = [d.split('model', 1)[0].strip('_') for d in directories if 'model' in d.lower() and d.split('model', 1)[0].strip('_')]
    languages.append(settings['LNG'])  # Add settings['LNG'] to the languages list
    language_switch = ttk.Combobox(tab2, style='Custom.TCombobox', values=languages, width=10)
    language_switch.set(settings['LNG'])
    language_switch.bind("<<ComboboxSelected>>", change_language)
    language_switch.grid(row=0, column=1, sticky="e")
# Create dropdowns for selecting input and output devices
    label = ttk.Label(tab2, text='Select Output Device:')
    label.grid(row=4, column=0,sticky="w")
    output_var = tk.StringVar(tab2)
    output_menu = tk.OptionMenu(tab2, output_var, "Select Output Device")
    output_menu.grid(row=4,column=1, sticky='e')
    # Add a blank row before the horizontal line
    test_button1 = tk.Button(tab2, text="Test output", command=lambda: test_devices())
    test_button1.grid(row=5,column=1,sticky='e')
    blank_label_before = ttk.Label(tab2, text="")
    blank_label_before.grid(row=6, column=0)
    # Create the horizontal line spanning the width of tab2
    separator = ttk.Separator(tab2, orient="horizontal")
    separator.grid(row=7, column=0, columnspan=2, sticky="ew")  


    select_output_device()
    generate_wav_files('success_messages', [obj['success_message'] for obj in settings['commands']])
    file_list = [f.replace('.json', '') for f in os.listdir('commandlists') if f.endswith('.json')]

    comman_settings_frame = tk.Frame(tab1)
    comman_settings_frame.pack()
    commandlist_delete_button = ttk.Button(comman_settings_frame, text="delete", command=delete_commandlist,width=6)
    commandlist_delete_button.grid(row=0, column=0)
    active_commandlist_label = ttk.Label(comman_settings_frame, text="activ commandlist:",width=17, anchor='e')
    active_commandlist_label.grid(row=0 , column=1)
    commandlist_select = ttk.Combobox(comman_settings_frame, style='Custom.TCombobox', values=file_list,width=17)
    commandlist_select.bind("<<ComboboxSelected>>", change_commandlist)
    commandlist_select.set(settings['commandlist'])
    commandlist_select.grid(row=0 , column=2, sticky="w")
    new_commandlist_label = ttk.Label(comman_settings_frame, text="add new command list:",width=20, anchor='e')
    new_commandlist_label.grid(row=0 , column=3)
    new_commandlist_entry = ttk.Entry(comman_settings_frame, width=16, style='Custom.TEntry')
    new_commandlist_entry.grid(row=0 , column=4)
    new_commandlist_entry.insert(0, 'example')
    commandlist_add_button = ttk.Button(comman_settings_frame, text="add", command=add_commandlist,width=6)
    commandlist_add_button.grid(row=0, column=5)

    space_above = tk.Frame(tab1, height=10)
    space_above.pack()
    separator = ttk.Separator(tab1, orient='horizontal')
    separator.pack(fill='x')
    space_below = tk.Frame(tab1, height=10)
    space_below.pack()

    # Create a canvas for tab1
    canvas0 = tk.Canvas(tab1, highlightthickness=0, bg="#222")
    canvas0.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(tab1, orient="vertical", command=canvas0.yview)
    scrollbar.pack(side="right", fill="y")
    canvas0.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the content of tab1
    frame = ttk.Frame(canvas0)

    canvas0.create_window((0, 0), window=frame, anchor="nw")


    # Configure the canvas to update scroll region when the size of the frame changes
    frame.bind("<Configure>", lambda e: canvas0.configure(scrollregion=canvas0.bbox("all")))
    style = ttk.Style()
    style.theme_use('alt')  # Use the "alt" theme for more granular customization

    style.configure('TCanvas', background='#222')
    style.configure('TLabel', foreground='white', background='#222')  # Set label text and background color
    style.configure('TButton', foreground='white', background='#444')  # Set button text and background color
    style.map('TButton', background=[('active', '#333')])  # Set button background color when active
    style.configure('TEntry', fieldbackground='#333', foreground='#fff', bordercolor='#222',insertcolor='white')  # Set entry background, foreground, and border colors
    style.configure('Custom.TCombobox', fieldbackground='#333', foreground='#fff', background='#333', arrowcolor='white')
    style.configure('TFrame', background='#222')  # Set frame background color
    # Add an update function to schedule periodic updates
    style.configure("TNotebook", background='#000',padding=20, foreground='#fff',lightcolor="white", borderwidth=1, font=('Helvetica', '14', 'bold'))
    style.configure("TNotebook.Tab", background='#111', foreground='#fff',lightcolor="white", borderwidth=1, padding=[20, 5], font=('Helvetica', '14', 'bold'))
    style.map("TNotebook.Tab", background=[("selected", "#222")])
    refresh_display()
    # Set dark theme colors
  
    root.after(1000, update_status) 
    root.mainloop()