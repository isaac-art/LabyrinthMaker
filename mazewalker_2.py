import sys
from queue import Queue
from PIL import Image
from datetime import datetime


def isblack(val):
    # print(val)
    if val == (0, 0, 0):
        return True


def getneighbour(n):
    x, y = n
    return [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]


def makemaze(start, end, thresh_pix, out_pix, out_img):
    queue = Queue()
    queue.put([start])
    c = 0
    while not queue.empty():
        path = queue.get()
        pixel = path[-1]
        if pixel == end:
            # print(path)
            return path
        for neighbour in getneighbour(pixel):
            x, y = neighbour
            # print(neighbour)
            if x >= 1 and x <= 599 and y >= 1 and y <= 429:
                if not isblack(thresh_pix[x, y]):
                    thresh_pix[x, y] = (127, 127, 127)
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.put(new_path)

        if c % 20000 == 0:
            for position in path:
                x, y = position
                out_pix[x, y] = (255, 0, 0)
                # save maze image
                out_img.save("solved/o_%s.png" % c)

        c += 1
    return path


if __name__ == '__main__':
    startTime = datetime.now()
    # python mazeMaker.py threshed color out
    thresh_img = Image.open(sys.argv[1])
    thresh_img = thresh_img.convert('RGB')
    thresh_pix = thresh_img.load()
    # load the color image
    out_img = Image.open(sys.argv[2])
    out_pix = out_img.load()
    # make the path
    width, height = thresh_img.size
    start = (2, 4)
    end = (199, 199)
    path = makemaze(start, end, thresh_pix, out_pix, out_img)
    # load the color image
    out_img = Image.open(sys.argv[2])
    out_pix = out_img.load()
    # draw ontop of color image
    for position in path:
        x, y = position
        out_pix[x, y] = (255, 0, 0)
    # save maze image
    out_img.save(sys.argv[3])
    print("Completed In : %s" % (datetime.now() - startTime))

    # To get a gif, output several images and then
    # run 'convert -delay 5 -loop 1 *.jpg bfs.gif'
