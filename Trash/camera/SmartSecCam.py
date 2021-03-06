import sys
from time import sleep
import cv2
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray

#Init camera (resolution, frameRate)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))


#fonction de traitement de la frame
def extract_features(image):
    face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')
    nose_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/Nariz.xml')
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    # iterate over all identified faces and try to find eyes and noses
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]


        eyes = eye_cascade.detectMultiScale(roi_gray, minSize=(30, 30))
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

        noses = nose_cascade.detectMultiScale(roi_gray, minSize=(100, 30))
        for (ex,ey,ew,eh) in noses:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)


    cv2.imshow('SmartSecCam', image)

if __name__ == "__main__":

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text

        #recuperqtion de la frame
        image = frame.array

        #recuperation de la touche press
        key = cv2.waitKey(1) & 0xFF


        #traitement et affichqge de l'image
        extract_features(image)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
