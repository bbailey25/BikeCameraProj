#!/usr/bin/env python2.7

import subprocess
from subprocess import call
import glob
import os
import datetime
import threading


import time
SDcard_threshold = 95  # % of SD card above which we'll delete the oldest .h264 files
VideoLength = 300000   # Length of video (seconds times 1000)

###############################################################################
def space_used():    # function displays amt of space left on device

    output_df = subprocess.Popen(["df", "-Ph"], stdout=subprocess.PIPE).communicate()[0]

    it_num = 0
    for line in output_df.split("\n"):
        line_list = line.split()
        if it_num == 1:
            storage = line_list
        it_num += 1
    print "Card size: %s Used: %s  Available: %s  Percent used: %s  SD Threshold: %d%%" % (storage[1], storage[2], storage[3], storage[4], SDcard_threshold)
    percent_used = int(storage[4][0:-1])

    if percent_used > SDcard_threshold:
        print "SD card %s full. Not enough space left! Removing oldest .h264 file" % storage[4]
        removeOldestFile()  # call our function to make some space on the card
        space_used()     # call this function recursively until enough space on card

###############################################################################
def removeOldestFile():

    try:
        list_of_files = glob.glob('/home/pi/Videos/*.h264')
        oldest_file = min(list_of_files, key=os.path.getctime)
        os.remove(oldest_file)
        pass
    except ValueError:
        pass

###############################################################################
def removeH264Files():

    directory = "/home/pi/Videos"
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".h264")]
    for file in filtered_files:
        print os.path.join(directory, file)
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

###############################################################################
def streamRecordVideo():

    firstRecording = True
    while True:
        space_used()
        dt = datetime.datetime.now()
        if firstRecording is True:
            title = "FirstRearCam_"
            firstRecording = False
        else:
            title = "RearCam_"

        fileName = (title + str(dt.month) + "-" + str(dt.day) + "-" +
                    str(dt.year) + "-" + str(dt.hour) + "-" + str(dt.minute) +
                    "-" + str(dt.second))

        command = "raspivid -t " + str(VideoLength) + " -vs -o /home/pi/Videos/" + fileName + ".h264 -b 8500000"
        call (command, shell=True)

###############################################################################
def main():

    streamRecordVideo()

###############################################################################
if __name__ == '__main__':
    main()

###############################################################################
