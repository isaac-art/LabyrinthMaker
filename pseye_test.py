import cv2
import numpy as np
from pseyepy import Camera, Display

c = Camera([0], fps=60, resolution=Camera.RES_LARGE, colour=True)

# print("frame: {}, time: {}".format(frame, timestamp))
# d = Display(c)


run = True

frame, timestamp = c.read()

cv2.namedWindow("mz", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("mz", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty("mz", cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_FREERATIO)

while run:

    # im = np.array(frame)


    frame, timestamp = c.read()
    # width, height = frame.shape
    
    frame = frame[100:320, 100:540]

    # b,g,r = cv2.split(im)
    cv2.imshow("mz", frame)
    # cv2.imshow("R", r)
    # cv2.imshow("G", g)
    # cv2.imshow("B", b)

    k = cv2.waitKey(1)
    if k == ord('n'):
        frame, timestamp = c.read()
    if k == ord('i'):
        frame = cv2.resize(frame, (0,0), fx=1.1, fy=1.1)
    if k == ord('o'):
        frame = cv2.resize(frame, (0,0), fx=0.9, fy=0.9)
    if k == ord('q'):
        run = False

cv2.destroyAllWindows()

# when finished, close the camera
# c.end()
