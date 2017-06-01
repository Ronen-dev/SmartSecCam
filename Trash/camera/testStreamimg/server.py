import sys
import io
import socket
import struct
from PIL import Image
import cv2
import numpy


if not sys.argv[1]:
    print('Usage : python server.py <addr>')
    return False


#fonction de traitement de la frame
def extract_features(image):
    print('Extract features')
    face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
    #eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')
    #nose_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/Nariz.xml')
    
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
        
        
        #eyes = eye_cascade.detectMultiScale(roi_gray, minSize=(30, 30))
        #for (ex,ey,ew,eh) in eyes:
        #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)
            
            #noses = nose_cascade.detectMultiScale(roi_gray, minSize=(100, 30))
            #for (ex,ey,ew,eh) in noses:
            #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)
    cv2.imshow('SmartSecCam', image)
    print('after show')

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
#server_socket.bind(('localhost', 8000))
server_socket.bind(sys.argv[1], 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        print('Image is %dx%d' % image.size)
        opencvImage = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)        
        key = cv2.waitKey(1) & 0xFF
        extract_features(opencvImage)
        if key == ord("q"):
            sock.close()
            break
        #image.verify()
        print('Image is verified')
finally:
    connection.close()
    server_socket.close()
