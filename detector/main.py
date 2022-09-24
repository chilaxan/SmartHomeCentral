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
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_users[first_match_index]
                do_user(name)

        # Display the resulting image
        cv2.imshow('Debug', small_frame)

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
    device = input('device: ')
    action = 'do something'
    print(device, action)

    requests.post(API_URL.format(user=username, device=urllib.parse.quote(device), action=urllib.parse.quote(action)), headers={
        'x-secret': PASSWORD
    })

if __name__ == '__main__':
    main()
