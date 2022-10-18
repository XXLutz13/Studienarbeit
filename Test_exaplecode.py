import imp


import cv2
from PIL import ImageGrab
import numpy as np
import time

def screen_record(): 
    while True:
        # 800x600 windowed mode
        printscreen_pil =  ImageGrab.grab(bbox=(14,56,935,575))
        printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8')\
        .reshape((printscreen_pil.size[1],printscreen_pil.size[0],3))
        edges = cv2.Canny(printscreen_numpy,100,200)
        #cv2.imshow('window',cv2.cvtColor(printscreen_numpy, cv2.COLOR_BGR2RGB))
        cv2.imshow('Edge_detection',edges)
        cv2.moveWindow("Edge_detection", 940,0)
        time.sleep(1)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

screen_record()