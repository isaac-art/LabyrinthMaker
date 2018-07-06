import os
import shutil
import sys
import cv2
import numpy as np


def save(lab, img):
    if not os.path.exists("split/"):
        os.makedirs("split/")
    cv2.imwrite(('split/%s.png' % lab), img)
    return


def split(img, sz):
    height, width = img.shape
    for x in range(width // sz):
        for y in range(height // sz):
            # print("x:%s, x+sz:%s" % (x * sz, x * sz + sz))
            # print("y:%s, y+sz:%s" % (y * sz, y * sz + sz))
            # print("---")
            img_seg = img[y * sz:y * sz + sz, x * sz:x * sz + sz]
            lab = "x%s_y%s" % (x, y)
            save(lab, img_seg)
            y += sz
        x += sz
    return


def threshold(img):
    ret, thr = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    return sure_bg


def load(img_name):
    col = cv2.imread(img_name, 1)
    bw = cv2.imread(img_name, 0)
    return col, bw


def removeFiles(folder):
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        try:
            if os.path.isfile(filepath):
                os.unlink(filepath)
        except Exception as e:
            print(e)
            pass
    return


def main(img_name, sz):
    removeFiles("strips/")
    removeFiles("split/")
    removeFiles("mz/")
    col, bw = load(img_name)
    thr = threshold(bw)
    split(thr, sz)
    return True


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
