import face_recognition
import cv2
import os
import requests
import urllib.parse
import speech_recognition as sr
import pyaudio
import time
import threading

API_URL = 'http://chilaxan.tech/{user}/{device}/{action}'
PASSWORD = 'best-password-ever'

mic = sr.Microphone()
rec = sr.Recognizer()
rec.dynamic_energy_threshold = False
rec.energy_threshold = 400

def main():
    video_capture = cv2.VideoCapture(0)
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
                try:
                    do_user(name)
                except Exception as e:
                    if e.args[0] == 'Quit':
                        video_capture.release()
                h, w, c = frame.shape
                cv2.putText(
                    frame,
                    f"Hey, {name.title()}, what would you like to do?",
                    (20, int(h) - 10),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

            names.append(name)

        # Display the resulting image
        for (top, right, bottom, left), name in zip(face_locations, names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            face_image = frame[top:bottom, left:right]

            # Blur the face image
            face_image = cv2.GaussianBlur(face_image, (99, 99), 30)

            # Put the blurred face region back into the frame image
            frame[top:bottom, left:right] = face_image

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Debug', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

from device_config import conf

def do_user(username):
    response = ''
    with mic as source:
        rec.adjust_for_ambient_noise(source)
        try:
            audio = rec.listen(source)
            response = rec.recognize_google(audio)
            print(response)
        except Exception as e:
            print(e)

    if not response:
        return

    response = response.split()
    if 'quit' in response:
        raise Exception('Quit')
    action = None
    device = None
    for dev, actions in conf.items():
        if dev in response:
            device = dev
            for act in actions:
                if act in response:
                    action = act
                    break
            break

    if not action or not device:
        return

    print(device, action)

    try:requests.post(
        API_URL.format(
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
