import cv2

cam = cv2.VideoCapture('http://admin:password@10.50.12.88/1')

print(cam.isOpened())


