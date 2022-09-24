import cv2

cap = cv2.VideoCapture(0)

user = input('Type username: ')

user = "".join([c for c in user if c.isalpha() or c.isdigit() or c==' ']).rstrip()

print('Click Camera and press q to take a picture')

while cap.isOpened():
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    cv2.imshow('frame', rgb)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        out = cv2.imwrite(f'users/{user}.png', frame)
        break

cap.release()
cv2.destroyAllWindows()
