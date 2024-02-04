import time
#___________________________________for mainprocess only__________________________________________________________
if __name__ == '__main__':#avoid that multiprocesses load unnessesary modules
#___________________________________multiprocess functions__________________________________________________________

    #___tts successmessage process_____________________________________________________________________________________________

    def sound_process(sound_queue,loopdelay,LNG,LNGshort,operatingsystem):
        from subprocess import call
        import espeakng
        # Initialize the speech engine
        engine = espeakng.Speaker('espeak')
        #voices = engine.getProperty('voices')
        #print(voices)
        #engine.setProperty('voice', voices[11].id)  # Use the appropriate voice for German language
        #engine.setProperty('rate', 150)
        #engine.setProperty('pitch', 0.5)
        engine.voice = LNGshort
        engine.pitch = 0.5
        engine.wpm = 150
        if LNG == "German":
            if operatingsystem == 'windows':
                call(["espeak/espeak","-s140 -ven+18 -z","aktiviere sprachassistenten"])
            else:
                engine.say("aktiviere sprachassistenten", wait4prev=True)
        else:
            engine.say("activating speech assistant", wait4prev=True)
        #engine.runAndWait()
        
        
        while True:
            time.sleep(loopdelay)
            sound_path = sound_queue.get()  # Wait for a sound path to play
            if sound_path:
                print("playing", sound_path)
                if operatingsystem == 'windows':
                    call(["espeak/espeak","-s140 -ven+18 -z",sound_path])
                else:
                    engine.say(sound_path, wait4prev=True)
                #engine.runAndWait()          




    #___command interpretation and execution process_____________________________________________________________________________________________

    def command_execution_process(sound_queue, commands_queue,loopdelay,commands):
        from pynput.keyboard import Key, Controller
        import pyautogui
        keyboard = Controller()
        while True:
            time.sleep(loopdelay)
            voicestring = commands_queue.get()  # Wait for a recognized voice command
            for command in commands:
                if command["order_string"] in voicestring.lower():
                    print('command:', command["success_message"], ' key_to_press:', command["key_to_press"])
                    try:
                        if "_" in command["key_to_press"]:
                            if command["key_to_press"] == "maus_left":
                                click_both_buttons(3)
                            keys = command["key_to_press"].split("_")
                            pyautogui.hotkey(*keys)
                            if command["order_string"] == "info":
                                pyautogui.typewrite("r_DisplayInfo 3")
                                pyautogui.hotkey("enter")
                                pyautogui.hotkey("shiftright", "^")
                        else:
                            if command["key_type"] == "special":
                                pyautogui.press(command["key_to_press"])
                            else:
                                keyboard.type(command["key_to_press"])
                        sound_queue.put(command['success_message'])
                    except Exception as e:
                        print(e)




    #____microphone process____________________________________________________________________________________________

    def microphone_recognition_process(audio_queue,r,sr):
        
        with sr.Microphone() as source:
            while True:
                audio = r.listen(source)
                audio_queue.put(audio)




    #____stt process____________________________________________________________________________________________

    def recognito(audio_queue,r,commands_queue,loopdelay,LNGshort):
        import json
        audiocount = 0
        audioall = 0
        while True:
            time.sleep(loopdelay)
            # Check if there's a recognized voice string in the queue
            if not audio_queue.empty():
                audio = audio_queue.get()
                # Process the recognized voice string
                recognized_text = json.loads(r.recognize_vosk(audio, language=LNGshort))["text"].strip()
                audioall = audioall +1
                if recognized_text != "":
                    audiocount = audiocount +1
                    print(f'[{audiocount}/{audioall}] {recognized_text}')
                    commands_queue.put(recognized_text) 
            
            



















