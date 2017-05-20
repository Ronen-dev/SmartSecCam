import socket
import sys
from time import sleep
import cv2
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray

#Init camera (resolution, frameRate)
camera = PiCamera()
camera.resolution = (480, 640)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(480, 640))


if __name__ == "__main__":
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print ('starting up on %s port %s' % server_address)
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        image = frame.array
        key = cv2.waitKey(1) & 0xFF

        
        print ('waiting for a connection')
        connection, client_address = sock.accept()
        print( 'connection from', client_address)
        cv2.imshow('imgserver', image)
        # Receive the data in small chunks and retransmit it
        i = 0
        while i < 480 :
            connection.send(image[i])
            i += 1
        rawCapture.truncate(0)
        f.close()
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            connection.close()
            break
