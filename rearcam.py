#!/usr/bin/env python2.7

import subprocess
from subprocess import call
import glob
import os
import datetime
import threading

SDcard_threshold = 56  # % of SD card above which we'll delete the oldest .h264 files

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

def removeOldestFile():

    try:
        list_of_files = glob.glob('/home/pi/Videos/*.mp4')
        oldest_file = min(list_of_files, key=os.path.getctime)
        os.remove(oldest_file)
        pass
    except ValueError:
        pass

# def recordVideo():

def convertToMp4(fileName):

    convertToMp4Cmd = "MP4Box -add /home/pi/Videos/" + fileName + ".h264 " + "/home/pi/Videos/" + fileName + ".mp4"
    call (convertToMp4Cmd, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

    rmFilePath = "/home/pi/Videos/" + fileName + ".h264"
    os.remove(rmFilePath)

def streamRecordVideo():

    while True:
	space_used()
        dt = datetime.datetime.now()
        print dt
        fileName = ("RearCam_" + str(dt.month) + "-" + str(dt.day) + "-" +
		str(dt.year) + "-" + str(dt.hour) + "-" + str(dt.minute) +
		"_" + str(dt.second))
        command = "raspivid -t 3000 -vs -o /home/pi/Videos/" + fileName + ".h264"
        call (command, shell=True)
        convertThread = threading.Thread(target=convertToMp4, args=(fileName,))
        convertThread.start()

def main():

    streamRecordVideo()

###############################################################################
if __name__ == '__main__':
    main()

###############################################################################
