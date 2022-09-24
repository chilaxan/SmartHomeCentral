import face_recognition
import cv2
import os
import requests
import urllib.parse

API_URL = 'http://chilaxan.tech/{user}/{device}/{action}'
PASSWORD = 'best-password-ever'

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
                do_user(name)
                names.append(name)

        # Display the resulting image
        for (top, right, bottom, left), name in zip(face_locations, names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def do_user(username):
    # talk to user
    # say: Hello, {username}
    # say: What would you like to do?
    # if user says "nothing", do nothing
    device = 'device'
    action = 'do something'
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
