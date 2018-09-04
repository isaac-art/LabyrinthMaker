import cv2
import freenect
import numpy as np
import frame_convert2
from PIL import Image

# 
# THIS IS A QUICK LITTLE PROGRAM FOR MANUALLY CATCHING THE
# TEST IMAGES TO BE USED FOR THE CAMERA CALIBRATION
# 

global f_num
f_num = 0

global mode
mode = "ir"


def kinect_get_video():
    # get the rgb image and make it correct format 
    return frame_convert2.video_cv(freenect.sync_get_video()[0])


def kinect_get_ir():
    # get the IR image and make it correct format
    array, t = freenect.sync_get_video(0,freenect.VIDEO_IR_10BIT)
    array = frame_convert2.pretty_depth_cv(array)
    return array


def main():
    global f_num
    cv2.namedWindow(mode)
    # While True runs a loop
    while 1:
        # if ir mode
        if mode == "ir":
            frame = kinect_get_ir()
            print(frame)
        # if rgb more
        else:
            frame = kinect_get_video()
            print(frame)

        # show the feed in a window
        cv2.imshow(mode, frame)
        
        # if esc the quit
        if cv2.waitKey(10) == 27:
            break
        elif cv2.waitKey(10) == 115:
            # if S then save a screenshot to the correct folder
            if mode == "ir":
                ir_out = Image.fromarray(frame)
                ir_out.save("calibrate/%s/%s.png" % (mode, f_num), 'png')
            else:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_out = Image.fromarray(rgb)
                rgb_out.save("calibrate/%s/%s.png" % (mode, f_num), 'png')
            f_num = f_num + 1

main()