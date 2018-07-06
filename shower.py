import os
import sys
import time
import cv2
import random
import shutil
import numpy as np
from math import floor
from tomorrow import threads
from PIL import Image

import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler


class ImageMaker(FileSystemEventHandler):
    def update_image(x, y):

        return

    def parse_name(self, name):
        xxx, yyy = name.split("/")
        xx, yy = yyy.split("_")
        x = xx[1:]
        y = yy[1:-4]
        return int(x), int(y)


    def on_modified(self, event):
        # x, y = self.parse_name(event.src_path)
        # print("x:%s, y:%s" % (x, y))
        print("event type: %s, path : %s" % (event.event_type, event.src_path))


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = "live_mz/"
    event_handler = ImageMaker()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
