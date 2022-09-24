import face_recognition
import cv2
import os
import requests
import urllib.parse
import speech_recognition as sr
import pyaudio
import PySimpleGUI as sg
import sys

import tkinter
root = tkinter.Tk()
root.withdraw()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

API_URL = 'http://chilaxan.tech/'
DEVICE_SLUG = '{user}/{device}/{action}'
PASSWORD = 'best-password-ever'

debug = len(sys.argv) == 2 and sys.argv[1] == 'debug'

mic = sr.Microphone()
rec = sr.Recognizer()
rec.dynamic_energy_threshold = False
rec.energy_threshold = 400

layout = [[sg.VPush(background_color = None)],
          [sg.Text('No One Detected', key='-OUTPUT-', font='Any 30', pad=(0,0)), sg.Text('🔇', key='speaker', font='Any 30', pad=(0,0))],
          [sg.VPush(background_color = None)],
          [sg.Output(size=(60,15))],
          [sg.VPush(background_color = None)],
          [sg.Button('Quit', font='Any 20', pad=(0,0))],
          [sg.VPush(background_color = None)]]

def main():
    video_capture = cv2.VideoCapture(0)
    window = sg.Window(
        'Detector',
        layout,
        element_justification='c',
        size=(WIDTH, HEIGHT)
    ).Finalize()
    known_encodings = []
    known_users = []
    for img in os.listdir('users'):
        image = face_recognition.load_image_file(f'users/{img}')
        known_encodings.append(face_recognition.face_encodings(image)[0])
        known_users.append(img[:-4])

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(small_frame, model="cnn")
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        # Display the results

        names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_users[first_match_index]
                names.append(name)

        if debug:
            # Display the resulting image
            for (top, right, bottom, left), name in zip(face_locations, names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size

                face_image = small_frame[top:bottom, left:right]

                # Blur the face image
                face_image = cv2.GaussianBlur(face_image, (99, 99), 30)

                # Put the blurred face region back into the frame image
                small_frame[top:bottom, left:right] = face_image

                # Draw a label with a name below the face
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(small_frame, name, (left + 6, bottom - 6), font, .5, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Debug', small_frame)

        if names:
            window['-OUTPUT-'].update(f"Hey, {','.join(map(str.title, names))}, what would you like to do?")
        else:
            window['-OUTPUT-'].update('No One Detected')
        event, values = window.read(timeout=200)
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if names:
            do_user(names[0], window)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    window.close()

def do_user(username, window):
    response = ''
    with mic as source:
        rec.adjust_for_ambient_noise(source)
        try:
            window['speaker'].update('🔊')
            window.refresh()
            audio = rec.listen(source, phrase_time_limit=5)
            window['speaker'].update('🔇')
            window.refresh()
            response = rec.recognize_google(audio)
        except Exception as e:
            print(e)

    if not response:
        return

    response = response.split()
    action = None
    device = None
    conf = requests.get(API_URL).json()
    for dev, actions in conf.items():
        if dev in response:
            device = dev
            if actions is None:
                action = ' '.join(response)
                break
            for act in actions:
                if act in response:
                    action = act
                    break
            break

    if not action or not device:
        return

    print(f'sending [{action}] to [{device}]')

    try:requests.post(
        API_URL + DEVICE_SLUG.format(
            user=urllib.parse.quote(username),
            device=urllib.parse.quote(device),
            action=urllib.parse.quote(action)
        ),
        headers={
            'x-secret': PASSWORD
        }
    )
    except:print('failed to communicate with api')

if __name__ == '__main__':
    main()
