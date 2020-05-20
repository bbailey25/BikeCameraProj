#!/usr/bin/env python2.7

import subprocess
from subprocess import call
import glob
import os
import datetime
import threading

SDcard_threshold = 58  # % of SD card above which we'll delete the oldest .h264 files
firstRecording = False

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
        print "SD card %s full. Not enough space left! Removing oldest .mp4 file" % storage[4]
        removeOldestFile()  # call our function to make some space on the card
        space_used()     # call this function recursively until enough space on card

###############################################################################
def removeOldestFile():

    try:
        list_of_files = glob.glob('/home/pi/Videos/*.mp4')
        oldest_file = min(list_of_files, key=os.path.getctime)
        os.remove(oldest_file)
        pass
    except ValueError:
        pass

###############################################################################
def writeRecNum(recNum):
    recFile = open("/home/pi/Videos/video_recording_number.txt", 'w')
    recFile.write(str(recNum))
    recFile.close()

###############################################################################
def getRecNum():
    recFile = open("/home/pi/Videos/video_recording_number.txt", 'r')
    rec_num = int(vrn.readline())
    print "rec_num is %d" % rec_num
    vrn.close()
    return rec_num

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
def convertToMp4(fileName):

    convertToMp4Cmd = "MP4Box -add /home/pi/Videos/" + fileName + ".h264 " + "/home/pi/Videos/" + fileName + ".mp4"
    call (convertToMp4Cmd, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

    fileLoc = "/home/pi/Videos/" + fileName + ".h264"
    os.remove(fileLoc)

###############################################################################
def streamRecordVideo():

    while True:
        space_used()
        dt = datetime.datetime.now()
        recordingNumber = getRecNum()
        title = ""
        if firstRecording:
            title = "_FirstRearCam_"
            firstRecording = False
        else:
            title = "_RearCam_"

        fileName = (recordingNumber + title + str(dt.month) + "-" + str(dt.day) + "-" +
                    str(dt.year) + "-" + str(dt.hour) + "-" + str(dt.minute) +
                    "-" + str(dt.second))

        command = "raspivid -t 3000 -vs -o /home/pi/Videos/" + fileName + ".h264"
        call (command, shell=True)
        writeRecNum(recordingNumber+=1)
        convertThread = threading.Thread(target=convertToMp4, args=(fileName,))
        convertThread.start()

###############################################################################
def main():

    removeH264Files()
    streamRecordVideo()

###############################################################################
if __name__ == '__main__':
    main()

###############################################################################
