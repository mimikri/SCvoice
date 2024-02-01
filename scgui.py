import tkinter as tk
from tkinter import ttk
import sys

def close_window():
    root.destroy()
    sys.exit()
import scconfig
root = tk.Tk()
root.title("SCvoice settings")
root.configure(background='#222')

# Set the window background to transparent
root.attributes('-alpha', 0.0)
tab_control = ttk.Notebook(root, style="TNotebook")

tab1 = ttk.Frame(tab_control,padding=20)
tab_control.add(tab1, text='commands')

tab2 = ttk.Frame(tab_control, padding=20)
tab2.grid(row=0, column=0, sticky="nsew")
tab_control.add(tab2, text='language')

tab3 = ttk.Frame(tab_control,padding=20)
tab_control.add(tab3, text='start')

tab_control.pack(expand=1, fill="both")

data = {
    'commands': scconfig.commands,
    'LNG': scconfig.LNG,
    'micsettings': scconfig.micsettings
}

def delete_row(index):
    del data['commands'][index]
    refresh_display()
    save_config()

def add_row():
    data['commands'].append({"order_string": "", "key_to_press": "", "success_message": "", "key_type": ""})
    refresh_display()

def refresh_display():
    for widget in frame.winfo_children():
        widget.destroy()

    # Table header
    header_labels = ['Num', 'Command', 'Keyboard Press', 'Success Message', 'Action Type']
    widths = [15,15,35]
    for i, label in enumerate(header_labels):
        header_label = ttk.Label(frame, text=label)
        header_label.grid(row=0, column=i)

    for i, row in enumerate(data['commands']):
        num = ttk.Label(frame, text=i+1)
        num.grid(row=i+1, column=0)
        for j, (key, value) in enumerate(row.items()):
            
            if key != 'key_type':
                entry = ttk.Entry(frame, width=widths[j], style='Custom.TEntry')
                entry.grid(row=i+1, column=j+1)
                entry.insert(0, value)
                entry.bind('<KeyRelease>', lambda event, i=i, j=key: update_data(event, i, key))
            else:
                # Action Type dropdown
                action_type_var = ['normal', 'special']
                action_type_combobox = ttk.Combobox(frame, values=action_type_var,width=10, style='Custom.TCombobox')
                action_type_combobox.set(value)
                action_type_combobox.bind("<<ComboboxSelected>>", lambda event, i=i, j=key: update_data(event, i, key))
                action_type_combobox.grid(row=i+1, column=j+1)


        delete_button = ttk.Button(frame, text="Delete", command=lambda i=i: delete_row(i))
        delete_button.grid(row=i+1, column=len(header_labels))
        lable_mic = ttk.Label(tab2, text="Mic settings:")
        lable_mic.grid(row=6, column=0,columnspan=2,sticky="w")
    for i, (key, value) in enumerate(data['micsettings'].items()):
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
    add_button.grid(row=len(data['commands'])+1, column=len(header_labels))

def update_micset(event, key):
    data['micsettings'][key] = event.widget.get()
    save_config()
def update_data(event, i, key):
    data['commands'][i][key] = event.widget.get()
    save_config()

def change_language(event):
    data['LNG'] = language_switch.get()
    save_config()

def save_config():
    with open('scconfig.py', 'w') as file:
        file.write(f"LNG = \"{data['LNG']}\"\nmicsettings = {data['micsettings']}\ncommands = {data['commands']}")




language_label = ttk.Label(tab2, text="Select Language:")
language_label.grid(row=0, column=0, sticky="w")

languages = ["English", "German"]
language_switch = ttk.Combobox(tab2, values=languages,width=10)
language_switch.set(data['LNG'])
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

root.mainloop()