import os
import sys
import time
import cv2
import random
import shutil
import OneTile
import numpy as np
from math import floor
from tomorrow import threads



@threads(20)
def callTile(path):
    OneTile.main(path, "live_mz")
    return

def maze(width, height, sz):
    for x in range(width // sz):
        for y in range(height // sz):
            lab = "live_cv/x%s_y%s.png" % (x, y)
            callTile(lab)
            y += sz
        x += sz
    return


def save(width, height, sz, bg):
    for x in range(width // sz):
        for y in range(height // sz):
            print("w:%s, h:%s, sz:%s" % (width, height, sz))
            seg = bg[y * sz:y * sz + sz, x * sz:x * sz + sz]
            lab = "live_cv/x%s_y%s.png" % (x, y)
            try:
                cv2.imwrite(lab, seg)
            except Exception as e:
                print(e)
                pass
            y += sz
        x += sz
    return


def main():
    cap = cv2.VideoCapture(0)

    width = floor(cap.get(3)) // 2
    height = floor(cap.get(4)) // 2
    sz = 100 
    run = True

    while(run):
        ret, frame = cap.read()
        small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 

        gray = cv2.cvtColor(small,cv2.COLOR_BGR2GRAY)
        ret, thr = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = np.ones((2, 2), np.uint8)
        opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=2)
        bg = cv2.dilate(opening, kernel, iterations=3)

        cv2.imshow('a', bg)
    
        
        if cv2.waitKey(1) == ord('s'):
            print("saving")
            save(width, height, sz, bg)
            
        if cv2.waitKey(1) == ord('a'):
            print("maze")
            maze(width, height, sz)

        if cv2.waitKey(1) == ord('q'):
            run = False

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


