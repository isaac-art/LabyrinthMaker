#!/usr/bin/python
from subprocess import Popen
import os
import sys
import time

filename = sys.argv[1]
while True:
    print("\nStarting " + filename)
    p = Popen("nohup python " + filename + " >/dev/null 2>&1 ", shell=True)
    p.wait()
    time.sleep(3) 