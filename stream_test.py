import cv2
import logging

class CAMERA:
    def __init__(self, camNum):
        try:
            self.cam = cv2.VideoCapture(camNum)
            print("started video")
        except:
            logging.warning("Error connection to Webcam")  # will print a message to the console

        while(self.cam.isOpened()):
            ret, frame = self.cam.read()
            cv2.imshow('Frame', frame)


    def __del__(self):
        self.cam.release ()


# cam1 = CAMERA(0)
cam1 = CAMERA('http://admin:password@10.50.12.88')


