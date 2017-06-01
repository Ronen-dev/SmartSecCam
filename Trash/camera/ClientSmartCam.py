import socket
import sys
import numpy
from time import sleep
import cv2
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray

#Init camera (resolution, frameRate)
#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(640, 480))


#fonction de traitement de la frame
def extract_features(image):
    print ("begin extract_features")
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

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print ('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    
    while True :
        image = numpy.empty([480, 640])
        i = 0
        while i < 480 :
            data = sock.recv(640)
            image[i] = numpy.fromstring(data, dtype=numpy.uint8, count=640)
            i += 1
        cv2.imshow('imageclient', image)
        #extract_features(image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') :
            keep_run = false
            sock.close()            
            break
