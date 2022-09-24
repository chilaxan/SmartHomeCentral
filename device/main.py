import sys
import requests
import PySimpleGUI as sg
import time
import urllib.parse

import tkinter
root = tkinter.Tk()
root.withdraw()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

device, on_command, off_command, on_text, off_text = sys.argv[1:]
PASSWORD = 'best-password-ever'
API_URL = 'http://chilaxan.tech/'
DEVICE_SLUG = '{device}'

requests.post(API_URL + f'register/{device}', headers={
    'x-secret': PASSWORD
}, json=[on_command, off_command])

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
        except:pass
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
# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read(timeout=200)
    # See if user wants to quit or window was closed
    try:
        command = requests.get(API_URL.format(device=urllib.parse.quote(device)), headers={
            'x-secret': PASSWORD
        }).content.decode()
        if command == on_command:
            update_all_colors(window, 'green')
            window['-OUTPUT-'].update(on_text)
        elif command == off_command:
            update_all_colors(window, 'red')
            window['-OUTPUT-'].update(off_text)
    except:
        print('couldn\'t communicate with api')
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    #time.sleep(.1)
    # Output a message to the window

# Finish up by removing from the screen
window.close()
