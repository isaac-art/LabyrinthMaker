import sys
import cv2
import OneTile
import numpy as np
from pseyepy import Camera
from tomorrow import threads
from skimage.measure import compare_ssim
from Mask import Mask
from RecursiveBacktracker import RecursiveBacktracker
from MaskedGrid import MaskedGrid

# setting globals
global processing
processing = False


@threads(20)
def drawTile(tile): 
    pil_im = Image.fromarray(tile)
    mask = Mask.from_img_data(tile)
    grid = MaskedGrid(mask)
    RecursiveBacktracker.on(grid)
    img = grid.to_png(cell_size=4, folder="live_full_mz", name="live_full_mz", save=False)
    return img


def processTiles(width, height, sz, bg):
    global processing
    tiles = []
    for x in range(width // sz):
        for y in range(height // sz):
            seg = bg[y * sz:y * sz + sz, x * sz:x * sz + sz]
            tile = drawTile(seg)
            tiles.append(tile)
            y += sz
        x += sz
    processing = False
    return tiles


def main(cam, show, pseye):
    global processing
    if pseye == 1:
        cap = Camera([0], fps=60, resolution=Camera.RES_LARGE, colour=False)
        frame, timestamp  = cap.read()
        # width, height = frame.shape
    else:
        cap = cv2.VideoCapture(cam)
    sz = 80
    run = True
    vals = {}

    tiles = []

    mz = cv2.imread("live_full_mz/live_full_mz.png")
    c = 1
    last_diff = 0

    # cv2.namedWindow("mz", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("mz", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    if show == 0:
        window = False
    else:
        window = True
    while(run):
        try:
            if pseye == 1:
                frame, timestamp = cap.read()
            else:
                ret, frame = cap.read()
            small = cv2.resize(frame, (0, 0), fx=0.18, fy=0.18)
            width, height = small.shape
            ret, thr = cv2.threshold(small, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = np.ones((1, 1), np.uint8)
            opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=2)
            bg = cv2.dilate(opening, kernel, iterations=3)
            
            if not processing:
                processing = True
                tiles = processTiles(width, height, sz, bg)
                for tile in tiles:
                    tile = np.array(tile)

            if window:
                # cv2.imshow('cam', bg)
                for i, tile in enumerate(tiles):
                    cv2.imshow(('%s' % i), tile)

            k = cv2.waitKey(1)
            if k == ord('q'):
                run = False
            c += 1
        except Exception as e:
            print(e)
            pass
    # program closing, stop camera stream and close windows
    if pseye == 1:
        cap.end()
    else:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # invoke: python sender_full.py cam_num show(0=false) pseye(0=false)
    cam = int(sys.argv[1])
    window = int(sys.argv[2])
    pseye = int(sys.argv[3])
    main(cam, window, pseye)
