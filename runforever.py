#!/usr/bin/python
from subprocess import Popen
import os
import sys
import time


# This is a python script that will restart the main script if it dies
# This can be killed by Ctrl-C or killall python


count = 0
# name of the file to run
filename = sys.argv[1]

# white True (forever)
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename , shell=True)
   
    # Immediately kill the process on the first two attempts
    # This is because the kinect has usb issues when first 
    # booting and causes the program to hang but not crash
    if count < 2:
        # wait a couple of seconds
        time.sleep(2)
        # kill it
        p.kill()
        count = count + 1
    else:
        # on third attempt leave runnning
        # it will run until the script exits
        p.wait()
        # time.sleep(3) 
        count = 0