import tkinter as tk
from tkinter import ttk
import scconfig

data = {
    'commands': scconfig.commands,
    'LNG': scconfig.LNG
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

    for i, row in enumerate(data['commands']):
        for j, (key, value) in enumerate(row.items()):
            entry = ttk.Entry(frame, width=15)
            entry.grid(row=i, column=j)
            entry.insert(0, value)
            entry.bind('<KeyRelease>', lambda event, i=i, j=key: update_data(event, i, j))

        delete_button = ttk.Button(frame, text="Delete", command=lambda i=i: delete_row(i))
        delete_button.grid(row=i, column=4)

    add_button = ttk.Button(frame, text="Add", command=add_row)
    add_button.grid(row=len(data['commands']), column=4)

def update_data(event, i, key):
    data['commands'][i][key] = event.widget.get()
    save_config()

def change_language(event):
    data['LNG'] = language_switch.get()
    save_config()

def save_config():
    with open('scconfig.py', 'w') as file:
        file.write(f"LNG = \"{data['LNG']}\"\n\ncommands = {data['commands']}")

root = tk.Tk()
root.title("Array Editor")

language_label = ttk.Label(root, text="Select Language:")
language_label.grid(row=0, column=0)

languages = ["English", "German"]
language_switch = ttk.Combobox(root, values=languages)
language_switch.set(data['LNG'])
language_switch.bind("<<ComboboxSelected>>", change_language)
language_switch.grid(row=0, column=1)

frame = ttk.Frame(root, padding="10")
frame.grid(row=1, column=0)

refresh_display()

root.mainloop()