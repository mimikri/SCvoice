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

    # Table header
    header_labels = ['Num', 'Command', 'Keyboard Press', 'Success Message', 'Action Type']
    widths = [1,15,15,35]
    for i, label in enumerate(header_labels):
        header_label = ttk.Label(frame, text=label)
        header_label.grid(row=0, column=i)

    for i, row in enumerate(data['commands']):
        num = ttk.Label(frame, text=i+1)
        num.grid(row=i+1, column=0)
        for j, (key, value) in enumerate(row.items()):
            j = j+1
            if key != 'key_type':
                entry = ttk.Entry(frame, width=widths[j], style='Custom.TEntry')
                entry.grid(row=i+1, column=j)
                entry.insert(0, value)
                entry.bind('<KeyRelease>', lambda event, i=i, j=key: update_data(event, i, key))
            else:
                # Action Type dropdown
                action_type_var = ['normal', 'special']
                action_type_combobox = ttk.Combobox(frame, values=action_type_var,width=10, style='Custom.TCombobox')
                action_type_combobox.set(value)
                action_type_combobox.bind("<<ComboboxSelected>>", lambda event, i=i, j=key: update_data(event, i, key))
                action_type_combobox.grid(row=i+1, column=j)


        delete_button = ttk.Button(frame, text="Delete", command=lambda i=i: delete_row(i))
        delete_button.grid(row=i+1, column=len(header_labels))

    add_button = ttk.Button(frame, text="Add", command=add_row)
    add_button.grid(row=len(data['commands'])+1, column=len(header_labels))

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
root.title("SCvoice settings")
root.configure(background='#222')


language_label = ttk.Label(root, text="Select Language:")
language_label.grid(row=0, column=0)

languages = ["English", "German"]
language_switch = ttk.Combobox(root, values=languages,width=10)
language_switch.set(data['LNG'])
language_switch.bind("<<ComboboxSelected>>", change_language)
language_switch.grid(row=1, column=0)

frame = ttk.Frame(root, padding="10")
frame.grid(row=2, column=0)

refresh_display()
# Set dark theme colors

style = ttk.Style()
style.theme_use('alt')  # Use the "alt" theme for more granular customization

# Set custom colors for specific elements
style.configure('TLabel', foreground='white', background='#222')  # Set label text and background color
style.configure('TButton', foreground='white', background='#444')  # Set button text and background color
style.map('TButton', background=[('active', '#333')])  # Set button background color when active
style.configure('TEntry', fieldbackground='#333', foreground='#fff', bordercolor='#222')  # Set entry background, foreground, and border colors
style.configure('Custom.TCombobox', fieldbackground='#333', foreground='#fff', background='#333', arrowcolor='white')
style.configure('TFrame', background='#222')  # Set frame background color

root.mainloop()