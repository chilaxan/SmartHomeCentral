import sys
import requests
import PySimpleGUI as sg
import time

device = sys.argv[1]
PASSWORD = 'best-password-ever'

layout = [[sg.Text(device)],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Device', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    time.sleep(1)
    window['-OUTPUT-'].update(requests.get(API_URL.format(device=urllib.parse.quote(device)), headers={
        'x-secret': PASSWORD
    }).content.decode())
    # Output a message to the window
    window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()
