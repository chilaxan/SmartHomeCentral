import sys
import PySimpleGUI as sg

import tkinter
root = tkinter.Tk()
root.withdraw()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

from device import Device

device, on_command, off_command, on_text, off_text = sys.argv[1:]

layout = [[sg.VPush(background_color = None)],
          [sg.Text(device, font='Any 100', pad=(0,0))],
          [sg.VPush(background_color = None)],
          [sg.Text(key='-OUTPUT-', font='Any 200', pad=(0,0))],
          [sg.VPush(background_color = None)],
          [sg.Button('Quit', font='Any 50', pad=(0,0))],
          [sg.VPush(background_color = None)]]

def update_all_colors(window, color):
    for element in window.element_list():
        try:
            element.Widget.config(background=color)
            element.Widget.config(highlightbackground=color)
            element.Widget.config(highlightcolor=color)
            element.Widget.ParentRowFrame.config(background=color)
        except Exception:pass
    window.TKroot.configure(background=color)

# Create the window
window = sg.Window(
    'Device',
    layout,
    element_justification='c',
    no_titlebar=True,
    location=(0,0),
    size=(WIDTH,HEIGHT),
    keep_on_top=True,
    background_color='black'
).Finalize()
window.Maximize()
update_all_colors(window, 'red')
window['-OUTPUT-'].update(off_text)

dev = Device(device)

@dev.register(name=on_command)
def on_com():
    update_all_colors(window, 'green')
    window['-OUTPUT-'].update(on_text)

@dev.register(name=off_command)
def off_com():
    update_all_colors(window, 'red')
    window['-OUTPUT-'].update(off_text)

@dev.loop
def read_window():
    global event, values
    event, values = window.read(timeout=200)

@dev.end_when
def check():
    print(event)
    return event == sg.WINDOW_CLOSED or event == 'Quit'

dev.run()

# Finish up by removing from the screen
window.close()
