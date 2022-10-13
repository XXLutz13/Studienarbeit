import cv2
import logging

class CAMERA:
    def __init__(self, camNum):
        try:
            self.cam = cv2.VideoCapture(camNum)
            print("started video")
        except:
            logging.warning("Error connection to Webcam")  # will print a message to the console

    def image(self):
        ret, frame = self.cam.read()
        #if image capture valid, then save
        if frame is None:
            logging.warning("Error capturing image")
        else:
            cv2.imwrite("TestImage.png", frame)

    def __del__(self):
        self.cam.release ()


cam1 = CAMERA(0)
cam1.image()


