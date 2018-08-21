import cv2
import freenect
import numpy as np
import frame_convert2
from PIL import Image


global f_num
f_num = 0

global mode
mode = "rgb"

def kinect_get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])


def kinect_get_ir():
    array, t = freenect.sync_get_video(0,freenect.VIDEO_IR_10BIT)
    array = frame_convert2.pretty_depth_cv(array)
    return array


def main():
    global f_num
    cv2.namedWindow(mode)
    while 1:
        if mode == "ir":
            frame = kinect_get_ir()
        else:
            frame = kinect_get_video()

        cv2.imshow(mode, frame)
        
        if cv2.waitKey(10) == 27:
            break
        elif cv2.waitKey(10) == 115:
            if mode == "ir":
                ir_out = Image.fromarray(frame)
                ir_out.save("calibrate/%s/%s.png" % (mode, f_num), 'png')
            else:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_out = Image.fromarray(rgb)
                rgb_out.save("calibrate/%s/%s.png" % (mode, f_num), 'png')
            f_num = f_num + 1

main()