#______________________________gui__________________________________________________________________________________

    process = 0
    loopdelay = 0.02
    print('hallo') 
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    import speech_recognition as sr
    import sys  
    import multiprocess
    import os
    multiprocess.freeze_support()
    operatingsystem = 'linux'
    if os.name == 'nt':
        operatingsystem = 'windows'
   
    def getconfig(): # get settings from settingsfile
        import scconfig
        settings = scconfig.settings
        return settings
    print('get config')
    settings = getconfig()


    


    #____regognizer vosk_______________________________________________________________________________________________________
    #this is a dump workaround since speech recognitions vosk loader has a hardcoded path to the model, sry, for updateabilite i didn't wanted to change it
    #injecting a changed function, i tryed but didn't work. had problems to access class items from function, so this is ugly but seems to be the cleanest solution so far
    #when stying with vosk only KaldiRecognizer is an option
    def set_tts_model_path(LNG):
        if os.path.exists('Englishmodel') and os.path.exists('model'):
            os.rename('model', 'Germanmodel')
        elif os.path.exists('model') and os.path.exists('Germanmodel'):
            os.rename('model', 'Englishmodel')
        if LNG == "English":
            os.rename('Englishmodel', 'model')
        elif LNG == "German":
            os.rename('Germanmodel', 'model')
    print('rename models')
    set_tts_model_path(settings['LNG'])
    print('done')




    #____gui functions____________________________________________________________________________________________________
    def start_process(sound_process,command_execution_process,microphone_recognition_process,recognito,operatingsystem,loopdelay,settings):
        if operatingsystem == 'windows':
            multiprocess.set_start_method('spawn')  # Set the start method before creating processes
        print('register recognizer')
        r = sr.Recognizer() #  `r` is the speech recognition object
        print('set recognizer config')
        r.energy_threshold = float(settings['micsettings']['energy_threshold'])  # minimum audio energy to consider for recording
        r.dynamic_energy_threshold = bool(settings['micsettings']['dynamic_energy_threshold'])
        r.dynamic_energy_adjustment_damping = float(settings['micsettings']['dynamic_energy_adjustment_damping'])
        r.dynamic_energy_ratio = float(settings['micsettings']['dynamic_energy_ratio'])
        r.pause_threshold = float(settings['micsettings']['pause_threshold'] ) # seconds of non-speaking audio before a phrase is considered complete
        r.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
        r.phrase_threshold = float(settings['micsettings']['phrase_threshold'] ) # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
        r.non_speaking_duration = float(settings['micsettings']['non_speaking_duration'] ) # seconds of non-speaking audio to keep on both sides of the recording
        print('start processes')
        global command_execution_processo
        global microphone_processo
        global recognito_process
        global sound_processo
        sound_queue = multiprocess.Queue()
        sound_processo = multiprocess.Process(target=sound_process, args=(sound_queue,loopdelay,settings['LNG'],settings['LNGshort'],operatingsystem), name='sound_process')
        print(' - sound process')
        sound_processo.start()
        commands_queue = multiprocess.Queue()
        command_execution_processo = multiprocess.Process(target=command_execution_process, args=(sound_queue, commands_queue,loopdelay,settings[settings['LNGshort'] +'commands']), name='command_process')
        print(' - command process')
        command_execution_processo.start()
        audio_queue = multiprocess.Queue()
        microphone_processo = multiprocess.Process(target=microphone_recognition_process, args=(audio_queue,r,sr), name='microphone_process')
        print(' - microphone process')
        microphone_processo.start()
        recognito_process = multiprocess.Process(target=recognito, args=(audio_queue,r,commands_queue,loopdelay,settings['LNGshort']), name='recognito_process')
        print(' - speech to text process')
        recognito_process.start()

    def get_microphones():
        print('start mic search')
        #for index, name in enumerate(sr.Microphone.list_microphone_names()):
        #    try:
        #        with sr.Microphone(device_index=48,chunk_size=4000) as source:
        #            audio = r.listen(source)
        #            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
        #    except Exception as e:
        #        print('nope')

    def stop_process():
        processes = multiprocess.active_children()
        print(processes)
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
        del settings[settings['LNGshort'] +'commands'][index]
        refresh_display()
        save_config()

    def add_row():
        settings[settings['LNGshort'] +'commands'].append({"order_string": "", "key_to_press": "", "success_message": "", "key_type": ""})
        refresh_display()


    def update_micset(event, key):
        settings['micsettings'][key] = event.widget.get()
        save_config()
    def update_data(event, i, key):
        settings[settings['LNGshort'] +'commands'][i][key] = event.widget.get()
        save_config()

    def change_language(event):
        settings['LNG'] = language_switch.get()
        settings['LNGshort'] = "de" if settings['LNG'] == "German" else "en"
        set_tts_model_path(settings['LNG'])
        save_config()
        set_tts_model_path(settings['LNG'])#chang model paths, so the stt process can pick the right model
        #message = "Please restart the program to finish language change" 
        #messagebox.showinfo("Restart Program", message)
        #stop_process()
        #sys.exit()

    def save_config():
        with open('scconfig.py', 'wb') as file:
            strs = f"settings = {settings}"
            file.write(strs.encode('utf-8'))
        getconfig()#reload config , not needed cause settings gets updayed on the fly














    #____start gui_______________________________________________________________________________________________________

    print('start gui: set tk root')
    root = tk.Tk()
    root.title("SCvoice settings")
    root.configure(background='#222')

    print('set tabs')
    tab_control = ttk.Notebook(root, style="TNotebook")

    tab1 = ttk.Frame(tab_control,padding=20)
    tab_control.add(tab1, text='commands')

    tab2 = ttk.Frame(tab_control, padding=20)
    tab2.grid(row=0, column=0, sticky="nsew")
    tab_control.add(tab2, text='language')

    tab3 = ttk.Frame(tab_control,padding=20)
    tab_control.add(tab3, text='start')

    tab_control.pack(expand=1, fill="both")
    print('set tab content')

    start_button = tk.Button(tab3, text="Start Process", command=lambda: start_process(sound_process, command_execution_process, microphone_recognition_process, recognito,operatingsystem,loopdelay,settings))
    start_button.grid(row=0, column=0)

    stop_button = tk.Button(tab3, text="Stop Process", command=stop_process)
    stop_button.grid(row=1, column=0)

    status_text = tk.Text(tab3, height=10, width=50)
    status_text.grid(row=2, column=0)
    def refresh_display():
        for widget in frame.winfo_children():
            widget.destroy()
        # Table header
        header_labels = ['Num', 'Command', 'Keyboard Press', 'Success Message', 'Action Type']
        widths = [15,15,35]
        for i, label in enumerate(header_labels):
            header_label = ttk.Label(frame, text=label)
            header_label.grid(row=0, column=i)

        for i, row in enumerate(settings[settings['LNGshort'] + 'commands']):
            num = ttk.Label(frame, text=i+1)
            num.grid(row=i+1, column=0)
            for j, (key, value) in enumerate(row.items()):
                
                if key != 'key_type':
                    entry = ttk.Entry(frame, width=widths[j], style='Custom.TEntry')
                    entry.grid(row=i+1, column=j+1)
                    entry.insert(0, value)
                    entry.bind('<KeyRelease>', lambda event, i=i, j=key: update_data(event, i, j))
                else:
                    # Action Type dropdown
                    action_type_var = ['normal', 'special']
                    action_type_combobox = ttk.Combobox(frame, values=action_type_var,width=10, style='Custom.TCombobox')
                    action_type_combobox.set(value)
                    action_type_combobox.bind("<<ComboboxSelected>>", lambda event, i=i, j=key: update_data(event, i, j))
                    action_type_combobox.grid(row=i+1, column=j+1)


            delete_button = ttk.Button(frame, text="Delete", command=lambda i=i: delete_row(i))
            delete_button.grid(row=i+1, column=len(header_labels))
            lable_mic = ttk.Label(tab2, text="Mic settings:")
            lable_mic.grid(row=6, column=0,columnspan=2,sticky="w")
        for i, (key, value) in enumerate(settings['micsettings'].items()):
            label = ttk.Label(tab2, text=key)
            label.grid(row=i+7, column=0,sticky="e")
            entry = ttk.Entry(tab2, width=10, style='Custom.TEntry')
            entry.grid(row=i+7, column=1)
            entry.insert(0, str(value))
            entry.bind('<KeyRelease>', lambda event, key=key: update_micset(event, key))

                # Add a blank row before the horizontal line
            blank_label_before = ttk.Label(tab2, text="")
            blank_label_before.grid(row=3, column=0)

            # Create the horizontal line spanning the width of tab2
            separator = ttk.Separator(tab2, orient="horizontal")
            separator.grid(row=4, column=0, columnspan=2, sticky="ew")  # Assuming there are 2 columns in tab2

            # Add a blank row after the horizontal line
            blank_label_after = ttk.Label(tab2, text="")
            blank_label_after.grid(row=5, column=0)
        add_button = ttk.Button(frame, text="Add", command=add_row)
        add_button.grid(row=len(settings[settings['LNGshort'] + 'commands'])+1, column=len(header_labels))

    language_label = ttk.Label(tab2, text="Select Language:")
    language_label.grid(row=0, column=0, sticky="w")

    languages = ["English", "German"]
    language_switch = ttk.Combobox(tab2, values=languages,width=10)
    language_switch.set(settings['LNG'])
    language_switch.bind("<<ComboboxSelected>>", change_language)
    language_switch.grid(row=0, column=1)

    frame = ttk.Frame(tab1, padding="10")
    frame.grid(row=2, column=0)

    style = ttk.Style()
    style.theme_use('alt')  # Use the "alt" theme for more granular customization

    # Set custom colors for specific elements
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