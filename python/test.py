import pathFinder
import numpy as np
import iterativePathFinder
import cv2

canvas = 255 * np.ones((250,330,3), dtype="uint8") # 250 by 330 canvas, set all pixels
cv2.imshow("Canvas", canvas)

prev_key = -1
while(1):
    key = cv2.waitKeyEx(1)
    if(prev_key != key):
        print(key)



