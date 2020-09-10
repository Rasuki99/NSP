from pynput.keyboard import Key, Controller
import time
import cv2

eye_cascPath = 'haarcascade_eye_tree_eyeglasses.xml'  #eye detect model
face_cascPath = 'haarcascade_frontalface_default.xml'  #face detect model

faceCascade = cv2.CascadeClassifier(face_cascPath)
eyeCascade = cv2.CascadeClassifier(eye_cascPath)

sleeptimer = 0
keyboard = Controller()
space_pressed = 0

cap = cv2.VideoCapture(0)
while 1:
    ret, img = cap.read()
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        # print("Found {0} faces!".format(len(faces)))
        if len(faces) > 0:
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
            eyes = eyeCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                # flags = cv2.CV_HAAR_SCALE_IMAGE
            )

            if len(eyes) == 0:
                print('no eyes!!!')
                if sleeptimer == 0:
                    sleeptimer = int(round(time.time() * 1000))

                if (int(round(time.time() * 1000))-sleeptimer) >= 2000 and space_pressed == 0:
                    keyboard.press(' ')

                    space_pressed = 1

            else:
                print('eyes!!!')
                keyboard.release(' ')
                space_pressed = 0
                sleeptimer = 0
            cv2.imshow('Face Recognition', img)
        waitkey = cv2.waitKey(1)
        if waitkey == ord('q') or waitkey == ord('Q'):
            cv2.destroyAllWindows()
            break