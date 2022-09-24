import PySimpleGUI as sg
import os

import tkinter
root = tkinter.Tk()
root.withdraw()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

window = sg.Window(
    'Device',
    layout,
    element_justification='c',
    no_titlebar=True,
    location=(0,0),
    size=(WIDTH, HEIGHT),
    keep_on_top=True,
    background_color='black'
).Finalize()

dev = Device('light')

@dev.register
def on():
    os.system('xbacklight -set 100')
    window.TKroot.configure(background='white')

@dev.register
def off():
    os.system('xbacklight -set 0')
    window.TKroot.configure(background='black')

@dev.register
def debug():
    global event
    event = 'Quit'

@dev.loop
def read_window():
    global event, values
    event, values = window.read(timeout=200)

@dev.end_when
def check():
    return event == sg.WINDOW_CLOSED or event == 'Quit'

dev.run()

# Finish up by removing from the screen
window.close()
